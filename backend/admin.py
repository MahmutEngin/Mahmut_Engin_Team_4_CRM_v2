from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6 import uic, QtWidgets
import os
from . import get_events
import sys
import smtplib
from email.message import EmailMessage
# from email.mime.text import MIMEText

class AdminPage(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # UI dosyasının yüklenmesi
        try:
            # Uygulamanın PyInstaller ile mi yoksa normal Python ile mi çalıştığını kontrol et
            if getattr(sys, 'frozen', False):
                # PyInstaller ile paketlenmişse, _MEIPASS geçici dizinin yolunu verir
                app_root_path = sys._MEIPASS
            else:
                # Normal Python betiği olarak çalışıyorsa
                # Bu kod bloğunun bulunduğu dosya (örn. admin.py) 'backend' klasöründe ise,
                # projenin ana kök dizinine (CRM_V2) ulaşmak için bir üst dizine çıkmalıyız.
                current_script_dir = os.path.dirname(os.path.abspath(__file__))
                app_root_path = os.path.abspath(os.path.join(current_script_dir, os.pardir))

            # UI dosyasının tam yolunu oluştur
            # PyInstaller'a "--add-data 'ui;ui'" dediğimiz için,
            # 'ui' klasörü exe'nin çıkarıldığı geçici dizinin doğrudan içinde yer alacaktır.
            ui_file_name = "admin_page_python.ui" # Yüklenecek .ui dosyasının adı
            ui_file_path = os.path.join(app_root_path, "ui", ui_file_name)

            # print(f"Yüklenmeye çalışılan UI dosya yolu: {ui_file_path}") # Hata ayıklama için

            # UI dosyasını yükle
            uic.loadUi(ui_file_path, self) # 'self' mevcut sınıf örneğinizdir.

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "UI Yükleme Hatası", f"UI dosyası yüklenemedi: {e}")
            # Hata durumunda uygulamanın ne yapacağını belirleyin, örneğin uygulamayı kapatabilirsiniz.
            # QApplication.instance().quit()


        # .ui dosyasını doğrudan yükle
        # ui_path = os.path.join(os.path.dirname(__file__), "..", "ui",'admin_page_python.ui')
        # uic.loadUi(ui_path, self)


        self.sayfa = None
         #ui ogelerine erisim 
        self.pushButton_etkinlikkontrolu = self.findChild(QtWidgets.QPushButton,"pushButton_etkinlikkontrolu")
        self.pushButton_mailgonder = self.findChild(QtWidgets.QPushButton,"pushButton_mailgonder")
        self.pushButton_tercihler = self.findChild(QtWidgets.QPushButton,"pushButton_tercihler")
        self.pushButton_exit = self.findChild(QtWidgets.QPushButton,"pushButton_exit")
        self.tableWidget_show = self.findChild(QtWidgets.QTableWidget,"tableWidget_show")
        #temel tablo islemleri 
        # temel tablo islemleri
        # tableWidget_show artık tanımlı olduğu için bu satır sorun çıkarmayacak
        self.olaylar = get_events.main()
        if self.olaylar: # Olaylar listesi boş olabilir, kontrol ekleyelim
            self.tableWidget_show.setRowCount(len(self.olaylar))
            self.etkinliklerin_kontrolu() # Başlangıçta tabloyu doldurmak için çağırabilirsiniz
        

    


        #olaylar
        self.pushButton_etkinlikkontrolu.clicked.connect(self.etkinliklerin_kontrolu)
        self.pushButton_mailgonder.clicked.connect(self.mailadreslerine_gonder)
        self.pushButton_tercihler.clicked.connect(self.sayfayaGeriDon)
        self.pushButton_exit.clicked.connect(self.uygulama_kapatma)
     
    #fonksiyonlar
        
    def etkinliklerin_kontrolu(self):
        self.olaylar = get_events.main()  # En güncel olayları çekmek için
        if not self.olaylar:
            self.tableWidget_show.setRowCount(0)
            return

        self.tableWidget_show.clear()  # Önceki verileri temizle
        self.tableWidget_show.setRowCount(len(self.olaylar))
        self.tableWidget_show.setColumnCount(5)
        self.tableWidget_show.setHorizontalHeaderLabels(["#", "Start", "Attendees", "Organizer", "Title"])

        for row, event in enumerate(self.olaylar):
            title = event.get('summary', 'Başlıksız')
            start = event['start'].get('dateTime', event['start'].get('date', ''))
            organizer = event.get('organizer', {}).get('email', '')
            attendees = event.get('attendees', [])
            attendee_emails = ', '.join([a['email'] for a in attendees]) if attendees else ''

            self.tableWidget_show.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row + 1)))
            self.tableWidget_show.setItem(row, 1, QtWidgets.QTableWidgetItem(str(start)))
            self.tableWidget_show.setItem(row, 2, QtWidgets.QTableWidgetItem(str(attendee_emails)))
            self.tableWidget_show.setItem(row, 3, QtWidgets.QTableWidgetItem(str(organizer)))
            self.tableWidget_show.setItem(row, 4, QtWidgets.QTableWidgetItem(str(title)))

        self.tableWidget_show.resizeColumnsToContents()


    def mailadreslerine_gonder(self):
        # Kullanıcıdan konu ve mesajı al
        konu, ok = QtWidgets.QInputDialog.getText(self, 'E-posta Konusu', 'E-postanın konusunu girin:')
        if not ok or not konu:
            QtWidgets.QMessageBox.information(self, "Bilgi", "E-posta konusu boş bırakılamaz veya işlem iptal edildi.")
            return

        mesaj, ok = QtWidgets.QInputDialog.getMultiLineText(self, 'E-posta Mesajı', 'E-posta mesajını girin:')
        if not ok or not mesaj:
            QtWidgets.QMessageBox.information(self, "Bilgi", "E-posta mesajı boş bırakılamaz veya işlem iptal edildi.")
            return

        # self.olaylar listesindeki tüm katılımcı e-postalarını topla
        tum_katilimci_mailleri = set()
        for event in self.olaylar:
            attendees = event.get('attendees', [])
            for attendee in attendees:
                if 'email' in attendee:
                    # E-posta adresini temizle ve sete ekle
                    email = attendee['email'].strip().lower()
                    if email: # Boş e-posta adreslerini atla
                        tum_katilimci_mailleri.add(email)

        if not tum_katilimci_mailleri:
            QtWidgets.QMessageBox.information(self, "Bilgi", "Hiç katılımcı e-postası bulunamadı. Mail gönderilemiyor.")
            return

        # E-posta adreslerini virgülle ayrılmış tek bir string haline getir
        kime_str = ", ".join(tum_katilimci_mailleri)

        # E-posta gönderme fonksiyonu
        def eposta_gonder(konu,mesaj,kime):
            msg = EmailMessage()
            msg.set_content(mesaj)
            msg["Subject"] = konu
            msg["From"] = "mahmutengin.nl@gmail.com"
            msg["To"] = kime_str # Birden fazla alıcıyı burada tek string olarak gönderiyoruz

            # Buradaki şifre, uygulamanızın dağıtımı için güvenli değildir.
            # Gerçek uygulamalarda bu tür bilgileri doğrudan kodda tutmayın.
            password = "ffta rhre pzwo tjqb" # Bu şifre Google App Password olmalı

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(msg["From"], password)
                server.send_message(msg)
                server.quit()
                QtWidgets.QMessageBox.information(self, "Başarılı", "E-posta başarıyla gönderildi!")
                print("Mesaj gönderildi:", kime_str) # Konsola da yazdırabiliriz
            except smtplib.SMTPAuthenticationError:
                QtWidgets.QMessageBox.critical(self, "Hata", "E-posta kimlik doğrulaması başarısız oldu. Lütfen gönderen e-posta adresinizi ve şifrenizi kontrol edin (uygulama şifresi kullanın).")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Hata", f"E-posta gönderilirken bir hata oluştu: {e}")

        # E-postayı gönder
        eposta_gonder(konu, mesaj, kime_str)
    
    def diger_sayfa(self,page):
        self.sayfa = page

    def uygulama_kapatma(self):
        self.close()

    def sayfayaGeriDon(self):
        self.sayfa.show()
        self.hide()

    