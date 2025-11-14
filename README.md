<<<<<<< HEAD
# webdosyapaylas-msunucusu
Web Dosya Paylaşım Sunucu oluşturun, hemde localde güveli.
=======
# 🌐 Web Dosya Paylaşım Sunucusu

Python Flask ve PyQt5 ile geliştirilmiş modern, güvenli ve kullanıcı dostu web tabanlı dosya paylaşım uygulaması.

## ✨ Özellikler

### 📁 Dosya Yönetimi
- Sürükle-bırak ile dosya yükleme
- Çoklu dosya yükleme desteği
- Klasör oluşturma ve yönetimi
- Dosya ve klasör silme (çöp kutusu sistemi)
- Alt klasörlere gezinme

### 👁️ Dosya Önizleme
- **Resimler:** JPG, PNG, GIF, BMP, WebP, SVG
- **Videolar:** MP4, AVI, MKV, MOV, WebM
- **Sesler:** MP3, WAV, OGG, FLAC, M4A
- **Belgeler:** PDF, TXT, MD, JSON, XML, HTML, CSS, JS, Python
- **Arşivler:** ZIP, RAR, 7Z içerik görüntüleme ve çıkarma

### 🔗 Paylaşım Sistemi
- Geçici paylaşım linkleri oluşturma
- Şifre korumalı linkler
- İndirme limiti belirleme
- Süre sonu ayarlama
- Kendi linklerinizi ve başkalarının linklerini görüntüleme

### 🛡️ Güvenlik
- Otomatik virüs taraması (ClamAV entegrasyonu)
- Şüpheli dosya türlerini engelleme
- Dosya imzası (magic bytes) kontrolü
- SHA-256 şifreli kullanıcı hesapları
- Aktivite ve güvenlik logları
- Kullanıcı izolasyonu (her kullanıcı kendi klasöründe)

### 👤 Kullanıcı Sistemi
- Kayıt olma ve giriş yapma
- Kullanıcı profil ayarları
- Tema seçimi (açık/koyu)
- Dil desteği
- Kullanıcı istatistikleri

### 👑 Admin Paneli
- Kullanıcı yönetimi
- Sistem istatistikleri (CPU, RAM, Disk)
- Aktivite logları
- Güvenlik olayları
- Analitik raporlar
- Gelişmiş arama

### 🔍 Gelişmiş Özellikler
- Dosya arama motoru
- Arşiv içeriği görüntüleme
- Çöp kutusu sistemi
- Dosya önizleme
- Responsive tasarım (mobil uyumlu)

---

## 📦 Kurulum

### Windows

