"""
Dosya Paylaşım Linki Modülü
Geçici paylaşım linkleri oluşturma ve yönetme
"""

import json
import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ShareLinkManager:
    def __init__(self, data_folder: str):
        self.data_folder = data_folder
        self.links_file = os.path.join(data_folder, 'share_links.json')
        
        if not os.path.exists(self.links_file):
            with open(self.links_file, 'w') as f:
                json.dump({}, f)
    
    def load_links(self) -> Dict:
        """Linkleri yükle"""
        try:
            with open(self.links_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_links(self, links: Dict):
        """Linkleri kaydet"""
        with open(self.links_file, 'w') as f:
            json.dump(links, f, indent=2, ensure_ascii=False)
    
    def create_link(
        self, 
        username: str, 
        filepath: str, 
        expires_hours: Optional[int] = None,
        password: Optional[str] = None,
        max_downloads: Optional[int] = None
    ) -> str:
        """Yeni paylaşım linki oluştur"""
        links = self.load_links()
        
        # Benzersiz token oluştur
        token = secrets.token_urlsafe(16)
        
        # Süre sonu hesapla
        expires_at = None
        if expires_hours:
            expires_at = (datetime.now() + timedelta(hours=expires_hours)).isoformat()
        
        links[token] = {
            'username': username,
            'filepath': filepath,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at,
            'password': password,
            'max_downloads': max_downloads,
            'download_count': 0,
            'is_active': True
        }
        
        self.save_links(links)
        return token
    
    def get_link(self, token: str) -> Optional[Dict]:
        """Link bilgilerini getir"""
        links = self.load_links()
        return links.get(token)
    
    def validate_link(self, token: str, password: Optional[str] = None) -> tuple[bool, str]:
        """Link geçerliliğini kontrol et"""
        link = self.get_link(token)
        
        if not link:
            return False, "Link bulunamadı"
        
        if not link.get('is_active'):
            return False, "Link devre dışı"
        
        # Süre kontrolü
        if link.get('expires_at'):
            expires_at = datetime.fromisoformat(link['expires_at'])
            if datetime.now() > expires_at:
                return False, "Link süresi dolmuş"
        
        # İndirme limiti kontrolü
        if link.get('max_downloads'):
            if link.get('download_count', 0) >= link['max_downloads']:
                return False, "İndirme limiti aşıldı"
        
        # Şifre kontrolü
        if link.get('password'):
            if not password or password != link['password']:
                return False, "Şifre gerekli veya hatalı"
        
        return True, "Geçerli"
    
    def increment_download_count(self, token: str):
        """İndirme sayısını artır"""
        links = self.load_links()
        
        if token in links:
            links[token]['download_count'] = links[token].get('download_count', 0) + 1
            self.save_links(links)
    
    def deactivate_link(self, token: str) -> bool:
        """Linki devre dışı bırak"""
        links = self.load_links()
        
        if token not in links:
            return False
        
        links[token]['is_active'] = False
        self.save_links(links)
        return True
    
    def delete_link(self, token: str) -> bool:
        """Linki sil"""
        links = self.load_links()
        
        if token not in links:
            return False
        
        del links[token]
        self.save_links(links)
        return True
    
    def get_user_links(self, username: str) -> List[Dict]:
        """Kullanıcının linklerini getir"""
        links = self.load_links()
        
        user_links = []
        for token, link_data in links.items():
            if link_data.get('username') == username:
                user_links.append({
                    'token': token,
                    **link_data
                })
        
        return user_links
    
    def cleanup_expired_links(self) -> int:
        """Süresi dolmuş linkleri temizle"""
        links = self.load_links()
        removed_count = 0
        
        tokens_to_remove = []
        for token, link_data in links.items():
            if link_data.get('expires_at'):
                expires_at = datetime.fromisoformat(link_data['expires_at'])
                if datetime.now() > expires_at:
                    tokens_to_remove.append(token)
        
        for token in tokens_to_remove:
            del links[token]
            removed_count += 1
        
        if removed_count > 0:
            self.save_links(links)
        
        return removed_count
    
    def get_all_links(self) -> List[Dict]:
        """Tüm linkleri getir (admin için)"""
        links = self.load_links()
        
        all_links = []
        for token, link_data in links.items():
            all_links.append({
                'token': token,
                **link_data
            })
        
        return all_links
    
    def get_all_active_links(self) -> List[Dict]:
        """Tüm aktif linkleri getir (herkese açık paylaşımlar için)"""
        links = self.load_links()
        
        active_links = []
        for token, link_data in links.items():
            # Sadece aktif linkleri al
            if not link_data.get('is_active'):
                continue
            
            # Süre kontrolü
            if link_data.get('expires_at'):
                expires_at = datetime.fromisoformat(link_data['expires_at'])
                if datetime.now() > expires_at:
                    continue
            
            # İndirme limiti kontrolü
            if link_data.get('max_downloads'):
                if link_data.get('download_count', 0) >= link_data['max_downloads']:
                    continue
            
            active_links.append({
                'token': token,
                'owner': link_data.get('username'),
                'filepath': link_data.get('filepath'),
                'created_at': link_data.get('created_at'),
                'download_count': link_data.get('download_count', 0),
                'password': link_data.get('password')
            })
        
        return active_links
