from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QMouseEvent, QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QInputDialog, QMessageBox, QDateEdit, QFileDialog, QScrollArea,
                             QMainWindow, QTreeView)
from PyQt5.Qt import QStandardItemModel, QStandardItem
from application.pages import home
from mailmerge import MailMerge
from PyQt5 import uic
import json


allDoctors = ["David Engen", "Add new Doctor"]
allImplants = ["Select Implant", "Implant 1", "Implant 2"]
allAnesthetics = ["None", "New Anesthetic", "Anesthetic 1"]
allPrescriptions = ["None", "New Prescription", "Prescription 1"]


class CreateReportPage(QMainWindow):
    def __init__(self):
        super(CreateReportPage, self).__init__()
        uic.loadUi('ui/createImplant.ui', self)

        self.patientName = self.findChild(QLineEdit, 'patientName')
        self.chartNumber = self.findChild(QLineEdit, 'chartNumber')
        self.doctor = self.findChild(QComboBox, 'doctor')

        self.date = self.findChild(QDateEdit, 'date')
        self.uncoverDate = self.findChild(QDateEdit, 'uncoverDate')
        self.singleStage = self.findChild(QCheckBox, 'singleStage')
        self.restoreDate = self.findChild(QDateEdit, 'restoreDate')

        self.setDateDefaults()
        self.singleStage.clicked.connect(self.singleStagePressed)

        self.implantTree = self.findChild(QTreeView, 'implantList')
        self.makeImplantTree()

        self.restorativePartsList = self.findChild(QVBoxLayout, 'restorativePartsList')
        self.fillRestorativeParts()


        self.show()


    def singleStagePressed(self):
        if self.singleStage.isChecked():
            self.uncoverDate.setEnabled(False)
        else:
            self.uncoverDate.setEnabled(True)

    def setDateDefaults(self):
        self.date.setDate(QDate.currentDate())
        self.uncoverDate.setDate(QDate.currentDate().addMonths(6))
        self.restoreDate.setDate(QDate.currentDate().addMonths(7))

    def makeImplantTree(self):

        with open("data/implants.json", "r") as content:
            implants = json.load(content)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        for root, child in implants.items():
            #print(root)
            outer = QStandardItem(root)
            #print(child)
            try:
                for root2, grandchild in child.items():
                    inner = QStandardItem(root2)

                    for gc in grandchild:
                        leaf = QStandardItem(gc)
                        inner.appendRow(leaf)
                    outer.appendRow(inner)

                    #print("\t"+str(root2))
                    #print("\t"+str(grandchild))
            except AttributeError:
                for c in child:
                    leaf = QStandardItem(c)
                    outer.appendRow(leaf)
            rootNode.appendRow(outer)

        self.implantTree.setModel(treeModel)
        self.implantTree.expandAll()
        self.implantTree.setHeaderHidden(True)


    def fillRestorativeParts(self):

        def toggleRestorativeParts():
            partCount = self.restorativePartsList.count()
            cb = self.restorativePartsList.itemAt(0).widget()

            for i in range(1, partCount):
                if cb.isChecked():
                    self.restorativePartsList.itemAt(i).widget().setEnabled(False)
                else:
                    self.restorativePartsList.itemAt(i).widget().setEnabled(True)

        f = open("data/restorativeParts.txt", "r")

        noPartsOption = QCheckBox("No restorative parts to order.  We will scan the implant digitally.  \n"
                                  "You can choose from one of our partner Digital Implant Solutions labs \n"
                                  "to will make the models, custom abutment, and the restoration all \n"
                                  "according to your instructions.  You can communicate with your lab directly\n")
        noPartsOption.setChecked(True)
        noPartsOption.toggled.connect(toggleRestorativeParts)
        self.restorativePartsList.addWidget(noPartsOption)
        print(noPartsOption)

        for line in f:
            if line[0] == "&":
                myFont = QFont()
                myFont.setBold(True)

                category = QLabel()
                category.setText("\n"+line[1:-1])
                category.setFont(myFont)

                self.restorativePartsList.addWidget(category)

            else:
                if len(line) > 3:

                    option = QCheckBox()
                    option.setText(line[0:-1])
                    self.restorativePartsList.addWidget(option)
        toggleRestorativeParts()




