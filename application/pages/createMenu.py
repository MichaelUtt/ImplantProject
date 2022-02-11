import os.path

from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget)
from . import (createReport, createImplant, createDoctor, createPart, viewAllReports, contactPage, createMaterial, \
              createAnesthetic, createPrescription)

class CreateMenuPage(QWidget):

    def __init__(self, parent):
        super(CreateMenuPage, self).__init__()
        uic.loadUi('ui/addMenu.ui', self)

        self.setWindowTitle("Add Menu")
        self.setWindowIcon(QIcon('data/favicon.ico'))
        self.parentWindow = parent

        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )

        # Display
        self.implantPage = createImplant.ImplantPage()
        self.implantPage.hide()
        self.partPage = createPart.PartPage()
        self.partPage.hide()
        self.doctorPage = createDoctor.DoctorPage()
        self.doctorPage.hide()
        self.materialPage = createMaterial.MaterialPage()
        self.materialPage.hide()
        self.anestheticPage = createAnesthetic.AnestheticPage()
        self.anestheticPage.hide()
        self.prescriptionPage = createPrescription.PrescriptionPage()
        self.prescriptionPage.hide()

        cornerLeft = 100
        cornerTop = 60
        self.setGeometry(cornerLeft, cornerTop, 650, 437)
        self.implantPage.setGeometry(cornerLeft, cornerTop, 650, 620)
        self.partPage.setGeometry(cornerLeft, cornerTop, 650, 620)

        self.show()

        # Buttons
        self.createImplantButton = self.findChild(QPushButton, "createImplant")
        self.createImplantButton.clicked.connect(self.createImplantPage)
        self.createRestorativePartButton = self.findChild(QPushButton, "createPart")
        self.createRestorativePartButton.clicked.connect(self.createRestorativePartPage)
        self.createDoctorButton = self.findChild(QPushButton, "createDoctor")
        self.createDoctorButton.clicked.connect(self.createDoctorPage)
        self.createMaterialButton = self.findChild(QPushButton, "createMaterial")
        self.createMaterialButton.clicked.connect(self.createMaterialPage)
        self.createAnestheticButton = self.findChild(QPushButton, "createAnesthetic")
        self.createAnestheticButton.clicked.connect(self.createAnestheticPage)
        self.createPrescriptionButton = self.findChild(QPushButton, "createPrescription")
        self.createPrescriptionButton.clicked.connect(self.createPrescriptionPage)

        self.backButton = self.findChild(QPushButton, "backButton")
        self.backButton.clicked.connect(self.closeAndOpenHome)


    def createImplantPage(self):
        if not self.implantPage.isVisible():
            self.implantPage.show()
        else:
            self.implantPage.hide()

    def createRestorativePartPage(self):
        if not self.partPage.isVisible():
            self.partPage.show()
        else:
            self.partPage.hide()

    def createDoctorPage(self):
        if not self.doctorPage.isVisible():
            self.doctorPage.show()
        else:
            self.doctorPage.hide()

    def createMaterialPage(self):
        if not self.materialPage.isVisible():
            self.materialPage.show()
        else:
            self.materialPage.hide()

    def createAnestheticPage(self):
        if not self.anestheticPage.isVisible():
            self.anestheticPage.show()
        else:
            self.anestheticPage.hide()

    def createPrescriptionPage(self):
        if not self.prescriptionPage.isVisible():
            self.prescriptionPage.show()
        else:
            self.prescriptionPage.hide()

    def closeAndOpenHome(self):
        self.parentWindow.show()
        self.close()

    def closeEvent(self, event):
        self.implantPage.close()
        self.partPage.close()
        self.doctorPage.close()
        self.materialPage.close()
        self.anestheticPage.close()
        self.prescriptionPage.close()

        self.parentWindow.show()
        event.accept()