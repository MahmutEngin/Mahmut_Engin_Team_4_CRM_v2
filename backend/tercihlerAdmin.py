from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic, QtWidgets
import os 
import sys


class TercihlerAdminPage(QMainWindow):
    
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
        ui_file_name = "tercihlerAdmin_page_python.ui" # Veya yüklemek istediğiniz diğer .ui dosyası
        ui_file_path = os.path.join(base_path, "ui", ui_file_name)

        # print(f"UI dosya yolu: {ui_file_path}") # Debug için

        # UI dosyasını yükle
        uic.loadUi(ui_file_path, self)

        # # .ui dosyasını doğrudan yükle
        # ui_path = os.path.join(os.path.dirname(__file__), "..", "ui" ,'tercihlerAdmin_page_python.ui')
        # uic.loadUi(ui_path, self)


        self.basvuruform_ta = None
        self.mulakatlarform_ta = None
        self.mentorform_ta = None
        self.adminform_ta = None
        self.tercihlerAdmin_ta = None


        #ui ogelerine erisim 
        self.pushButton_adminMenu = self.findChild(QtWidgets.QPushButton,"pushButton_adminMenu")
        self.pushButton_basvurular = self.findChild(QtWidgets.QPushButton,"pushButton_basvurular")
        self.pushButton_anaMenu = self.findChild(QtWidgets.QPushButton,"pushButton_anaMenu")
        self.pushButton_exit = self.findChild(QtWidgets.QPushButton,"pushButton_exit")
        self.pushButton_mentorGorusmesi = self.findChild(QtWidgets.QPushButton,"pushButton_mentorGorusmesi")
        self.pushButton_mulakatlar = self.findChild(QtWidgets.QPushButton,"pushButton_mulakatlar")


        #olaylar
        self.pushButton_adminMenu.clicked.connect(self.adminMenu_fonk)
        self.pushButton_basvurular.clicked.connect(self.basvurular_fonk)
        self.pushButton_anaMenu.clicked.connect(self.anamenu_fonk)
        self.pushButton_exit.clicked.connect(self.kapatma_fonk)
        self.pushButton_mentorGorusmesi.clicked.connect(self.mentorGorusmesi_fonk)
        self.pushButton_mulakatlar.clicked.connect(self.mulakatlar_fonk)      


  #fonksiyonlar
        #gerekli sayfalarin aktarilmasi
    def diger_sayfalar(self,basvuruform,mentorform,mulakatlarform,adminform,tercihlerAdmin): 
        self.basvuruform_ta = basvuruform
        self.mulakatlarform_ta = mulakatlarform
        self.mentorform_ta = mentorform
        self.adminform_ta = adminform
        self.tercihlerAdmin_ta = tercihlerAdmin

    def basvurular_fonk(self):
        self.hide()
        self.basvuruform_ta.diger_sayfa(self.tercihlerAdmin_ta) # sayfanin gonderilmesi
        self.basvuruform_ta.show()

    def mentorGorusmesi_fonk(self):
        self.hide()
        self.mentorform_ta.diger_sayfa(self.tercihlerAdmin_ta)
        self.mentorform_ta.show()

    def mulakatlar_fonk(self):
        self.hide()
        self.mulakatlarform_ta.diger_sayfa(self.tercihlerAdmin_ta)
        self.mulakatlarform_ta.show()

    def adminMenu_fonk(self):
        self.hide()
        self.adminform_ta.diger_sayfa(self.tercihlerAdmin_ta)
        self.adminform_ta.show()


    def anamenu_fonk(self):  # burasi kaldi
        pass
    
    def kapatma_fonk(self):
        self.close()


        
