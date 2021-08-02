import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from application.pages import createReport

resolution = (800, 900)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = createReport.CreateReportPage()
    sys.exit(app.exec_())



