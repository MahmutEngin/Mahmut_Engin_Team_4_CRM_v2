from PyQt6.QtWidgets import QMainWindow, QMessageBox # QMessageBox'u import ettiğinizden emin olun!
from PyQt6 import uic, QtWidgets
import os 
from backend.find_excel import get_excel_files_from_latest_vit
import openpyxl
import sys
from openpyxl import load_workbook

class MulakatlarPage(QMainWindow):
    
    def __init__(self):
        super().__init__()

        # UI ve Excel dosyaları için TEK VE TUTARLI BİR app_root_path tanımlaması yapıyoruz
        if getattr(sys, 'frozen', False):
            # PyInstaller ile paketlenmişse, _MEIPASS geçici dizinin yolunu verir
            self.app_root_path = sys._MEIPASS # self.app_root_path olarak kaydettik
        else:
            # Normal Python betiği olarak çalışıyorsa
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            self.app_root_path = os.path.abspath(os.path.join(current_script_dir, os.pardir)) # self.app_root_path olarak kaydettik

        # UI dosyasının tam yolunu oluştur
        ui_file_name = "mulakatlar_page_python.ui"
        ui_file_path = os.path.join(self.app_root_path, "ui", ui_file_name) # self.app_root_path kullandık

        # UI dosyasını yükle
        try:
            uic.loadUi(ui_file_path, self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"UI dosyası yüklenemedi: {ui_file_path}\nHata: {e}")
            sys.exit(1) # Hata durumunda uygulamayı kapat

        # Excel dosyasının yolu
        try:
            # get_excel_files_from_latest_vit fonksiyonuna doğru kök yolu iletin
            excel_files = get_excel_files_from_latest_vit(self.app_root_path) # self.app_root_path kullandık
            mulakatlar_path = excel_files.get("Mulakatlar")

            if not mulakatlar_path or not os.path.exists(mulakatlar_path):
                raise FileNotFoundError(f"Mulakatlar.xlsx dosyası bulunamadı. Lütfen dosyanın 'data' klasöründe olduğundan emin olun. Yol: {mulakatlar_path}")

            self.excel_path = mulakatlar_path 
            dosya_mulakatlar = openpyxl.load_workbook(mulakatlar_path)
            self.sayfa_mulakatlar = dosya_mulakatlar.active

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Excel dosyası yüklenemedi: {e}")
            self.excel_path = None # Hata durumunda excel_path'i None yap
            # return # Hata durumunda uygulamanın kapanmasını istiyorsanız burayı açın


        # ui öğelerine erişim (burayı UI'daki isimlendirmelerinize göre kontrol edin!)
        self.pushButton_ara = self.findChild(QtWidgets.QPushButton,"pushButton_ara")
        self.pushButton_projesiGonderilmisOlanlar = self.findChild(QtWidgets.QPushButton,"pushButton_projesiGonderilmisOlanlar")
        self.pushButton_ProjesiGelmisOlanlar = self.findChild(QtWidgets.QPushButton,"pushButton_ProjesiGelmisOlanlar")
        self.pushButton_tercihler = self.findChild(QtWidgets.QPushButton,"pushButton_tercihler")
        self.pushButton_exit = self.findChild(QtWidgets.QPushButton,"pushButton_exit")
        self.lineEdit_ara = self.findChild(QtWidgets.QLineEdit, "lineEdit_ara") # Arama butonu varsa lineEdit de olmalı
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget") # Tablo widget'ı da olmalı

        # olaylar
        self.pushButton_ara.clicked.connect(self.search)
        self.pushButton_projesiGonderilmisOlanlar.clicked.connect(self.projesi_gonderilmis_olanlar)
        self.pushButton_ProjesiGelmisOlanlar.clicked.connect(self.projesi_gelmis_olanlar)
        self.pushButton_tercihler.clicked.connect(self.tercihlerSayfasinaDon)
        self.pushButton_exit.clicked.connect(self.cikis_yap)

        # Önceki sayfa referansı (geri dönmek için)
        self.sayfa = None

    # fonksiyonlar
    def load_excel(self):
        # Bu fonksiyon artık __init__ içinde belirlenen self.excel_path'i kullanacak
        # Bu nedenle, burada ayrıca get_excel_files_from_latest_vit'i çağırmaya gerek yok.
        # Sadece self.excel_path'in varlığını ve geçerliliğini kontrol edin.
        if not self.excel_path or not os.path.exists(self.excel_path):
            QtWidgets.QMessageBox.warning(self, "Hata", "Mulakatlar.xlsx dosyası bulunamadı veya yolu geçersiz.")
            return [], []

        try:
            wb = load_workbook(self.excel_path)
            sheet = wb.active
            data = []
            headers = []
            for i, row in enumerate(sheet.iter_rows(values_only=True)):
                if i == 0:
                    headers = list(row)
                else:
                    data.append(list(row))
            return headers, data
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Hata", f"Excel dosyası okunamadı: {str(e)}")
            return [], []
        
    def display_data(self, headers, data):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                if item is None:
                    item = ""
                table_item = QtWidgets.QTableWidgetItem(str(item))
                self.tableWidget.setItem(row_idx, col_idx, table_item)
        self.tableWidget.resizeColumnsToContents()

    def search(self):
        search_text = self.lineEdit_ara.text().strip().lower()
        if not search_text:
            QtWidgets.QMessageBox.information(self, "Bilgi", "Lütfen arama metni giriniz.")
            return

        headers, data = self.load_excel() # <-- load_excel() doğru yolu kullanacak
        if not data:
            return

        filtered = []
        for row in data:
            # Her hücreyi kontrol et, ancak 'startswith' metodu ile
            if any(cell and str(cell).lower().startswith(search_text) for cell in row):
                filtered.append(row)

        if not filtered:
            QtWidgets.QMessageBox.information(self, "Sonuç", "Arama kriterlerine uygun kayıt bulunamadı.")
            self.tableWidget.clear()
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            return

        self.display_data(headers, filtered)
    
    def projesi_gonderilmis_olanlar(self):
        try:
            # self.app_root_path'i kullanarak dosyaları tekrar bulun
            excel_files = get_excel_files_from_latest_vit(self.app_root_path) # <-- BURAYI DÜZELTTİK!
            mulakatlar_path = excel_files.get("Mulakatlar")

            if not mulakatlar_path or not os.path.exists(mulakatlar_path):
                raise FileNotFoundError("Mulakatlar.xlsx dosyası bulunamadı veya yolu geçersiz.")

            wb = openpyxl.load_workbook(mulakatlar_path)
            sheet = wb.active

            # Başlıkları al
            headers = list(next(sheet.iter_rows(min_row=1, max_row=1, values_only=True)))
            data = [
                list(row)
                for row in sheet.iter_rows(min_row=2, values_only=True)
            ]

            # "Projesi Gönderilmiş" sütununun index'ini bul
            try:
                proje_gonderilmis_index = headers.index("Projesi Gönderilmiş")
            except ValueError:
                raise Exception("'Projesi Gönderilmiş' sütunu bulunamadı.")

            # "ok" olan satırları filtrele
            filtered = [
                row for row in data
                if row[proje_gonderilmis_index] and str(row[proje_gonderilmis_index]).strip().lower() == "ok"
            ]

            if not filtered:
                QtWidgets.QMessageBox.information(self, "Sonuç", "Projesi gönderilmiş aday bulunamadı.")
                self.tableWidget.clear()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(0)
                return

            # Tabloya veriyi yaz
            self.display_data(headers, filtered)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")

    def projesi_gelmis_olanlar(self):
        try:
            # self.app_root_path'i kullanarak dosyaları tekrar bulun
            excel_files = get_excel_files_from_latest_vit(self.app_root_path) # <-- BURAYI DÜZELTTİK!
            mulakatlar_path = excel_files.get("Mulakatlar")

            if not mulakatlar_path or not os.path.exists(mulakatlar_path):
                raise FileNotFoundError("Mulakatlar.xlsx dosyası bulunamadı veya yolu geçersiz.")

            wb = openpyxl.load_workbook(mulakatlar_path)
            sheet = wb.active

            # Başlıkları al
            headers = list(next(sheet.iter_rows(min_row=1, max_row=1, values_only=True)))
            data = [
                list(row)
                for row in sheet.iter_rows(min_row=2, values_only=True)
            ]

            # "Projesi Gönderilmiş" sütununun index'ini bul
            try:
                proje_gonderilmis_index = headers.index("Projesi Gönderilmiş")
            except ValueError:
                raise Exception("'Projesi Gönderilmiş' sütunu bulunamadı.")

            # "Projesi Gönderilmiş" sütunu boş olan satırları filtrele
            filtered = [
                row for row in data
                if not row[proje_gonderilmis_index] or str(row[proje_gonderilmis_index]).strip() == ""
            ]

            if not filtered:
                QtWidgets.QMessageBox.information(self, "Sonuç", "Projesi gelmiş aday bulunamadı.")
                self.tableWidget.clear()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(0)
                return

            # Tabloya veriyi yaz
            self.display_data(headers, filtered)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Veri yüklenemedi: {e}")

    def diger_sayfa(self,page):
        self.sayfa = page

    def tercihlerSayfasinaDon(self):
        if self.sayfa: # sayfa objesinin None olmadığından emin olun
            self.sayfa.show()
        self.hide()

    def cikis_yap(self):
        self.close()