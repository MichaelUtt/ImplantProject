import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from application.pages import createReport, home, createImplant

resolution = (800, 900)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = home.HomePage()
    #gallery = createImplant.ImplantPage()
    sys.exit(app.exec_())



