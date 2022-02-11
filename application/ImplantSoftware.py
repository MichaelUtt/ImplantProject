# pyinstaller ImplantSoftware.spec

import sys

from PyQt5.QtWidgets import QApplication

from pages import home

resolution = (800, 900)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = home.HomePage()
    #gallery = createImplant.ImplantPage()
    sys.exit(app.exec_())



