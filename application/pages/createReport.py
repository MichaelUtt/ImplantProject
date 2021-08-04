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

        for doctorIndex in [1,2,3]:
            self.findChild(QRadioButton, "doctor"+str(doctorIndex)).clicked.connect(self.doctorChanged)

        self.doctor = "David W. Engen, DDS, MSD"

        self.date = self.findChild(QDateEdit, 'date')
        self.uncoverDate = self.findChild(QDateEdit, 'uncoverDate')
        self.singleStage = self.findChild(QCheckBox, 'singleStage')
        self.restoreDate = self.findChild(QDateEdit, 'restoreDate')

        self.singleStage.clicked.connect(self.singleStagePressed)


        self.firstImplant = NewImplantForm()
        self.implantLayout = self.findChild(QVBoxLayout, "implantLayout")
        self.implantLayout.addWidget(self.firstImplant)

        self.implantCount = 1

        self.depthBox = self.findChild(QGroupBox, 'depthBox')

        self.healingCapBox = self.findChild(QGroupBox, 'healingCapBox')
        self.healingCapEdit = self.findChild(QLineEdit, 'healingCapEdit')

        self.graftBox = self.findChild(QGroupBox, 'graftBox')
        self.implantRestoreBox = self.findChild(QGroupBox, 'implantRestoreBox')

        self.anestheticBox = self.findChild(QGroupBox, 'anestheticBox')
        self.toleranceBox = self.findChild(QGroupBox, 'toleranceBox')
        self.prescriptionsBox = self.findChild(QGroupBox, 'prescriptionsBox')

        self.xrayButton = self.findChild(QPushButton, 'addXray')
        self.xrayButton.clicked.connect(self.getXrayPath)

        self.addImplantButtonYes = self.findChild(QPushButton, 'addImplantYes')
        self.addImplantButtonYes.clicked.connect(self.addImplantTab)
        self.addImplantButtonNo = self.findChild(QPushButton, 'addImplantNo')
        # self.addImplantButtonNo.clicked.connect(self.something)

        self.tabWidget = self.findChild(QTabWidget, "createPages")

        # self.newImplantWidget = NewImplantForm()
        # print(self.newImplantWidget)
        # self.tabWidget.addTab(self.newImplantWidget, "Tab2")


        self.setDateDefaults()
        self.uncoverDate.dateChanged.connect(self.dateChanged)
        self.restoreDate.dateChanged.connect(self.dateChanged)
        self.dateChanged()
        self.tabWidget.setTabText(0,self.getTabName(self.implantCount))
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

    def dateChanged(self):

        options = self.implantRestoreBox.findChildren(QLabel)

        for opt in options:
            txt = opt.text()
            txt = txt.replace("<Implant restore date>", self.restoreDate.text())
            txt = txt.replace("<implant uncovery date>", self.uncoverDate.text())

            opt.setText(txt)

    def getXrayPath(self):
        fname = QFileDialog.getOpenFileName(self, 'Open X-Ray',
                                            '', "Image files (*.jpg *.jpeg *.png)")

        self.findChild(QLabel, 'xrayPath').setText("File Path: "+fname[0])



    def addImplantTab(self):
        self.implantCount += 1
        newImplantWidget = NewImplantForm()
        self.tabWidget.addTab(newImplantWidget, self.getTabName(self.implantCount))

        self.tabWidget.setCurrentIndex(self.implantCount-1)
        self.findChild(QScrollArea, 'mainScroll').verticalScrollBar().setValue(0)

    def doctorChanged(self):
        for doctorIndex in [1, 2, 3]:
            doc = self.findChild(QRadioButton, "doctor" + str(doctorIndex))
            if doc.isChecked():
                self.doctor = doc.text()

        for i in range(self.tabWidget.count()):
            print(i)
            self.tabWidget.setTabText(i,self.getTabName(i+1))


    def getTabName(self, pageNum):
        return (self.doctor.split()[0]+"-Implant-"+str(pageNum)+"-"+self.date.text())



