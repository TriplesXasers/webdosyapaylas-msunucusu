"""
Kullanıcı Yönetimi Modülü
Kullanıcı CRUD işlemleri ve kota yönetimi
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class UserManager:
    def __init__(self, users_file: str, data_folder: str):
        self.users_file = users_file
        self.data_folder = data_folder
        self.user_data_file = os.path.join(data_folder, 'user_data.json')
        
        # Kullanıcı veri dosyasını oluştur
        if not os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'w') as f:
                json.dump({}, f)
    
    def load_users(self) -> Dict:
        """Kullanıcıları yükle"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_users(self, users: Dict):
        """Kullanıcıları kaydet"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_user_data(self) -> Dict:
        """Kullanıcı verilerini yükle"""
        try:
            with open(self.user_data_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_user_data(self, data: Dict):
        """Kullanıcı verilerini kaydet"""
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Kullanıcı bilgilerini getir"""
        user_data = self.load_user_data()
        return user_data.get(username)
    
    def set_user_info(self, username: str, info: Dict):
        """Kullanıcı bilgilerini güncelle"""
        user_data = self.load_user_data()
        if username not in user_data:
            user_data[username] = {
                'created_at': datetime.now().isoformat(),
                'quota_mb': 1000,  # Varsayılan 1GB
                'is_active': True,
                'last_login': None,
                'total_uploads': 0,
                'total_downloads': 0
            }
        
        user_data[username].update(info)
        self.save_user_data(user_data)
    
    def create_user(self, username: str, password_hash: str, quota_mb: int = 1000) -> bool:
        """Yeni kullanıcı oluştur"""
        users = self.load_users()
        
        if username in users:
            return False
        
        users[username] = password_hash
        self.save_users(users)
        
        # Kullanıcı verilerini oluştur
        self.set_user_info(username, {
            'quota_mb': quota_mb,
            'is_active': True
        })
        
        return True
    
    def delete_user(self, username: str) -> bool:
        """Kullanıcıyı sil"""
        if username == 'admin':
            return False
        
        users = self.load_users()
        
        if username not in users:
            return False
        
        del users[username]
        self.save_users(users)
        
        # Kullanıcı verilerini sil
        user_data = self.load_user_data()
        if username in user_data:
            del user_data[username]
            self.save_user_data(user_data)
        
        return True
    
    def toggle_user_status(self, username: str) -> bool:
        """Kullanıcı durumunu değiştir (aktif/pasif)"""
        if username == 'admin':
            return False
        
        user_data = self.load_user_data()
        if username not in user_data:
            return False
        
        user_data[username]['is_active'] = not user_data[username].get('is_active', True)
        self.save_user_data(user_data)
        
        return True
    
    def is_user_active(self, username: str) -> bool:
        """Kullanıcı aktif mi kontrol et"""
        if username == 'admin':
            return True
        
        user_info = self.get_user_info(username)
        if not user_info:
            return True  # Veri yoksa varsayılan olarak aktif
        
        return user_info.get('is_active', True)
    
    def set_user_quota(self, username: str, quota_mb: int) -> bool:
        """Kullanıcı kotasını ayarla"""
        if username == 'admin':
            return False
        
        self.set_user_info(username, {'quota_mb': quota_mb})
        return True
    
    def get_user_quota(self, username: str) -> int:
        """Kullanıcı kotasını getir (MB)"""
        user_info = self.get_user_info(username)
        if not user_info:
            return 1000  # Varsayılan 1GB
        
        return user_info.get('quota_mb', 1000)
    
    def update_last_login(self, username: str):
        """Son giriş zamanını güncelle"""
        self.set_user_info(username, {
            'last_login': datetime.now().isoformat()
        })
    
    def increment_upload_count(self, username: str):
        """Yükleme sayısını artır"""
        user_info = self.get_user_info(username) or {}
        current_count = user_info.get('total_uploads', 0)
        self.set_user_info(username, {'total_uploads': current_count + 1})
    
    def increment_download_count(self, username: str):
        """İndirme sayısını artır"""
        user_info = self.get_user_info(username) or {}
        current_count = user_info.get('total_downloads', 0)
        self.set_user_info(username, {'total_downloads': current_count + 1})
    
    def get_all_users_info(self) -> List[Dict]:
        """Tüm kullanıcı bilgilerini getir"""
        users = self.load_users()
        user_data = self.load_user_data()
        
        result = []
        for username in users.keys():
            if username == 'admin':
                continue
            
            info = user_data.get(username, {})
            result.append({
                'username': username,
                'created_at': info.get('created_at', 'Bilinmiyor'),
                'quota_mb': info.get('quota_mb', 1000),
                'is_active': info.get('is_active', True),
                'last_login': info.get('last_login', 'Hiç giriş yapmadı'),
                'total_uploads': info.get('total_uploads', 0),
                'total_downloads': info.get('total_downloads', 0)
            })
        
        return result
    
    def reset_password(self, username: str, new_password_hash: str) -> bool:
        """Kullanıcı şifresini sıfırla"""
        users = self.load_users()
        
        if username not in users:
            return False
        
        users[username] = new_password_hash
        self.save_users(users)
        
        return True
