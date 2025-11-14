"""
Virüs Tarama Modülü
ClamAV kullanarak dosya güvenlik taraması
"""

import os
import subprocess
import hashlib
from typing import Tuple, Optional

class VirusScanner:
    def __init__(self):
        self.clamav_available = self._check_clamav()
        
    def _check_clamav(self) -> bool:
        """ClamAV kurulu mu kontrol et"""
        try:
            result = subprocess.run(['clamscan', '--version'], 
                                  capture_output=True, 
                                  timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def scan_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Dosyayı tara
        Returns: (is_safe, message)
        """
        if not os.path.exists(file_path):
            return False, "Dosya bulunamadı"
        
        # ClamAV varsa kullan
        if self.clamav_available:
            return self._scan_with_clamav(file_path)
        
        # ClamAV yoksa basit kontroller yap
        return self._basic_security_check(file_path)
    
    def _scan_with_clamav(self, file_path: str) -> Tuple[bool, str]:
        """ClamAV ile tara"""
        try:
            result = subprocess.run(
                ['clamscan', '--no-summary', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # ClamAV return codes:
            # 0 = temiz
            # 1 = virüs bulundu
            # 2 = hata
            
            if result.returncode == 0:
                return True, "Dosya güvenli"
            elif result.returncode == 1:
                # Virüs adını çıkar
                output = result.stdout
                if "FOUND" in output:
                    virus_name = output.split("FOUND")[0].split(":")[-1].strip()
                    return False, f"Tehdit tespit edildi: {virus_name}"
                return False, "Zararlı içerik tespit edildi"
            else:
                return False, "Tarama hatası"
                
        except subprocess.TimeoutExpired:
            return False, "Tarama zaman aşımına uğradı"
        except Exception as e:
            return False, f"Tarama hatası: {str(e)}"
    
    def _basic_security_check(self, file_path: str) -> Tuple[bool, str]:
        """Basit güvenlik kontrolleri (ClamAV yoksa)"""
        try:
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Şüpheli uzantılar
            dangerous_exts = [
                '.exe', '.bat', '.cmd', '.com', '.pif', '.scr',
                '.vbs', '.js', '.jar', '.msi', '.dll', '.sys',
                '.ps1', '.sh', '.app', '.deb', '.rpm'
            ]
            
            if file_ext in dangerous_exts:
                return False, f"Şüpheli dosya türü: {file_ext}"
            
            # Çok büyük dosyalar (10GB üzeri)
            if file_size > 10 * 1024 * 1024 * 1024:
                return False, "Dosya çok büyük (max 10GB)"
            
            # Dosya imzası kontrolü (magic bytes)
            if not self._check_file_signature(file_path, file_ext):
                return False, "Dosya imzası uyumsuz"
            
            return True, "Temel kontroller geçildi (ClamAV önerilir)"
            
        except Exception as e:
            return False, f"Kontrol hatası: {str(e)}"
    
    def _check_file_signature(self, file_path: str, expected_ext: str) -> bool:
        """Dosya magic bytes kontrolü"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
            
            # Yaygın dosya imzaları
            signatures = {
                '.pdf': [b'%PDF'],
                '.zip': [b'PK\x03\x04', b'PK\x05\x06'],
                '.rar': [b'Rar!\x1a\x07'],
                '.7z': [b'7z\xbc\xaf\x27\x1c'],
                '.jpg': [b'\xff\xd8\xff'],
                '.png': [b'\x89PNG'],
                '.gif': [b'GIF87a', b'GIF89a'],
                '.mp4': [b'\x00\x00\x00\x18ftypmp4', b'\x00\x00\x00\x1cftypmp4'],
                '.mp3': [b'ID3', b'\xff\xfb', b'\xff\xf3'],
            }
            
            if expected_ext in signatures:
                for sig in signatures[expected_ext]:
                    if header.startswith(sig):
                        return True
                return False
            
            # Bilinmeyen uzantılar için geçer
            return True
            
        except:
            return True
    
    def get_file_hash(self, file_path: str) -> Optional[str]:
        """Dosyanın SHA256 hash'ini al"""
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except:
            return None
    
    def is_available(self) -> bool:
        """ClamAV kullanılabilir mi?"""
        return self.clamav_available