class NewImplantForm(QWidget):
    def __init__(self):
        super(NewImplantForm, self).__init__()
        uic.loadUi('ui/newImplantForm.ui', self)

        self.implantTree = self.findChild(QTreeView, 'implantList')
        self.makeImplantTree()
        self.implantTree.clicked.connect(self.implantChanged)

        self.toothNumber = self.findChild(QLineEdit, 'toothNumber')
        self.lotNumber = self.findChild(QLineEdit, 'lotNumber')
        self.expirationDate = self.findChild(QDateEdit, 'expirationDate')

        self.restorativePartsList = self.findChild(QVBoxLayout, 'restorativePartsList')
        self.fillRestorativeParts()

        self.incisionBox = self.findChild(QGroupBox, 'incisionBox')
        self.incisionEdit1 = self.findChild(QLineEdit, 'incisionEdit1')
        self.incisionEdit2 = self.findChild(QLineEdit, 'incisionEdit2')
        self.incisionEdit1.textEdited.connect(self.incisionChanging)
        self.incisionEdit2.textEdited.connect(self.incisionChanging)
        self.incisionEdit1.editingFinished.connect(self.incisionChanged)
        self.incisionEdit2.editingFinished.connect(self.incisionChanged)

        self.flapBox = self.findChild(QGroupBox, 'flapBox')
        self.extractionBox = self.findChild(QGroupBox, 'extractionBox')
        self.extractionEdit = self.findChild(QLineEdit, 'extractionEdit')
        self.extractionEdit.textEdited.connect(self.extractionChanging)
        self.extractionEdit.editingFinished.connect(self.extractionChanged)

        self.osteotomyBox = self.findChild(QGroupBox, 'osteotomyBox')
        self.osteotomyEdit1 = self.findChild(QLineEdit, 'osteotomyEdit1')
        self.osteotomyEdit2 = self.findChild(QLineEdit, 'osteotomyEdit2')
        self.osteotomyEdit1.textEdited.connect(self.osteotomyChanging)
        self.osteotomyEdit2.textEdited.connect(self.osteotomyChanging)
        self.osteotomyEdit1.editingFinished.connect(self.osteotomyChanged)
        self.osteotomyEdit2.editingFinished.connect(self.osteotomyChanged)

        self.boneDensityBox = self.findChild(QGroupBox, 'boneDensityBox')
        self.perforationsBox = self.findChild(QGroupBox, 'perforationsBox')
        self.tappedBox = self.findChild(QGroupBox, 'tappedBox')
        self.sinusBox = self.findChild(QGroupBox, 'sinusBox')
        self.implantSeatedBox = self.findChild(QGroupBox, 'implantSeatedBox')




    def makeImplantTree(self):

        with open("data/implants.json", "r") as content:
            implants = json.load(content)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        for root, child in implants.items():
            # print(root)
            outer = QStandardItem(root)
            # print(child)
            try:
                for root2, grandchild in child.items():
                    inner = QStandardItem(root2)

                    for gc in grandchild:
                        leaf = QStandardItem(gc)
                        inner.appendRow(leaf)
                    outer.appendRow(inner)

                    # print("\t"+str(root2))
                    # print("\t"+str(grandchild))
            except AttributeError:
                for c in child:
                    leaf = QStandardItem(c)
                    outer.appendRow(leaf)
            rootNode.appendRow(outer)

        self.implantTree.setModel(treeModel)
        self.implantTree.expandAll()
        self.implantTree.setHeaderHidden(True)

    def implantChanged(self, index):
        selectedItem = self.implantTree.model().itemFromIndex(index)
        self.implant = selectedItem.text()

        self.implantSeatedBox.setTitle("A " + self.implant + " implant was seated to depth.")

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
        # print(noPartsOption)

        for line in f:
            if line[0] == "&":
                myFont = QFont()
                myFont.setBold(True)

                category = QLabel()
                category.setText("\n" + line[1:-1])
                category.setFont(myFont)

                self.restorativePartsList.addWidget(category)

            else:
                if len(line) > 3:
                    option = QCheckBox()
                    option.setText(line[0:-1])
                    self.restorativePartsList.addWidget(option)
        toggleRestorativeParts()

    def incisionChanging(self):

        if self.incisionBox.findChild(QLabel, 'helpMessage') == None:
            helpMessage = QLabel("Separate multiple teeth with commas.")
            helpMessage.setStyleSheet("color: red")
            helpMessage.setObjectName("helpMessage")

            self.incisionBox.layout().addWidget(helpMessage, 5, 3)

    def incisionChanged(self):
        helpMessage = self.incisionBox.findChild(QLabel, 'helpMessage')
        if helpMessage != None:
            self.incisionBox.layout().removeWidget(helpMessage)
            helpMessage.destroy()

    def extractionChanging(self):
        if self.extractionBox.findChild(QLabel, 'helpMessage') == None:
            helpMessage = QLabel("Separate multiple teeth with commas.")
            helpMessage.setStyleSheet("color: red")
            helpMessage.setObjectName("helpMessage")

            self.extractionBox.layout().addWidget(helpMessage, 2, 3)

    def extractionChanged(self):
        helpMessage = self.extractionBox.findChild(QLabel, 'helpMessage')
        if helpMessage != None:
            self.extractionBox.layout().removeWidget(helpMessage)
            helpMessage.destroy()

    def osteotomyChanging(self):
        if self.osteotomyBox.findChild(QLabel, 'helpMessage') == None:
            helpMessage = QLabel("Separate multiple teeth with commas.")
            helpMessage.setStyleSheet("color: red")
            helpMessage.setObjectName("helpMessage")

            self.osteotomyBox.layout().addWidget(helpMessage, 7, 0)

    def osteotomyChanged(self):
        helpMessage = self.osteotomyBox.findChild(QLabel, 'helpMessage')
        if helpMessage != None:
            self.osteotomyBox.layout().removeWidget(helpMessage)
            helpMessage.destroy()
