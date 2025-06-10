import openpyxl
import os 
from PyQt6.QtWidgets import QMainWindow, QMessageBox # QMessageBox'ı hata mesajları için ekledik
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import QTimer
import sys # sys modülünü import ettiğinizden emin olun!


class LoginPage(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # Uygulamanın PyInstaller ile mi yoksa normal Python ile mi çalıştığını kontrol et
        if getattr(sys, 'frozen', False):
            # PyInstaller ile paketlenmişse, _MEIPASS geçici dizinin yolunu verir
            app_root_path = sys._MEIPASS
        else:
            # Normal Python betiği olarak çalışıyorsa
            # Bu dosya (login.py) backend klasörünün içinde olmalı.
            # Projenin ana kök dizinine (CRM_V2) ulaşmak için 'backend'den bir üst dizine çıkmalıyız.
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            app_root_path = os.path.abspath(os.path.join(current_script_dir, os.pardir))

        # .ui dosyasının yolunu oluştur
        ui_path = os.path.join(app_root_path, "ui", 'login_page_python.ui')

        # .ui dosyasını yükle
        try:
            uic.loadUi(ui_path, self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"UI dosyası yüklenemedi: {ui_path}\nHata: {e}")
            sys.exit(1) # Hata durumunda uygulamayı kapat

        self.basvuruform = None
        self.mulakatlarform = None
        self.mentorform = None
        self.adminform  = None
        self.tercihlerAdmin = None
        self.tercihlerKullanici = None


        #ui ogelerine erisim 
        self.pushButton_login = self.findChild(QtWidgets.QPushButton,"pushButton_login")
        self.pushButton_exit = self.findChild(QtWidgets.QPushButton,"pushButton_exit")
        self.lineEdit_username = self.findChild(QtWidgets.QLineEdit,"lineEdit_username")
        self.lineEdit_password = self.findChild(QtWidgets.QLineEdit,"lineEdit_password")
        self.label_bilgilendirme = self.findChild(QtWidgets.QLabel,"label_bilgilendirme")


        #olaylar 
        self.pushButton_login.clicked.connect(self.girisyap)
        self.pushButton_exit.clicked.connect(self.uygulama_kapatma)


    #gerekli sayfalarin aktarilmasi
    def diger_sayfalar(self,basvuruform,mulakatlarform,mentorform,adminform,tercihlerKullanici,tercihlerAdmin):
        self.basvuruform_lg = basvuruform
        self.mulakatlarform_lg = mulakatlarform
        self.mentorform_lg = mentorform
        self.adminform_lg  = adminform
        self.tercihlerAdmin_lg = tercihlerAdmin
        self.tercihlerKullanici_lg = tercihlerKullanici

    def girisyap(self):
        kullaniciAdi = self.lineEdit_username.text()
        sifre = self.lineEdit_password.text()
        
        #dosya islemleri(verilerin cekilmesi)
        try:
            # Uygulamanın PyInstaller ile mi yoksa normal Python ile mi çalıştığını kontrol et
            if getattr(sys, 'frozen', False):
                app_root_path = sys._MEIPASS
            else:
                current_script_dir = os.path.dirname(os.path.abspath(__file__))
                app_root_path = os.path.abspath(os.path.join(current_script_dir, os.pardir))

            # Kullanicilar.xlsx dosyasının tam yolu - BURAYI GÜNCELLEDİK!
            kullanicilar_excel_path = os.path.join(app_root_path, "data", "Kullanicilar.xlsx")

            # Dosyanın gerçekten var olup olmadığını kontrol et
            if not os.path.exists(kullanicilar_excel_path):
                # Kullanıcıya hata mesajı göster ve fonksiyonu sonlandır
                QMessageBox.critical(self, "Hata", f"Kullanicilar.xlsx dosyası bulunamadı: {kullanicilar_excel_path}")
                return # Buradan sonraki kodun çalışmasını durdurur

            # Excel dosyasını yükle - ŞİMDİ DOĞRU YOL KULLANILIYOR!
            dosya_kullanicilar = openpyxl.load_workbook(kullanicilar_excel_path)
            # dosya_basvurular, dosya_mentor, dosya4_mulakatlar zaten yorum satırındaydı.

            sayfa2 = dosya_kullanicilar.active

            adminler = [[cell.value.strip() if isinstance(cell.value, str) else cell.value for cell in row] for row in sayfa2.iter_rows() ]

            del adminler[0] # İlk satırı (başlıkları) sil

            found_user = False
            for i in adminler:
                if i[0] == kullaniciAdi and sifre == i[1]:
                    found_user = True
                    if i[2] == "admin":
                        self.tercihlerAdmin_lg.diger_sayfalar(self.basvuruform_lg,self.mentorform_lg,
                                                             self.mulakatlarform_lg,self.adminform_lg,self.tercihlerAdmin_lg) 
                        self.label_bilgilendirme.setText("You have logged in as an admin.")
                        QTimer.singleShot(1500, lambda: self.gecis_yap(self.tercihlerAdmin_lg))
                        break

                    else:     
                        self.tercihlerKullanici_lg.diger_sayfalar(self.basvuruform_lg,self.mulakatlarform_lg,
                                                                 self.mentorform_lg,self.tercihlerKullanici_lg)
                        self.label_bilgilendirme.setText("You have logged in as a user.")
                        QTimer.singleShot(1500, lambda: self.gecis_yap(self.tercihlerKullanici_lg))
                        break
            
            if not found_user: # Kullanıcı bulunamadıysa mesaj göster
                self.label_bilgilendirme.setText("Login failed. Please try again.")

        except Exception as e:
            # Genel bir hata oluştuğunda kullanıcıya bilgi ver
            QMessageBox.critical(self, "Hata", f"Giriş sırasında bir hata oluştu: {e}")
            self.label_bilgilendirme.setText("Giriş sırasında bir hata oluştu.")

    def gecis_yap(self,hedef_sayfa):
        hedef_sayfa.show()
        self.hide()
                
    def uygulama_kapatma(self):
        self.close()