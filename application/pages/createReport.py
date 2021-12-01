import os

from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QMouseEvent, QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QInputDialog, QMessageBox, QDateEdit, QFileDialog, QScrollArea,
                             QMainWindow, QTreeView, QButtonGroup)
from PyQt5.Qt import QStandardItemModel, QStandardItem
from application.pages import home
from mailmerge import MailMerge
from docx import Document
from docx.shared import Inches
from PyQt5 import uic
import json


class CreateReportPage(QMainWindow):
    def __init__(self):
        super(CreateReportPage, self).__init__()
        uic.loadUi('ui/createImplant.ui', self)

        self.setWindowTitle('Create Report')
        self.setWindowIcon(QIcon('data/favicon.ico'))

        self.patientName = self.findChild(QLineEdit, 'patientName')
        self.chartNumber = self.findChild(QLineEdit, 'chartNumber')

        #for doctorIndex in [1,2,3]:
        #    self.findChild(QRadioButton, "doctor"+str(doctorIndex)).clicked.connect(self.doctorChanged)
        self.doctorBox = self.findChild(QVBoxLayout, "doctorBox")
        #print(self.doctorBox)

        #self.doctorBox.setExclusive(True)
        self.createDoctors()

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


        self.implantRestoreBox = self.findChild(QGroupBox, 'implantRestoreBox')

        self.anestheticBox = self.findChild(QGroupBox, 'anestheticBox')
        self.toleranceBox = self.findChild(QGroupBox, 'toleranceBox')
        self.prescriptionsBox = self.findChild(QGroupBox, 'prescriptionsBox')

        self.xrayButton = self.findChild(QPushButton, 'addXray')
        self.xrayButton.clicked.connect(self.getXrayPath)
        self.xrayPath = 'data/noImage.jpg'

        self.addImplantButtonYes = self.findChild(QPushButton, 'addImplantYes')
        self.addImplantButtonYes.clicked.connect(self.addImplantTab)
        self.addImplantButtonNo = self.findChild(QPushButton, 'addImplantNo')
        # self.addImplantButtonNo.clicked.connect(self.something)

        self.tabWidget = self.findChild(QTabWidget, "createPages")

        # self.newImplantWidget = NewImplantForm()
        # print(self.newImplantWidget)
        # self.tabWidget.addTab(self.newImplantWidget, "Tab2")
        self.printSurgeryReportButton = self.findChild(QPushButton, "printSurgeryReport")
        self.printSurgeryReportButton.clicked.connect(self.printSurgeryReportPressed)

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
        with open("data/fileLocations.txt", "r") as content:
            lines = content.readlines()

        lastDir = " "
        if len(lines[1]) > 6:
            lastDir = lines[1][6:]
        # print(lastDir)

        fname = QFileDialog.getOpenFileName(self, 'Open X-Ray',
                                            lastDir, "Image files (*.jpg *.jpeg)")
        if len(fname[0]) < 2:
            return
        self.xrayPath = fname[0]
        self.findChild(QLabel, 'xrayPath').setText("File Path: "+fname[0])

        with open("data/fileLocations.txt", "w") as content:
            content.write(lines[0])
            content.write("xrays="+os.path.dirname(fname[0]))



    def addImplantTab(self):
        self.implantCount += 1
        newImplantWidget = NewImplantForm()
        self.tabWidget.addTab(newImplantWidget, self.getTabName(self.implantCount))

        self.tabWidget.setCurrentIndex(self.implantCount-1)
        self.findChild(QScrollArea, 'mainScroll').verticalScrollBar().setValue(0)

    def createDoctors(self):

        with open("data/doctors.txt", "r") as content:
            lines = content.readlines()
            docs = []
            for line in lines:
                if len(line) > 3:
                    docs.append(line)

            self.docCount = len(docs)

            docGroup = QGroupBox()
            docLayout = QVBoxLayout()
            i = 0
            for doc in docs:
                d = QRadioButton(doc.replace("\n", ""))
                if i == 0:
                    d.setChecked(True)
                d.setObjectName("doctor" + str(i))
                d.clicked.connect(self.doctorChanged)
                docLayout.addWidget(d)
                i += 1
            docGroup.setLayout(docLayout)
            self.doctorBox.addWidget(docGroup)




    def doctorChanged(self):
        for doctorIndex in range(self.docCount):
            doc = self.findChild(QRadioButton, "doctor" + str(doctorIndex))
            if doc.isChecked():
                self.doctor = doc.text()

        for i in range(self.tabWidget.count()):

            self.tabWidget.setTabText(i,self.getTabName(i+1))


    def getTabName(self, pageNum):
        return (self.doctor.split()[0]+"_Implant_"+str(pageNum))

    def getRestore(self):
        options = self.implantRestoreBox.findChildren(QRadioButton)
        for opt in options:
            if opt.isChecked():
                val = opt.objectName()[-1]
                txt = self.implantRestoreBox.findChild(QLabel, ("restoreOpt"+str(val))).text()
                return txt
        return ""

    def getAnesthetic(self):
        options = self.anestheticBox.findChildren(QRadioButton)
        for opt in options:
            if opt.isChecked():
                return opt.text()
        return "N/A"

    def getTolerance(self):
        options = self.toleranceBox.findChildren(QRadioButton)
        for opt in options:
            if opt.isChecked():
                return opt.text()
        return "N/A"

    def getRX(self):
        options = self.prescriptionsBox.findChildren(QCheckBox)
        txt = ""
        for opt in options:
            if opt.isChecked():
                txt += (opt.text()+"\n")
        if txt == "":
            return "N/A"
        else:
            return txt

    def printSurgeryReportPressed(self):
        print(self.firstImplant.generateParagraph())
        print(self.firstImplant.getRestorativeParts())
        implants = ""
        reports = ""
        parts = ""
        for tab in self.tabWidget.findChildren(NewImplantForm):
            implants += (tab.getImplant()+"\n")
            reports += (tab.generateParagraph()+"\n\n")
            parts += (tab.getRestorativeParts()+"\n\n")

        restoreChoice = self.getRestore()
        anestheticChoice = self.getAnesthetic()
        toleranceChoice = self.getTolerance()
        rxChoice = self.getRX()

        if self.singleStage.isChecked():
            uncoverVal = "Single Stage"
        else:
            uncoverVal = self.date.text()
        template = "data/template.docx"

        document = MailMerge(template)
        print(document.get_merge_fields())
        document.merge(
            patient=self.patientName.text(),
            chart=self.chartNumber.text(),
            surgeon=self.doctor,
            date=self.date.text(),
            uncover_date=uncoverVal,
            restore_date=self.restoreDate.text(),
            implant=implants,
            healing_cap="healingCaps",
            restorative_parts=parts,
            report=reports,
            restore=restoreChoice,
            anesthetic=anestheticChoice,
            tolerance=toleranceChoice,
            prescriptions=rxChoice)

        #xray = "C:\\PythonProjects\\ImplantApp\\app\\static\\images\\exampleXray.jpeg"
        document.write('temp.docx')
        doc = Document('temp.docx')
        if self.xrayPath != None:

            tables = doc.tables

            p = tables[0].rows[0].cells[0].add_paragraph()
            r = p.add_run()
            r.add_picture(self.xrayPath, width=Inches(2.5), height=Inches(2.5))

        with open("data/fileLocations.txt", "r") as content:
            lines = content.readlines()
        dir = lines[0][8:]
        doc.save('test5.docx')

        os.remove('temp.docx')