#### 1. Python Kurulumu
1. [Python 3.8+](https://www.python.org/downloads/) indirin ve kurun
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin

#### 2. Proje Kurulumu
```cmd
# Proje klasörüne gidin
cd Web-Dosya-Paylasim-Sunucusu

# Virtual environment oluşturun
python -m venv .venv

# Virtual environment'ı aktifleştirin
.venv\Scripts\activate

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Örnek konfigürasyon dosyalarını kopyalayın
copy users.json.example users.json
copy config.json.example config.json

# Gerekli klasörleri oluşturun
mkdir Shared Backup logs Veriler
```

#### 3. ClamAV Kurulumu (Opsiyonel - Virüs Taraması İçin)
1. [ClamAV for Windows](https://www.clamav.net/downloads) indirin
2. Kurulumu tamamlayın
3. ClamAV'ı PATH'e ekleyin
4. Virüs tanımlarını güncelleyin:
```cmd
freshclam
```

#### 4. Çalıştırma
```cmd
# Virtual environment aktifse
python main.py
```

---

### Ubuntu / Debian / Linux Mint

#### 1. Sistem Güncellemesi ve Gereksinimler
```bash
sudo apt update
sudo apt upgrade -y

# Python ve pip kurulumu
sudo apt install python3 python3-pip python3-venv -y

# PyQt5 için gerekli sistem paketleri
sudo apt install python3-pyqt5 libxcb-xinerama0 -y
```

#### 2. Proje Kurulumu
```bash
# Proje klasörüne gidin
cd Web-Dosya-Paylasim-Sunucusu

# Virtual environment oluşturun
python3 -m venv .venv

# Virtual environment'ı aktifleştirin
source .venv/bin/activate


# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Örnek konfigürasyon dosyalarını kopyalayın
cp users.json.example users.json
cp config.json.example config.json

# Gerekli klasörleri oluşturun
mkdir -p Shared Backup logs Veriler
```

#### 3. ClamAV Kurulumu (Opsiyonel - Virüs Taraması İçin)
```bash
# ClamAV kurulumu
sudo apt install clamav clamav-daemon -y

# Virüs tanımlarını güncelleyin
sudo freshclam

# ClamAV servisini başlatın
sudo systemctl start clamav-daemon
sudo systemctl enable clamav-daemon

# Servis durumunu kontrol edin
sudo systemctl status clamav-daemon
```

#### 4. Çalıştırma
```bash
# Virtual environment aktifse
python main.py
```

---

### macOS

#### 1. Homebrew Kurulumu (yoksa)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Python Kurulumu
```bash
# Python 3 kurulumu
brew install python@3.11

# Kurulumu doğrulayın
python3 --version
```

#### 3. Proje Kurulumu
```bash
# Proje klasörüne gidin
cd Web-Dosya-Paylasim-Sunucusu

# Virtual environment oluşturun
python3 -m venv .venv

# Virtual environment'ı aktifleştirin
source .venv/bin/activate

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Örnek konfigürasyon dosyalarını kopyalayın
cp users.json.example users.json
cp config.json.example config.json

# Gerekli klasörleri oluşturun
mkdir -p Shared Backup logs Veriler
```

#### 4. ClamAV Kurulumu (Opsiyonel - Virüs Taraması İçin)
```bash
# ClamAV kurulumu
brew install clamav

# Konfigürasyon dosyalarını oluşturun
cd /opt/homebrew/etc/clamav/
cp freshclam.conf.sample freshclam.conf
cp clamd.conf.sample clamd.conf

# Konfigürasyon dosyalarını düzenleyin (Example satırlarını kaldırın)
sed -i '' 's/^Example/#Example/' freshclam.conf
sed -i '' 's/^Example/#Example/' clamd.conf

# Virüs tanımlarını güncelleyin
freshclam

# ClamAV servisini başlatın
brew services start clamav
```

#### 5. Çalıştırma
```bash
# Virtual environment aktifse
python main.py
```

---

## 🚀 Kullanım

### İlk Başlatma

1. Uygulamayı çalıştırın:
```bash
python main.py
```

2. GUI penceresi açılacak:
   - Port numarasını seçin (varsayılan: 5000)
   - "🚀 Sunucuyu Başlat" butonuna tıklayın
   - Tarayıcınız otomatik olarak açılacak

3. İlk kullanım:
   - Kayıt ol sayfasından yeni hesap oluşturun
   - Veya admin hesabıyla giriş yapın

### Varsayılan Admin Hesabı

- **Kullanıcı adı:** `admin`
- **Şifre:** `admin`
- **⚠️ ÖNEMLİ:** İlk girişten sonra admin şifresini GUI'den mutlaka değiştirin!

### Temel İşlemler

#### Dosya Yükleme
1. Ana sayfada "📤 Dosya Yükle" butonuna tıklayın
2. Dosyaları seçin veya sürükle-bırak yapın
3. Dosyalar otomatik olarak virüs taramasından geçer

#### Klasör Oluşturma
1. "📁 Yeni Klasör" butonuna tıklayın
2. Klasör adını girin
3. Oluştur'a tıklayın

#### Dosya Paylaşma
1. Dosyaya sağ tıklayın veya "🔗 Paylaş" butonuna tıklayın
2. Paylaşım ayarlarını yapın:
   - Süre sonu (opsiyonel)
   - Şifre (opsiyonel)
   - İndirme limiti (opsiyonel)
3. Link oluştur
4. Linki kopyalayıp paylaşın

#### Dosya Önizleme
- Resim, video, ses, PDF veya metin dosyalarına "👁️ Önizle" butonuyla tıklayın

#### Arşiv İçeriği Görüntüleme
- ZIP, RAR veya 7Z dosyalarına "📦 İçeriği Gör" butonuyla tıklayın
- İçeriği normal klasöre çıkarabilirsiniz

---

## 🔧 Yapılandırma

### Port Değiştirme
GUI'den port numarasını değiştirin veya `config.json` dosyasını düzenleyin:
```json
{
  "last_port": 8080,
  "autostart": false
}
```

### Kullanıcı Ayarları
Her kullanıcı kendi ayarlarını `/settings` sayfasından yapabilir:
- Tema (Açık/Koyu)
- Dil
- Bildirimler

---

## 📊 Klasör Yapısı

```
Web-Dosya-Paylasim-Sunucusu/
├── main.py                 # Ana uygulama
├── requirements.txt        # Python bağımlılıkları
├── users.json             # Kullanıcı veritabanı
├── config.json            # Uygulama ayarları
├── modules/               # Modüller
│   ├── activity_logger.py
│   ├── analytics.py
│   ├── search_engine.py
│   ├── share_links.py
│   ├── user_manager.py
│   └── virus_scanner.py
├── templates/             # HTML şablonları
│   ├── admin/            # Admin paneli
│   ├── user/             # Kullanıcı sayfaları
│   └── shared/           # Paylaşılan sayfalar
├── Shared/               # Kullanıcı dosyaları
├── Backup/               # Çöp kutusu
├── Veriler/              # Uygulama verileri
└── logs/                 # Log dosyaları
```

---

## 🛡️ Güvenlik

### Virüs Taraması
- ClamAV kuruluysa: Tam virüs taraması
- ClamAV yoksa: Temel güvenlik kontrolleri
  - Şüpheli uzantılar engellenir (.exe, .bat, .sh, vb.)
  - Dosya imzası kontrolü
  - Maksimum dosya boyutu kontrolü (10GB)

### Engellenen Dosya Türleri (ClamAV yoksa)
`.exe`, `.bat`, `.cmd`, `.com`, `.pif`, `.scr`, `.vbs`, `.js`, `.jar`, `.msi`, `.dll`, `.sys`, `.ps1`, `.sh`, `.app`, `.deb`, `.rpm`

### Güvenlik Önerileri
1. ✅ Admin şifresini hemen değiştirin
2. ✅ ClamAV kurun ve güncel tutun
3. ✅ Sunucuyu internete açarken güvenlik duvarı kuralları ekleyin
4. ✅ Düzenli olarak logları kontrol edin
5. ✅ Güçlü şifreler kullanın
6. ✅ Kullanıcı izinlerini düzenli kontrol edin

---

## 🐛 Sorun Giderme

### Port zaten kullanımda
```bash
# Linux/Mac - Portu kullanan işlemi bulun
sudo lsof -i :5000

# Windows - Portu kullanan işlemi bulun
netstat -ano | findstr :5000

# Farklı bir port kullanın
```

### PyQt5 kurulum hatası (Linux)
```bash
sudo apt install python3-pyqt5 libxcb-xinerama0
```

### ClamAV çalışmıyor
```bash
# Servis durumunu kontrol edin
sudo systemctl status clamav-daemon

# Yeniden başlatın
sudo systemctl restart clamav-daemon

# Virüs tanımlarını güncelleyin
sudo freshclam
```

### Virtual environment aktifleşmiyor
```bash
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

---

## 📧 İletişim

Sorularınız veya önerileriniz için issue açabilirsiniz.

---

## 🙏 Teşekkürler

- Flask - Web framework
- PyQt5 - GUI framework
- ClamAV - Virüs tarama motoru
- Tüm katkıda bulunanlara

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!**
>>>>>>> c0cabdb (Yaptığım değişiklikler)
