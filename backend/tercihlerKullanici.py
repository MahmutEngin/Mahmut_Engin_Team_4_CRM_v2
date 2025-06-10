from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic, QtWidgets
import os 
import sys

class TercihlerKullaniciPage(QMainWindow):
    
    def __init__(self):
        super().__init__()


        # Uygulamanın PyInstaller ile mi yoksa normal Python ile mi çalıştığını kontrol et
        if getattr(sys, 'frozen', False):
            # PyInstaller ile paketlenmişse, _MEIPASS geçici dizinin yolunu verir
            base_path = sys._MEIPASS
        else:
            # Normal Python betiği olarak çalışıyorsa, betiğin bulunduğu dizini kullan
            # os.path.dirname(os.path.abspath(__file__)) size geçerli betiğin dizinini verir.
            # Eğer main.py içindeyseniz ve ui klasörü main.py'nin bir üst dizinindeyse,
            # bu path'i uygun şekilde ayarlamanız gerekebilir.
            # Ancak PyInstaller'a "ui;ui" dediğimiz için, paketlendikten sonra ui klasörü base_path içinde olacak.
            base_path = os.path.dirname(os.path.abspath(__file__))
            # Eğer main.py backend'de ve ui klasörü C:\'de ise, normal çalışırken bir üst dizine gitmeniz gerekir.
            # Bunu test etmeniz önemlidir. Örneğin:
            # base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
            # print(f"Normal çalışma base_path: {base_path}") # Debug için

        # UI dosyasının tam yolunu oluştur
        # PyInstaller'a "--add-data 'ui;ui'" dediğimiz için,
        # 'ui' klasörü exe'nin çıkarıldığı geçici dizinin doğrudan içinde yer alacaktır.
        # Bu yüzden '../ui/' gibi göreli yollara gerek kalmaz.
        ui_file_name = "tercihlerKullanici_page_python.ui" # Veya yüklemek istediğiniz diğer .ui dosyası
        ui_file_path = os.path.join(base_path, "ui", ui_file_name)

        # print(f"UI dosya yolu: {ui_file_path}") # Debug için

        # UI dosyasını yükle
        uic.loadUi(ui_file_path, self)

        # # .ui dosyasını doğrudan yükle
        # ui_path = os.path.join(os.path.dirname(__file__), "..", "ui" ,'tercihlerKullanici_page_python.ui')
        # uic.loadUi(ui_path, self)


        self.basvuruform_tk = None
        self.mulakatlarform_tk = None
        self.mentorform_tk = None
        self.tercihlerKullanici_tk = None


        #ui ogelerine erisim 
        self.pushButton_basvurular = self.findChild(QtWidgets.QPushButton,"pushButton_basvurular")
        self.pushButton_anaMenu = self.findChild(QtWidgets.QPushButton,"pushButton_anaMenu")
        self.pushButton_exit = self.findChild(QtWidgets.QPushButton,"pushButton_exit")
        self.pushButton_mentorGorusmesi = self.findChild(QtWidgets.QPushButton,"pushButton_mentorGorusmesi")
        self.pushButton_mulakatlar = self.findChild(QtWidgets.QPushButton,"pushButton_mulakatlar")


        #olaylar
        self.pushButton_basvurular.clicked.connect(self.basvuru_fonk)
        self.pushButton_anaMenu.clicked.connect(self.anamenu_fonk)
        self.pushButton_exit.clicked.connect(self.kapatma_fonk)
        self.pushButton_mentorGorusmesi.clicked.connect(self.mentorGorusmesi_fonk)
        self.pushButton_mulakatlar.clicked.connect(self.mulakatlar_fonk)       



    #fonksiyonlar
    def diger_sayfalar(self,basvuruform,mulakatlarform,mentorform,tercihlerKullanici):
        self.basvuruform_tk = basvuruform
        self.mulakatlarform_tk = mulakatlarform
        self.mentorform_tk = mentorform
        self.tercihlerKullanici_tk = tercihlerKullanici

    def basvuru_fonk(self):
        self.hide()
        self.basvuruform_tk.diger_sayfa(self.tercihlerKullanici_tk)
        self.basvuruform_tk.show()

    def mentorGorusmesi_fonk(self):
        self.hide()
        self.mentorform_tk.diger_sayfa(self.tercihlerKullanici_tk)
        self.mentorform_tk.show()

    def mulakatlar_fonk(self):
        self.hide()
        self.mulakatlarform_tk.diger_sayfa(self.tercihlerKullanici_tk)
        self.mulakatlarform_tk.show()

    def anamenu_fonk(self):
        self.hide()
        pass
    
    def kapatma_fonk(self):
        self.close()




