# Requirements Document

## Introduction

`main.py` çalıştırıldığında port 11111'de web tabanlı admin kontrol paneli açılır. Bu panel sadece adminler içindir ve kullanıcı dosya sunucusunu başlatmak/durdurmak için kullanılır. Normal kullanıcılar için dosya sunucusu, admin panelinden seçilen portta başlatılır.

## Glossary

- **main.py**: Uygulamanın ana dosyası (eski adı: gui.py)
- **Admin Panel**: Port 11111'de çalışan yönetim arayüzü (sadece adminler için)
- **User Server**: Normal kullanıcıların dosya yönetimi yaptığı sunucu (admin panelinden başlatılır)
- **Admin Password**: Admin paneline giriş şifresi (varsayılan: admin1303)
- **Console**: Sunucu loglarının gösterildiği terminal benzeri alan
- **Control Port**: Admin panelinin çalıştığı port (11111 - sabit)
- **User Port**: Kullanıcı sunucusunun çalıştığı port (admin tarafından seçilir)

## Requirements

### Requirement 1

**User Story:** Admin olarak, main.py çalıştırdığımda web arayüzü açılmasını istiyorum, böylece tarayıcıdan yönetim yapabilirim

#### Acceptance Criteria

1. WHEN main.py çalıştırıldığında, THE System SHALL port 11111'de admin panelini başlatacak
2. THE System SHALL konsola erişim bilgilerini yazdıracak (http://localhost:11111)
3. WHEN admin paneline (port 11111) erişildiğinde, THE System SHALL şifre giriş ekranı gösterecek
4. WHEN doğru şifre girildiğinde, THE System SHALL yönetim panelini açacak
5. WHEN yanlış şifre girildiğinde, THE System SHALL hata mesajı gösterecek
6. THE System SHALL her girişte şifre isteyecek (session yok)
7. THE System SHALL normal kullanıcıların port 11111'e erişmesini engelleyecek

### Requirement 2

**User Story:** Admin olarak, kullanıcı dosya sunucusunu başlatmak istiyorum, böylece normal kullanıcılar dosya paylaşabilir

#### Acceptance Criteria

1. THE Admin Panel SHALL port numarası girme alanı içerecek
2. THE Admin Panel SHALL "Kullanıcı Sunucusunu Başlat" butonu içerecek
3. WHEN "Kullanıcı Sunucusunu Başlat" butonuna tıklandığında, THE System SHALL girilen portta kullanıcı sunucusunu başlatacak
4. WHEN kullanıcı sunucusu başlatıldığında, THE System SHALL konsola başlatma logları yazacak
5. THE System SHALL kullanıcı sunucusu çalışırken başlat butonunu devre dışı bırakacak
6. THE System SHALL kullanıcı sunucusu URL'ini konsola yazdıracak (http://localhost:PORT)
7. THE Admin Panel SHALL admin panelinden (port 11111) bağımsız çalışacak

### Requirement 3

**User Story:** Admin olarak, çalışan kullanıcı sunucusunu durdurmak istiyorum, böylece bakım yapabilirim

#### Acceptance Criteria

1. THE Admin Panel SHALL "Kullanıcı Sunucusunu Durdur" butonu içerecek
2. WHEN kullanıcı sunucusu çalışmıyorken, THE System SHALL durdur butonunu devre dışı bırakacak
3. WHEN "Kullanıcı Sunucusunu Durdur" butonuna tıklandığında, THE System SHALL kullanıcı sunucusunu kapatacak
4. WHEN kullanıcı sunucusu durdurulduğunda, THE System SHALL konsola durdurma logları yazacak
5. THE System SHALL admin panelini (port 11111) çalışır durumda tutacak

### Requirement 4

**User Story:** Admin olarak, admin paneli şifresini değiştirmek istiyorum, böylece güvenliği artırabilirim

#### Acceptance Criteria

1. THE Admin Panel SHALL "Admin Şifresi Değiştir" bölümü içerecek
2. THE System SHALL yeni şifre girme alanı sunacak
3. WHEN yeni şifre girilip kaydedildiğinde, THE System SHALL şifreyi güncelleyecek
4. THE System SHALL şifre değişikliğini konsola logla yacak
5. THE System SHALL minimum 4 karakter şifre zorunluluğu uygulayacak

### Requirement 5

**User Story:** Admin olarak, kullanıcı istatistiklerini görmek istiyorum, böylece sistem kullanımını takip edebilirim

#### Acceptance Criteria

1. THE Admin Panel SHALL toplam kullanıcı sayısını gösterecek
2. THE Admin Panel SHALL her kullanıcının kapladığı alanı gösterecek
3. THE Admin Panel SHALL Shared klasörünün toplam boyutunu gösterecek
4. THE System SHALL istatistikleri otomatik güncelleyecek (her 10 saniyede)

### Requirement 6

**User Story:** Admin olarak, sunucu loglarını görmek istiyorum, böylece neler olduğunu takip edebilirim

#### Acceptance Criteria

1. THE Admin Panel SHALL konsol alanı içerecek
2. THE Console SHALL terminal benzeri görünüme sahip olacak
3. WHEN sunucu başlatıldığında, THE Console SHALL başlatma loglarını gösterecek
4. WHEN dosya yüklendiğinde, THE Console SHALL yükleme loglarını gösterecek (IP, dosya adı, boyut)
5. THE Console SHALL otomatik scroll yapacak (en son log görünür)
6. THE Console SHALL maksimum 1000 satır log tutacak

### Requirement 7

**User Story:** Admin olarak, sistem kaynaklarını görmek istiyorum, böylece sunucu performansını izleyebilirim

#### Acceptance Criteria

1. THE Admin Panel SHALL CPU kullanım yüzdesini gösterecek
2. THE Admin Panel SHALL RAM kullanım yüzdesini gösterecek
3. THE Admin Panel SHALL Shared klasör boyutunu gösterecek
4. THE System SHALL sistem istatistiklerini otomatik güncelleyecek (her 2 saniyede)

### Requirement 8

**User Story:** Admin olarak, son kullanılan portu hatırlamak istiyorum, böylece her seferinde girmek zorunda kalmayayım

#### Acceptance Criteria

1. THE System SHALL son kullanılan port numarasını kaydedecek
2. WHEN admin paneli açıldığında, THE System SHALL son kullanılan portu varsayılan olarak gösterecek
3. THE System SHALL port numarasını config.json dosyasında saklayacak
