from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QMouseEvent, QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QInputDialog, QMessageBox, QDateEdit, QFileDialog, QScrollArea,
                             QMainWindow, QTreeView)
from PyQt5.Qt import QStandardItemModel, QStandardItem
from mailmerge import MailMerge
from PyQt5 import uic
import json

from application.pages import createReport, createImplant, createDoctor, createPart, viewAllReports

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage, self).__init__()
        uic.loadUi('ui/home.ui', self)

        self.setWindowTitle('Implant Report Maker')
        self.setWindowIcon(QIcon('data/favicon.ico'))

        # TODO maybe
        #self.findChild(QPushButton, "viewReports").setHidden(True)

        self.createReportButton = self.findChild(QPushButton, "createReport")
        self.createReportButton.clicked.connect(self.createReportPage)

        self.createImplantButton = self.findChild(QPushButton, "createImplant")
        self.createImplantButton.clicked.connect(self.createImplantPage)
        self.createRestorativePartButton = self.findChild(QPushButton, "createRestorativePart")
        self.createRestorativePartButton.clicked.connect(self.createRestorativePartPage)

        self.createDoctorButton = self.findChild(QPushButton, "createDoctor")
        self.createDoctorButton.clicked.connect(self.createDoctorPage)
        self.viewReportsButton = self.findChild(QPushButton, "viewReports")
        self.viewReportsButton.clicked.connect(self.viewReportsPage)
        self.defaultFolderButton = self.findChild(QPushButton, "defaultFolderButton")
        self.defaultFolderButton.clicked.connect(self.setDefaultFolder)
        self.closeButton = self.findChild(QPushButton, "closeButton")
        self.closeButton.clicked.connect(self.closeApp)

        self.viewPage = viewAllReports.ViewPage()
        self.viewPage.hide()
        self.implantPage = createImplant.ImplantPage()
        self.implantPage.hide()
        self.partPage = createPart.PartPage()
        self.partPage.hide()
        self.doctorPage = createDoctor.DoctorPage()
        self.doctorPage.hide()


        self.show()

    def closeApp(self):
        self.close()

    def createImplantPage(self):

        if not self.implantPage.isVisible():
            self.implantPage.show()
        else:
            self.implantPage.hide()


    def createReportPage(self):
        self.reportPage = createReport.CreateReportPage()
        self.hide()

    def createRestorativePartPage(self, val):
        if not self.partPage.isVisible():
            self.partPage.show()
        else:
            self.partPage.hide()

    def createDoctorPage(self,val):
        if not self.doctorPage.isVisible():
            self.doctorPage.show()
        else:
            self.doctorPage.hide()

    def viewReportsPage(self):
        if not self.viewPage.isVisible():
            self.viewPage.show()
            self.viewPage.generateTable()
        else:
            self.viewPage.hide()

    def setDefaultFolder(self):
        pass
