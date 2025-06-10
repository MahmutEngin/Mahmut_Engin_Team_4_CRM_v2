# VIT CRM Projesi: Excel Veri Yönetim Sistemi - README

## Proje Hakkında
Bu uygulama, VIT (Vizyoner İnovasyon ve Teknoloji) programı kapsamında, Excel tabanlı başvuru, mülakat ve mentor görüşmesi verilerini yönetmek için geliştirilmiş bir Customer Relationship Management (CRM) masaüstü aracıdır. Python ve PyQt6 kullanılarak hayata geçirilen bu sistem, Google Drive üzerinde tutulan karmaşık Excel verilerini daha erişilebilir, aranabilir ve yönetilebilir hale getirmeyi amaçlar.

## Özellikler
* **Güvenli Kullanıcı Girişi**: 'Kullanicilar.xlsx' dosyasından okunan kullanıcı adları, şifreler ve rollere (Admin/User) göre kimlik doğrulama.
* **Rol Tabanlı Menü Erişimi**: Kullanıcı rolüne göre dinamik olarak 'Tercihler - Admin' veya 'Tercihler' menülerine yönlendirme.
* **Özelleştirilmiş UI**: Qt Designer ile tasarlanmış, tutarlı arka plan renkleri, yuvarlak kenarlı butonlar ve hover/pressed efektleri içeren kullanıcı dostu arayüz.
* **Dinamik Excel Veri Yükleme**: 'data/' klasöründeki en güncel 'VIT_YYYY_MM_DD' formatlı klasörü otomatik olarak algılar ve içindeki 'Basvurular.xlsx', 'Mentor.xlsx', 'Mulakatlar.xlsx' gibi Excel dosyalarını yükler.
* **Detaylı Başvuru Yönetimi**:
    * İsim/soyisim bazında arama.
    * Tüm başvuruları görüntüleme.
    * Mentor görüşmesi tanımlanan/tanımlanmayanları listeleme.
    * **Mükerrer Kayıt Tespiti**: Aynı isim ve mail adresine sahip tekrarlayan adayları belirleme.
    * **Önceki VIT Kontrolü**: Adayın birden fazla VIT programına başvurup başvurmadığını görmek için VIT1, VIT2 ve mevcut başvurular arasında ortak adayları gösterme.
    * **Farklı Kayıtlar**: VIT1 ve VIT2'de ortak olmayan adayları listeleme.
    * **Filtrelenmiş Başvurular**: Mükerrer kayıtları hariç tutarak benzersiz başvuruları listeleme (bu seçenekler QComboBox ile birleştirilebilir).
* **Mentor Görüşmesi Takibi**:
    * İsim/soyisim bazında arama.
    * Tüm görüşmeleri görüntüleme.
    * 'Çoklu Sekme' (QComboBox) ile belirli tercihlere (örn: 'VIT projesinin tamamına katılması uygun olur') göre filtreleme.
* **Mülakat Sonuçları Yönetimi**:
    * İsim/soyisim bazında arama.
    * 'Projesi Gönderilmiş Olanlar' ve 'Projesi Gelmiş Olanlar'a göre filtreleme.
* **Admin Menüsü Entegrasyonu**:
    * Google Takvim'deki etkinlikleri çekme ve bir tabloda görüntüleme.
    * Takvimdeki etkinliklere kayıtlı e-posta adreslerine otomatik toplu mail gönderme.
* **Kolay Navigasyon**: Her modülden 'Tercihler' veya 'Tercihler-Admin' ekranlarına tek tıkla geri dönüş.

## Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Ön Gereksinimler
* **Python 3.8 veya üzeri** yüklü olmalıdır.
* **pip** (Python paket yöneticisi) yüklü olmalıdır.

### 2. Depoyu Klonlayın
Projeyi GitHub'dan yerel makinenize klonlayın ve proje dizinine gidin:
```bash
git clone [https://github.com/KULLANICI_ADINIZ/PROJE_ADINIZ.git](https://github.com/KULLANICI_ADINIZ/PROJE_ADINIZ.git)
cd PROJE_ADINIZ