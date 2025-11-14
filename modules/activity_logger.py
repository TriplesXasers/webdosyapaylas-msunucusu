"""
Aktivite Loglama Modülü
Kullanıcı aktivitelerini ve sistem olaylarını kaydeder
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class ActivityLogger:
    def __init__(self, log_dir: str = 'logs'):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.activity_file = os.path.join(log_dir, 'activities.json')
        self.security_file = os.path.join(log_dir, 'security.json')
        
        # Log dosyalarını oluştur
        for file in [self.activity_file, self.security_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump([], f)
    
    def _write_log(self, log_file: str, entry: Dict):
        """Log dosyasına yaz"""
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
        
        logs.append(entry)
        
        # Son 10000 kaydı tut
        if len(logs) > 10000:
            logs = logs[-10000:]
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def log_login(self, username: str, ip: str, success: bool = True):
        """Giriş denemesini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'login_success' if success else 'login_failed',
            'username': username,
            'ip': ip,
            'success': success
        }
        self._write_log(self.security_file, entry)
    
    def log_logout(self, username: str, ip: str):
        """Çıkış işlemini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'logout',
            'username': username,
            'ip': ip
        }
        self._write_log(self.security_file, entry)
    
    def log_file_upload(self, username: str, filename: str, size: int, ip: str):
        """Dosya yükleme işlemini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'file_upload',
            'username': username,
            'filename': filename,
            'size': size,
            'ip': ip
        }
        self._write_log(self.activity_file, entry)
    
    def log_file_download(self, username: str, filename: str, ip: str):
        """Dosya indirme işlemini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'file_download',
            'username': username,
            'filename': filename,
            'ip': ip
        }
        self._write_log(self.activity_file, entry)
    
    def log_file_delete(self, username: str, filename: str, ip: str):
        """Dosya silme işlemini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'file_delete',
            'username': username,
            'filename': filename,
            'ip': ip
        }
        self._write_log(self.activity_file, entry)
    
    def log_folder_create(self, username: str, foldername: str, ip: str):
        """Klasör oluşturma işlemini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'folder_create',
            'username': username,
            'foldername': foldername,
            'ip': ip
        }
        self._write_log(self.activity_file, entry)
    
    def log_user_created(self, username: str, created_by: str, ip: str):
        """Yeni kullanıcı oluşturma işlemini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'user_created',
            'username': username,
            'created_by': created_by,
            'ip': ip
        }
        self._write_log(self.security_file, entry)
    
    def log_user_deleted(self, username: str, deleted_by: str, ip: str):
        """Kullanıcı silme işlemini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'user_deleted',
            'username': username,
            'deleted_by': deleted_by,
            'ip': ip
        }
        self._write_log(self.security_file, entry)
    
    def log_password_change(self, username: str, ip: str):
        """Şifre değişikliğini logla"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'password_change',
            'username': username,
            'ip': ip
        }
        self._write_log(self.security_file, entry)
    
    def get_recent_activities(self, limit: int = 50, activity_type: Optional[str] = None) -> List[Dict]:
        """Son aktiviteleri getir"""
        try:
            with open(self.activity_file, 'r') as f:
                logs = json.load(f)
            
            if activity_type:
                logs = [log for log in logs if log.get('type') == activity_type]
            
            return logs[-limit:][::-1]  # Son N kaydı ters sırada
        except:
            return []
    
    def get_security_logs(self, limit: int = 50, log_type: Optional[str] = None) -> List[Dict]:
        """Güvenlik loglarını getir"""
        try:
            with open(self.security_file, 'r') as f:
                logs = json.load(f)
            
            if log_type:
                logs = [log for log in logs if log.get('type') == log_type]
            
            return logs[-limit:][::-1]
        except:
            return []
    
    def get_user_activities(self, username: str, limit: int = 50) -> List[Dict]:
        """Belirli bir kullanıcının aktivitelerini getir"""
        try:
            with open(self.activity_file, 'r') as f:
                logs = json.load(f)
            
            user_logs = [log for log in logs if log.get('username') == username]
            return user_logs[-limit:][::-1]
        except:
            return []
    
    def get_failed_login_attempts(self, username: Optional[str] = None, hours: int = 24) -> List[Dict]:
        """Başarısız giriş denemelerini getir"""
        try:
            with open(self.security_file, 'r') as f:
                logs = json.load(f)
            
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            failed_logins = [
                log for log in logs 
                if log.get('type') == 'login_failed' 
                and datetime.fromisoformat(log['timestamp']) > cutoff_time
            ]
            
            if username:
                failed_logins = [log for log in failed_logins if log.get('username') == username]
            
            return failed_logins[::-1]
        except:
            return []
    
    def get_statistics(self) -> Dict:
        """Genel istatistikleri getir"""
        try:
            with open(self.activity_file, 'r') as f:
                activity_logs = json.load(f)
            
            with open(self.security_file, 'r') as f:
                security_logs = json.load(f)
            
            # Son 24 saat
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            recent_activities = [
                log for log in activity_logs 
                if datetime.fromisoformat(log['timestamp']) > cutoff_time
            ]
            
            recent_security = [
                log for log in security_logs 
                if datetime.fromisoformat(log['timestamp']) > cutoff_time
            ]
            
            return {
                'total_activities': len(activity_logs),
                'total_security_events': len(security_logs),
                'last_24h_activities': len(recent_activities),
                'last_24h_uploads': len([l for l in recent_activities if l.get('type') == 'file_upload']),
                'last_24h_downloads': len([l for l in recent_activities if l.get('type') == 'file_download']),
                'last_24h_logins': len([l for l in recent_security if l.get('type') == 'login_success']),
                'last_24h_failed_logins': len([l for l in recent_security if l.get('type') == 'login_failed'])
            }
        except:
            return {
                'total_activities': 0,
                'total_security_events': 0,
                'last_24h_activities': 0,
                'last_24h_uploads': 0,
                'last_24h_downloads': 0,
                'last_24h_logins': 0,
                'last_24h_failed_logins': 0
            }
