import os.path
import sys

import psutil
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMainWindow, QMessageBox
from PyQt5 import uic

from . import createReport, createImplant, createDoctor, createPart, viewAllReports, contactPage, createMenu


class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage, self).__init__()
        uic.loadUi('ui/home.ui', self)

        self.setWindowTitle('Implant Report Maker')
        self.setWindowIcon(QIcon('data/favicon.ico'))

        self.createReportButton = self.findChild(QPushButton, "createReport")
        self.createReportButton.clicked.connect(self.createReportPage)

        # self.createImplantButton = self.findChild(QPushButton, "createImplant")
        # self.createImplantButton.clicked.connect(self.createImplantPage)
        # self.createRestorativePartButton = self.findChild(QPushButton, "createRestorativePart")
        # self.createRestorativePartButton.clicked.connect(self.createRestorativePartPage)
        # self.createDoctorButton = self.findChild(QPushButton, "createDoctor")
        # self.createDoctorButton.clicked.connect(self.createDoctorPage)
        self.addMenuButton = self.findChild(QPushButton, "addMenu")
        self.addMenuButton.clicked.connect(self.createMenuPage)

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

        # self.viewPage = viewAllReports.ViewPage()
        # self.viewPage.hide()
        self.helpPage = contactPage.HelpPage()
        self.helpPage.hide()

        cornerLeft = 100
        cornerTop = 60
        self.setGeometry(cornerLeft, cornerTop, 650, 600)

        self.show()

        self.isFrozen = False
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.isFrozen = True
        else:
            self.isFrozen = False
            print('running in a normal Python process')

    def closeApp(self):
        self.close()

    def createReportPage(self):
        self.reportPage = createReport.CreateReportPage(self)
        self.hide()

    def createMenuPage(self):
        self.addMenuPage = createMenu.CreateMenuPage(self)
        self.hide()

    def viewReportsPage(self):
        if "EXCEL.EXE" in (p.name() for p in psutil.process_iter()):
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Error")
            error_dialog.setText('The Excel File is already open. Cannot open file. ')
            error_dialog.exec_()
            return
        else:
            with open("data/fileLocations.txt", "r") as content:
                lines = content.readlines()
            excelFile = lines[2][6:].strip()
            if len(excelFile) < 3:
                error_dialog = QMessageBox()
                error_dialog.setWindowTitle("Select File")
                error_dialog.setText("Select an Excel File. ")
                error_dialog.exec_()
                self.setDefaultExcel()
                with open("data/fileLocations.txt", "r") as content:
                    lines = content.readlines()
                excelFile = lines[2][6:].strip()
            os.startfile(excelFile)
        # if not self.viewPage.isVisible():
        #     self.viewPage.show()
        #     self.viewPage.generateTable()
        # else:
        #     self.viewPage.hide()

    def setDefaultFolder(self):

        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\fileLocations.txt')
        #print(path_to_dat)
        with open(path_to_dat, "r") as content:
            lines = content.readlines()

        dir = lines[0][8:]
        if len(dir) > 3:
            try:
                file = str(QFileDialog.getExistingDirectory(self, "Select Directory", dir, QFileDialog.ShowDirsOnly))
            except:
                file = str(QFileDialog.getExistingDirectory(self, "Select Directory", options=QFileDialog.ShowDirsOnly))
        else:
            file = str(QFileDialog.getExistingDirectory(self, "Select Directory", options=QFileDialog.ShowDirsOnly))

        if len(file) < 2:
            return
        #print(file)

        with open(path_to_dat, "w") as content:
            content.write("reports="+file+"/\n")
            content.write(lines[1])
            content.write(lines[2])

    def setDefaultExcel(self):

        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\fileLocations.txt')
        # print(path_to_dat)
        with open(path_to_dat, "r") as content:
            lines = content.readlines()

        path = lines[2][6:]
        if len(path) > 3:
            try:
                lastDir = os.path.dirname(path)
                file = QFileDialog.getOpenFileName(self, 'Open Excel', lastDir, "Microsoft Excel files (*.xlsx)")
            except:
                file = QFileDialog.getOpenFileName(self, 'Open Excel', filter="Microsoft Excel files (*.xlsx)")
        else:
            file = QFileDialog.getOpenFileName(self, 'Open Excel', filter="Microsoft Excel files (*.xlsx)")


        if len(file[0]) < 2:
            return
        # print(file)

        with open(path_to_dat, "w") as content:
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
        self.helpPage.close()
        event.accept()

    def excelBackupCreate(self):
        pass

    def excelBackupCheck(self):
        pass