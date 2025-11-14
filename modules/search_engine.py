"""
Gelişmiş Arama Motoru
Dosya arama, filtreleme ve sıralama
"""

import os
from datetime import datetime
from typing import List, Dict, Optional

class SearchEngine:
    def __init__(self):
        self.supported_extensions = {
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'],
            'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'audio': ['.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac'],
            'document': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf'],
            'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c']
        }
    
    def search_files(
        self,
        base_path: str,
        query: Optional[str] = None,
        file_type: Optional[str] = None,
        min_size: Optional[int] = None,
        max_size: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        sort_by: str = 'name',
        sort_order: str = 'asc'
    ) -> List[Dict]:
        """Gelişmiş dosya arama"""
        results = []
        
        try:
            for root, dirs, files in os.walk(base_path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    
                    # Dosya bilgilerini al
                    try:
                        stat = os.stat(filepath)
                        file_info = {
                            'name': filename,
                            'path': os.path.relpath(filepath, base_path),
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime),
                            'extension': os.path.splitext(filename)[1].lower(),
                            'type': self._get_file_type(filename)
                        }
                        
                        # Filtreleri uygula
                        if not self._apply_filters(file_info, query, file_type, 
                                                   min_size, max_size, date_from, date_to):
                            continue
                        
                        results.append(file_info)
                    except:
                        continue
            
            # Sıralama
            results = self._sort_results(results, sort_by, sort_order)
            
        except Exception as e:
            print(f"Arama hatası: {e}")
        
        return results

    
    def _get_file_type(self, filename: str) -> str:
        """Dosya tipini belirle"""
        ext = os.path.splitext(filename)[1].lower()
        
        for file_type, extensions in self.supported_extensions.items():
            if ext in extensions:
                return file_type
        
        return 'other'
    
    def _apply_filters(
        self,
        file_info: Dict,
        query: Optional[str],
        file_type: Optional[str],
        min_size: Optional[int],
        max_size: Optional[int],
        date_from: Optional[str],
        date_to: Optional[str]
    ) -> bool:
        """Filtreleri uygula"""
        
        # İsim araması
        if query and query.lower() not in file_info['name'].lower():
            return False
        
        # Dosya tipi filtresi
        if file_type and file_info['type'] != file_type:
            return False
        
        # Boyut filtresi
        if min_size and file_info['size'] < min_size:
            return False
        if max_size and file_info['size'] > max_size:
            return False
        
        # Tarih filtresi
        if date_from:
            try:
                from_date = datetime.fromisoformat(date_from)
                if file_info['modified'] < from_date:
                    return False
            except:
                pass
        
        if date_to:
            try:
                to_date = datetime.fromisoformat(date_to)
                if file_info['modified'] > to_date:
                    return False
            except:
                pass
        
        return True
    
    def _sort_results(self, results: List[Dict], sort_by: str, sort_order: str) -> List[Dict]:
        """Sonuçları sırala"""
        reverse = (sort_order == 'desc')
        
        if sort_by == 'name':
            results.sort(key=lambda x: x['name'].lower(), reverse=reverse)
        elif sort_by == 'size':
            results.sort(key=lambda x: x['size'], reverse=reverse)
        elif sort_by == 'date':
            results.sort(key=lambda x: x['modified'], reverse=reverse)
        elif sort_by == 'type':
            results.sort(key=lambda x: x['type'], reverse=reverse)
        
        return results
    
    def get_statistics(self, base_path: str) -> Dict:
        """Dosya istatistikleri"""
        stats = {
            'total_files': 0,
            'total_size': 0,
            'by_type': {},
            'largest_files': []
        }
        
        all_files = []
        
        try:
            for root, dirs, files in os.walk(base_path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    try:
                        stat = os.stat(filepath)
                        file_type = self._get_file_type(filename)
                        
                        stats['total_files'] += 1
                        stats['total_size'] += stat.st_size
                        
                        if file_type not in stats['by_type']:
                            stats['by_type'][file_type] = {'count': 0, 'size': 0}
                        
                        stats['by_type'][file_type]['count'] += 1
                        stats['by_type'][file_type]['size'] += stat.st_size
                        
                        all_files.append({
                            'name': filename,
                            'size': stat.st_size,
                            'path': os.path.relpath(filepath, base_path)
                        })
                    except:
                        continue
            
            # En büyük 10 dosya
            all_files.sort(key=lambda x: x['size'], reverse=True)
            stats['largest_files'] = all_files[:10]
            
        except Exception as e:
            print(f"İstatistik hatası: {e}")
        
        return stats
