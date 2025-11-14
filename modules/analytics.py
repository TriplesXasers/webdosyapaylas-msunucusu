"""
Analitik ve Grafik Raporlama Modülü
Chart.js için veri hazırlama
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict

class Analytics:
    def __init__(self, activity_logger, user_manager):
        self.activity_logger = activity_logger
        self.user_manager = user_manager
    
    def get_activity_chart_data(self, days: int = 7) -> Dict:
        """Son N günün aktivite grafiği"""
        activities = self.activity_logger.get_recent_activities(limit=1000)
        
        # Tarih bazlı gruplama
        date_counts = defaultdict(lambda: {'uploads': 0, 'downloads': 0, 'deletes': 0})
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for activity in activities:
            try:
                activity_date = datetime.fromisoformat(activity['timestamp'])
                if activity_date < cutoff_date:
                    continue
                
                date_key = activity_date.strftime('%Y-%m-%d')
                
                if activity['type'] == 'file_upload':
                    date_counts[date_key]['uploads'] += 1
                elif activity['type'] == 'file_download':
                    date_counts[date_key]['downloads'] += 1
                elif activity['type'] == 'file_delete':
                    date_counts[date_key]['deletes'] += 1
            except:
                continue
        
        # Son N günü oluştur
        labels = []
        uploads = []
        downloads = []
        deletes = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            date_key = date.strftime('%Y-%m-%d')
            labels.append(date.strftime('%d.%m'))
            
            uploads.append(date_counts[date_key]['uploads'])
            downloads.append(date_counts[date_key]['downloads'])
            deletes.append(date_counts[date_key]['deletes'])
        
        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Yükleme',
                    'data': uploads,
                    'borderColor': '#28a745',
                    'backgroundColor': 'rgba(40, 167, 69, 0.1)',
                    'tension': 0.4
                },
                {
                    'label': 'İndirme',
                    'data': downloads,
                    'borderColor': '#007bff',
                    'backgroundColor': 'rgba(0, 123, 255, 0.1)',
                    'tension': 0.4
                },
                {
                    'label': 'Silme',
                    'data': deletes,
                    'borderColor': '#dc3545',
                    'backgroundColor': 'rgba(220, 53, 69, 0.1)',
                    'tension': 0.4
                }
            ]
        }

    
    def get_user_storage_chart(self) -> Dict:
        """Kullanıcı depolama dağılımı (Pasta grafik)"""
        users = self.user_manager.get_all_users_info()
        
        labels = []
        data = []
        colors = [
            '#667eea', '#764ba2', '#f093fb', '#4facfe',
            '#43e97b', '#fa709a', '#fee140', '#30cfd0'
        ]
        
        for i, user in enumerate(users[:8]):  # İlk 8 kullanıcı
            labels.append(user['username'])
            # Kullanıcının klasör boyutunu hesapla (simüle)
            data.append(user.get('total_uploads', 0) * 10)  # Yaklaşık
        
        return {
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': colors[:len(labels)],
                'borderWidth': 2,
                'borderColor': '#fff'
            }]
        }
    
    def get_file_type_distribution(self, base_path: str) -> Dict:
        """Dosya tipi dağılımı"""
        import os
        
        type_counts = defaultdict(int)
        
        try:
            for root, dirs, files in os.walk(base_path):
                for filename in files:
                    ext = os.path.splitext(filename)[1].lower()
                    
                    # Dosya tipini belirle
                    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                        type_counts['Resim'] += 1
                    elif ext in ['.mp4', '.avi', '.mkv', '.mov']:
                        type_counts['Video'] += 1
                    elif ext in ['.mp3', '.wav', '.ogg', '.flac']:
                        type_counts['Müzik'] += 1
                    elif ext in ['.pdf', '.doc', '.docx', '.txt']:
                        type_counts['Doküman'] += 1
                    elif ext in ['.zip', '.rar', '.7z']:
                        type_counts['Arşiv'] += 1
                    else:
                        type_counts['Diğer'] += 1
        except:
            pass
        
        return {
            'labels': list(type_counts.keys()),
            'datasets': [{
                'data': list(type_counts.values()),
                'backgroundColor': [
                    '#667eea', '#764ba2', '#f093fb', 
                    '#4facfe', '#43e97b', '#fa709a'
                ],
                'borderWidth': 2,
                'borderColor': '#fff'
            }]
        }
    
    def get_hourly_activity(self) -> Dict:
        """Saatlik aktivite dağılımı"""
        activities = self.activity_logger.get_recent_activities(limit=500)
        
        hour_counts = [0] * 24
        
        for activity in activities:
            try:
                activity_time = datetime.fromisoformat(activity['timestamp'])
                hour_counts[activity_time.hour] += 1
            except:
                continue
        
        return {
            'labels': [f'{i:02d}:00' for i in range(24)],
            'datasets': [{
                'label': 'Aktivite Sayısı',
                'data': hour_counts,
                'backgroundColor': 'rgba(102, 126, 234, 0.5)',
                'borderColor': '#667eea',
                'borderWidth': 2
            }]
        }
    
    def get_top_users(self, limit: int = 10) -> Dict:
        """En aktif kullanıcılar"""
        users = self.user_manager.get_all_users_info()
        
        # Aktiviteye göre sırala
        sorted_users = sorted(
            users, 
            key=lambda x: x.get('total_uploads', 0) + x.get('total_downloads', 0),
            reverse=True
        )[:limit]
        
        labels = [u['username'] for u in sorted_users]
        uploads = [u.get('total_uploads', 0) for u in sorted_users]
        downloads = [u.get('total_downloads', 0) for u in sorted_users]
        
        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Yükleme',
                    'data': uploads,
                    'backgroundColor': '#28a745'
                },
                {
                    'label': 'İndirme',
                    'data': downloads,
                    'backgroundColor': '#007bff'
                }
            ]
        }
    
    def get_summary_stats(self) -> Dict:
        """Özet istatistikler"""
        stats = self.activity_logger.get_statistics()
        users = self.user_manager.get_all_users_info()
        
        return {
            'total_users': len(users),
            'active_users': len([u for u in users if u.get('is_active', True)]),
            'total_activities': stats.get('total_activities', 0),
            'last_24h_uploads': stats.get('last_24h_uploads', 0),
            'last_24h_downloads': stats.get('last_24h_downloads', 0),
            'last_24h_logins': stats.get('last_24h_logins', 0),
            'failed_logins': stats.get('last_24h_failed_logins', 0)
        }