class NewImplantForm(QWidget):
    def __init__(self):
        super(NewImplantForm, self).__init__()
        uic.loadUi('ui/newImplantForm.ui', self)

        self.implant = ""
        self.implantTree = self.findChild(QTreeView, 'implantList')
        self.makeImplantTree()
        self.implantTree.clicked.connect(self.implantChanged)

        self.toothNumber = self.findChild(QLineEdit, 'toothNumber')
        self.lotNumber = self.findChild(QLineEdit, 'lotNumber')
        self.expirationDate = self.findChild(QDateEdit, 'expirationDate')
        self.expirationDate.setDate(QDate.currentDate())

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
        self.depthBox = self.findChild(QGroupBox, 'depthBox')

        self.healingCapBox = self.findChild(QGroupBox, 'healingCapBox')
        self.healingCapEdit = self.findChild(QLineEdit, 'healingCapEdit')

        self.graftBox = self.findChild(QGroupBox, 'graftBox')

        #self.generateParagraph()

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

        self.findChild(QLabel, "implantBoxLabel").setText("Implant: "+self.implant)

        self.implantSeatedBox.setTitle("A " + self.implant + " implant was seated to depth. ")

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
        f.close()
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

    def getIncision(self):
        if not self.incisionBox.isChecked():
            return ""

        button1 = self.incisionBox.findChild(QRadioButton, 'incisionButton1')
        button2 = self.incisionBox.findChild(QRadioButton, 'incisionButton2')
        edit1 = self.incisionBox.findChild(QLineEdit, 'incisionEdit1')
        edit2 = self.incisionBox.findChild(QLineEdit, 'incisionEdit2')

        if button1.isChecked():
            teeth = edit1.text().split(",")
            if len(teeth) > 1:
                return "Sulcular incisions were made around teeth #"+edit1.text()+". "
            else:
                return "Sulcular incisions were made around tooth #" + edit1.text()+". "
        elif button2.isChecked():
            teeth = edit2.text().split(",")
            if len(teeth) > 1:
                return "A crestal incision was made distal of teeth #" + edit2.text()+". "
            else:
                return "A crestal incision was made between tooth #" + edit2.text()+". "
        else:
            return ""

    def getFlap(self):
        if not self.flapBox.isChecked():
            return ""

        for flap in self.flapBox.findChildren(QRadioButton):
            if flap.isChecked():
                return flap.text()
        return ""

    def getExtraction(self):
        if not self.extractionBox.isChecked():
            return ""

        edit = self.extractionBox.findChild(QLineEdit, "extractionEdit")
        btn1 = self.extractionBox.findChild(QRadioButton, "extractionButton1")
        btn2 = self.extractionBox.findChild(QRadioButton, "extractionButton2")
        btn3 = self.extractionBox.findChild(QRadioButton, "extractionButton3")
        btn4 = self.extractionBox.findChild(QRadioButton, "extractionButton4")

        teeth = edit.text().split(",")
        txt = ""
        if len(teeth) > 1:
            txt += "Teeth "+edit.text()+" were removed via forcep extraction. "
            if btn1.isChecked():
                txt += "The sockets were perfectly preserved. "
            elif btn2.isChecked():
                txt += "The sockets were well preserved. "
            elif btn3.isChecked():
                txt += "The sockets were moderately preserved. "
            elif btn4.isChecked():
                txt += "There was damage to the sockets. "
        else:
            txt += "Tooth " + edit.text() + " was removed via forcep extraction. "
            if btn1.isChecked():
                txt += "The socket was perfectly preserved. "
            elif btn2.isChecked():
                txt += "The socket was well preserved. "
            elif btn3.isChecked():
                txt += "The socket was moderately preserved. "
            elif btn4.isChecked():
                txt += "There was damage to the socket. "
        return txt

    def getOsteotomy(self):
        if not self.osteotomyBox.isChecked():
            return ""

        button1 = self.osteotomyBox.findChild(QRadioButton, 'osteotomyButton1')
        button2 = self.osteotomyBox.findChild(QRadioButton, 'osteotomyButton2')
        edit1 = self.osteotomyBox.findChild(QLineEdit, 'osteotomyEdit1')
        edit2 = self.osteotomyBox.findChild(QLineEdit, 'osteotomyEdit2')

        if button1.isChecked():
            teeth = edit1.text().split(",")
            if len(teeth) > 1:
                return "An osteotomy was prepared in sites #"+edit1.text()+". "
            else:
                return "An osteotomy was prepared in site #" + edit1.text()+". "
        elif button2.isChecked():
            teeth = edit2.text().split(",")
            if len(teeth) > 1:
                return "An osteotomy was prepared in sockets #" + edit2.text()+". "
            else:
                return "An osteotomy was prepared in socket #" + edit2.text()+". "
        else:
            return ""

    def getBoneDensity(self):
        if not self.boneDensityBox.isChecked():
            return ""

        for density in self.boneDensityBox.findChildren(QRadioButton):
            if density.isChecked():
                return density.text()
        return ""

    def getPerforation(self):
        if not self.perforationsBox.isChecked():
            return ""

        for perforation in self.perforationsBox.findChildren(QRadioButton):
            if perforation.isChecked():
                return perforation.text()
        return ""

    def getTapped(self):
        if not self.tappedBox.isChecked():
            return "The site was not tapped. "
        else:
            return "The site was tapped. "

    def getSinus(self):
        if not self.sinusBox.isChecked():
            return ""

        for opt in self.sinusBox.findChildren(QRadioButton):
            if opt.isChecked():
                return opt.text()
        return ""

    def getSeated(self):
        if not self.implantSeatedBox.isChecked():
            return self.implantSeatedBox.title().replace("was", "was not")
            # return ""
        else:
            return self.implantSeatedBox.title()

    def getDepth(self):
        if not self.depthBox.isChecked():
            return ""

        for opt in self.depthBox.findChildren(QRadioButton):
            if opt.isChecked():
                return opt.text()
        return ""

    # def getCover(self):
    #     if not self.cove.isChecked():
    #         return ""

    def getHealingCap(self):
        if not self.healingCapBox.isChecked():
            return ""

        btn1 = self.healingCapBox.findChild(QRadioButton, 'healingCapButton1')
        btn2 = self.healingCapBox.findChild(QRadioButton, 'healingCapButton2')
        edit = self.healingCapBox.findChild(QLineEdit, 'healingCapEdit')


        if btn1.isChecked():
            return "A cover screw was placed. "
        else:
            return "A " + edit.text() + " healing cap was placed for a single stage approach."

    def getGraft(self):
        if not self.graftBox.isChecked():
            return ""

        boneMaterialBox = self.graftBox.findChild(QGroupBox, "boneMaterialBox")
        boneMembraneBox = self.graftBox.findChild(QGroupBox, "boneMembraneBox")
        boneMaterial = ""
        boneMembrane = ""

        for opt in boneMaterialBox.findChildren(QRadioButton):
            if opt.isChecked():
                boneMaterial = opt.text()
        for opt in boneMembraneBox.findChildren(QRadioButton):
            if opt.isChecked():
                boneMembrane = opt.text()

        return "The site was grafted with "+boneMaterial+" and covered with a "+boneMembrane+" membrane. "

    def generateParagraph(self):
        #print("generating paragraph")
        txt = ""
        txt += self.getIncision()
        txt += self.getFlap()
        txt += self.getExtraction()
        txt += self.getOsteotomy()

        txt += self.getBoneDensity()
        txt += self.getPerforation()
        txt += self.getTapped()
        txt += self.getSinus()
        txt += self.getSeated()
        txt += self.getDepth()
        #txt += self.getCover()
        txt += self.getHealingCap()
        txt += self.getGraft()
        return txt

    def getRestorativeParts(self):
        #print(self.restorativePartsList.findChildren(QCheckBox))
        options = self.findChild(QScrollArea, "restorativePartsScroll").findChildren(QCheckBox)

        txt = ""
        for opt in options:
            if opt.isChecked():
               txt += opt.text() + "\n"
        return txt

    def getImplant(self):
        return str(self.implant)





