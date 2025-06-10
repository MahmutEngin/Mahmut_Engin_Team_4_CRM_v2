import sys 
from PyQt6 import QtWidgets 

from backend.login import LoginPage
from backend.mentor import MentorPage
from backend.mulakatlar import MulakatlarPage
from backend.basvurular import BasvurularPage
from backend.admin import AdminPage
from backend.tercihlerAdmin import TercihlerAdminPage
from backend.tercihlerKullanici import TercihlerKullaniciPage


app = QtWidgets.QApplication(sys.argv)

#tum sayfalarin olusturulmasi
degisken_basvuruform = BasvurularPage()
degisken_mulakatlarform = MulakatlarPage()
degisken_mentorform = MentorPage()
degisken_adminform = AdminPage()
degisken_tercihlerKullanici = TercihlerKullaniciPage()
degisken_tercihlerAdmin = TercihlerAdminPage()


pencere = LoginPage()
#sayfalarin ihtiyac duydugu sayfa objelerinin gonderilmesi
pencere.diger_sayfalar(degisken_basvuruform,degisken_mulakatlarform,degisken_mentorform,
                       degisken_adminform,degisken_tercihlerKullanici,degisken_tercihlerAdmin)

pencere.show()
sys.exit(app.exec())
