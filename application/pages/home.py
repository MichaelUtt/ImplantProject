import os.path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMainWindow
from PyQt5 import uic

from . import createReport, createImplant, createDoctor, createPart, viewAllReports, contactPage


class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage, self).__init__()
        uic.loadUi('ui/home.ui', self)

        self.setWindowTitle('Implant Report Maker')
        self.setWindowIcon(QIcon('data/favicon.ico'))

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
        self.closeButton = self.findChild(QPushButton, "closeButton")
        self.closeButton.clicked.connect(self.closeApp)

        self.defaultFolderButton = self.findChild(QPushButton, "defaultFolderButton")
        self.defaultFolderButton.clicked.connect(self.setDefaultFolder)
        self.defaultExcelButton = self.findChild(QPushButton, "defaultExcelButton")
        self.defaultExcelButton.clicked.connect(self.setDefaultExcel)
        self.helpButton = self.findChild(QPushButton, "helpButton")
        self.helpButton.clicked.connect(self.getHelp)


        self.viewPage = viewAllReports.ViewPage()
        self.viewPage.hide()
        self.implantPage = createImplant.ImplantPage()
        self.implantPage.hide()
        self.partPage = createPart.PartPage()
        self.partPage.hide()
        self.doctorPage = createDoctor.DoctorPage()
        self.doctorPage.hide()
        self.helpPage = contactPage.HelpPage()
        self.helpPage.hide()

        cornerLeft = 100
        cornerTop = 60
        self.setGeometry(cornerLeft, cornerTop, 650, 600)
        self.viewPage.setGeometry(cornerLeft, cornerTop, 836, 450)
        self.implantPage.setGeometry(cornerLeft, cornerTop, 491, 545)
        self.partPage.setGeometry(cornerLeft, cornerTop, 491, 487)
        self.helpPage.setGeometry(cornerLeft, cornerTop, 600, 350)

        self.show()

    def closeApp(self):
        self.close()

    def createImplantPage(self):

        if not self.implantPage.isVisible():
            self.implantPage.show()
        else:
            self.implantPage.hide()


    def createReportPage(self):
        self.reportPage = createReport.CreateReportPage(self)
        #self.reportPage.closeEvent(self.closeReportPage)
        self.hide()

    def closeReportPage(self):
        self.show()

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

        with open("data/fileLocations.txt", "r") as content:
            lines = content.readlines()

        dir = lines[0][8:]
        if len(dir) > 3:
            try:
                file = str(QFileDialog.getExistingDirectory(self, "Select Directory", dir, QFileDialog.ShowDirsOnly))
            except:
                file = str(QFileDialog.getExistingDirectory(self, "Select Directory", QFileDialog.ShowDirsOnly))
        else:
            file = str(QFileDialog.getExistingDirectory(self, "Select Directory", QFileDialog.ShowDirsOnly))

        if len(file) < 2:
            return
        #print(file)

        with open("data/fileLocations.txt", "w") as content:
            content.write("reports="+file+"/\n")
            content.write(lines[1])
            content.write(lines[2])

    def setDefaultExcel(self):
        with open("data/fileLocations.txt", "r") as content:
            lines = content.readlines()

        path = lines[2][6:]
        if len(path) > 3:
            try:
                lastDir = os.path.dirname(path)
                file = QFileDialog.getOpenFileName(self, 'Open Excel', lastDir, "Microsoft Excel files (*.xlsx)")
            except:
                file = QFileDialog.getOpenFileName(self, 'Open Excel', "Microsoft Excel files (*.xlsx)")
        else:
            file = QFileDialog.getOpenFileName(self, 'Open Excel', "Microsoft Excel files (*.xlsx)")

        if len(file[0]) < 2:
            return
        # print(file)

        with open("data/fileLocations.txt", "w") as content:
            content.write(lines[0])
            content.write(lines[1])
            content.write("excel=" + file[0] + "\n")

    def getHelp(self):
        if not self.helpPage.isVisible():
            self.helpPage.show()
        else:
            self.helpPage.hide()

    def closeEvent(self, event):
        self.viewPage.close()
        self.implantPage.close()
        self.partPage.close()
        self.doctorPage.close()
        self.helpPage.close()

    def excelBackupCreate(self):
        pass

    def excelBackupCheck(self):
        pass