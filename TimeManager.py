"""
Author: Michael Utt

Notes:
    Use external files
        > ImplantReports
            > reports
                > lastFirst.json (look at other extensions)
                > lastFirst.pdf (a viewable file if wanted?)
            > implants.txt (maybe a folder depending on what is needed or .json)
            > properties.txt (.json?)
            > README.txt (.txt is more universal)
            >
    properties.txt
        Savepath
        LastDoctor
        AllDoctors[]
        Theme
        Color
        anesthetics[]
        tolerances[]
        prescriptions[]
        firstTime[] = false (tips to make the software clearer on first use)


    Settings menu so all the customization options are not overwhelming
        Doctor Name
        Save path (can I open an external window?)
        Various Colors
        Contact info
    First time start up menu if no preexisting properties exist
        Doctor Name:
        Save Location: C:\Program Files\ImplantReports
        Note: further customization available in settings
    <HomePage>
        Create a new implant report
            <CreateReport>
                Patient:
                    Last:   First:   Chart #:
                Surgeon: <default> or allow a new doctor to be added
                Date: <get computer time> or leave blank
                Uncover: Blank
                Restore: Blank

                [Add x-ray]

                Implant Type:
                <implant type selector>#<tooth #>
                <healing cap size?>#<tooth #>

                Restorative Part to Order:

                Report:

                Anesthestic: <options> [new anesthestic]
                Patient Tolerance: (<options> [new tolerance]) or blank
                Rx: <options> [new prescription]

                [Save]

        View implant reports
            <ViewReports>
                Search: <by name or # or doctor or date(eh)>
                Order By: <Last name or # or date added>
                Reports:
                [Last name | First name | Doctor      | Date     ]
                 Utt         Michael      David Engen   4/23/2021
            <EditReport>
                Similar to create
            <DeleteReport>
                Double check
        Add a new implant
            <CreateImplant>
                Will be easy once reports are inplace. Need more info on details.
        View implants (may merge with create implant)
            <ReadImplants>
                Search: <name>
                Implants:
                [implant name]
                [implant name]
            <EditImplant>
            <DeleteImplant>
                Double Check



    When saving a file make a backup with the previous
        How many backups? Never delete? Delete after successful open?

    Things to keep in check:
        Forward and backwards on all pages
            Do a double check on backs when on create pages
        Exit works from all places
    On save display a text bubble displaying the full path of the saved file





Time worked:
30 hours
16 hours


"""

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QFont, QMouseEvent, QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QInputDialog, QMessageBox, QDateEdit, QFileDialog)
import sys
import pymongo
#from datetime import date
from mailmerge import MailMerge

myclient = pymongo.MongoClient()
mydb = myclient["reports"]

mycol = mydb["patients"]

#post = {"number": 7}
#mycol.insert_one(post)

newWindow = None
resolution = (800, 900)

allDoctors = ["David Engen", "Add new Doctor"]
allImplants = ["Select Implant", "Implant 1", "Implant 2"]
allAnesthetics = ["None", "New Anesthetic", "Anesthetic 1"]
allPrescriptions = ["None", "New Prescription", "Prescription 1"]

class HomePage(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setHidden(False)
        self.setWindowTitle("Home")
        self.resize(resolution[0], resolution[1])

        QApplication.setStyle("Fusion")


        self.topLeftGroupBox = QGroupBox()

        self.createButton = QPushButton("Create New Report", self)
        self.createButton.resize(300, 500)

        # self.createButton.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        # self.createButton.move(275, 200)
        # self.createButton.setToolTip("<h3>Create a new </h3>")

        self.createButton.clicked.connect(self.createReport)

        hbox = QHBoxLayout()
        #hbox.addStretch(1)

        hbox.addWidget(self.createButton)

        # hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        #vbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox.setAlignment(Qt.AlignHCenter)
        # vbox.setAlignment(Qt.AlignCenter)


        self.setLayout(vbox)







    def createReport(self):
        global newWindow
        newWindow = CreateReport(self)
        newWindow.show()
        self.destroy()
        # gallery = CreateReport()
        # gallery.show()
        # self.hide()
"""
<CreateReport>
                Patient:
                    Last:   First:   Chart #:
                Surgeon: <default> or allow a new doctor to be added
                Date: <get computer time> or leave blank
                Uncover: Blank
                Restore: Blank

                [Add x-ray]

                Implant Type:
                <implant type selector>#<tooth #>
                <healing cap size?>#<tooth #>

                Restorative Part to Order:

                Report:

                Anesthestic: <options> [new anesthestic]
                Patient Tolerance: (<options> [new tolerance]) or blank
                Rx: <options> [new prescription]

                [Save]
"""
class CreateReport(QDialog):

    def declareVars(self):
        self.name = " "
        self.chartNumber = " "
        self.surgeonName = " "
        self.date = " "
        self.uncoverDate = " "
        self.restoreDate = " "

        self.implantType = " "
        self.implantTooth = " "
        self.healingCapSize = " "
        self.healingCapTooth = " "

        self.restorativePartOrder = " "

        self.report = " "

        self.anesthetic = "None"
        self.tolerance = "0"
        self.rx = "None"

        self.imagePath = " "

    def __init__(self, parent=None):

        super().__init__()
        self.setWindowTitle("Create")
        self.resize(resolution[0], resolution[1])
        self.setFont(QFont('Arial', 12))
        self.declareVars()

        self.grid = QGridLayout()

        titleLabel = QLabel("Implant Surgery Report")
        titleLabel.setFont(QFont('Arial', 22))
        titleLabel.setAlignment(Qt.AlignHCenter)
        titleLabel.setContentsMargins(0,0,0,25)
        self.grid.addWidget(titleLabel, 0, 1, 1, 2)

        patientGrid = QGridLayout()
        patientGrid.setAlignment(Qt.AlignBottom)

        nameField = QLineEdit()
        chartNumberField = QLineEdit()
        nameField.textChanged.connect(self.setFirstName)
        chartNumberField.textChanged.connect(self.setChartNum)
        patientGrid.addWidget(nameField, 2, 1)
        patientGrid.addWidget(chartNumberField, 2, 3)

        nameLabel = QLabel()
        chartNumberLabel = QLabel()
        nameLabel.setText("Patient Name")
        chartNumberLabel.setText("Chart Number")
        nameLabel.setBuddy(nameField)
        chartNumberLabel.setBuddy(chartNumberField)
        nameLabel.setAlignment(Qt.AlignBottom)
        chartNumberLabel.setAlignment(Qt.AlignBottom)
        patientGrid.addWidget(nameLabel, 1, 1)
        patientGrid.addWidget(chartNumberLabel, 1, 3)

        #patientGrid.setContentsMargins(0,0,200,0)
        self.grid.addLayout(patientGrid, 1, 1, 1, 2)

        topGrid = QGridLayout()

        self.surgeonBox = QComboBox()
        self.surgeonBox.addItems(allDoctors)
        self.surgeonName = allDoctors[0]
        self.surgeonBox.currentIndexChanged.connect(self.setSurgeon)
        topGrid.addWidget(self.surgeonBox, 3, 2)
        surgeonLabel = QLabel()
        surgeonLabel.setBuddy(self.surgeonBox)
        surgeonLabel.setText("Surgeon")
        topGrid.addWidget(surgeonLabel, 3, 1)


        dateLabel = QLabel()
        dateLabel.setText("Date")
        topGrid.addWidget(dateLabel, 4, 1)
        self.dateField = QDateEdit(calendarPopup=True)
        self.dateField.setDateTime(QDateTime.currentDateTime())
        self.dateField.dateChanged.connect(self.setDate)
        self.date = QDateTime.currentDateTime().toString()
        topGrid.addWidget(self.dateField, 4, 2)

        uncoverLabel = QLabel()
        uncoverLabel.setText("Uncover Date")
        topGrid.addWidget(uncoverLabel, 5, 1)
        self.uncoverField = QDateEdit(calendarPopup=True)
        self.uncoverField.setDateTime(QDateTime.currentDateTime())
        self.uncoverField.dateChanged.connect(self.setUncoverDate)
        self.uncoverDate = QDateTime.currentDateTime().toString()
        topGrid.addWidget(self.uncoverField, 5, 2)

        restoreLabel = QLabel()
        restoreLabel.setText("Restore Date")
        topGrid.addWidget(restoreLabel, 6, 1)
        self.restoreField = QDateEdit(calendarPopup=True)
        self.restoreField.setDateTime(QDateTime.currentDateTime())
        self.restoreField.dateChanged.connect(self.setRestoreDate)
        self.restoreDate = QDateTime.currentDateTime().toString()
        topGrid.addWidget(self.restoreField, 6, 2)

        self.grid.addLayout(topGrid,2,1,1,2)

        implantLabel = QLabel()
        implantLabel.setText("Implant Type")
        implantLabel.setFont(QFont('Arial', 18))
        implantLabel.setContentsMargins(0,25,0,5)
        self.grid.addWidget(implantLabel, 3, 1)

        implantGrid = QGridLayout()

        self.implantTypeBox = QComboBox()
        self.implantTypeBox.addItems(allImplants)
        self.implantTypeBox.currentIndexChanged.connect(self.setImplant)
        implantGrid.addWidget(self.implantTypeBox, 1, 1)
        self.implantToothNum = QLabel()
        self.implantToothNum.setBuddy(self.implantTypeBox)
        self.implantToothNum.mousePressEvent = self.setImplantNumber
        self.implantToothNum.setText("# 0")
        implantGrid.addWidget(self.implantToothNum, 1, 2)

        self.healingCapBox = QComboBox()
        self.healingCapBox.addItems(["Select Cap Size","0","1","2","3","4","5","6","7"])
        self.healingCapBox.currentIndexChanged.connect(self.setHealingCap)
        implantGrid.addWidget(self.healingCapBox, 2, 1)
        self.healingCapNum = QLabel()
        self.healingCapNum.setBuddy(self.implantTypeBox)
        self.healingCapNum.mousePressEvent = self.setHealingCapNumber
        self.healingCapNum.setText("# 0")
        implantGrid.addWidget(self.healingCapNum, 2, 2)

        self.grid.addLayout(implantGrid, 4,1,1,1)



        restorativePartLabel = QLabel()
        restorativePartLabel.setText("Restorative Part To Order")
        restorativePartLabel.setFont(QFont('Arial', 18))
        restorativePartLabel.setContentsMargins(0, 25, 0, 5)
        self.grid.addWidget(restorativePartLabel, 5, 1)

        restorativePartField = QLineEdit()
        restorativePartField.textChanged.connect(self.setRestoritivePartOrder)
        self.grid.addWidget(restorativePartField, 6, 1, 1, 2)

        reportLabel = QLabel()
        reportLabel.setText("Report")
        reportLabel.setFont(QFont('Arial', 18))
        reportLabel.setContentsMargins(0, 25, 0, 5)
        self.grid.addWidget(reportLabel, 7, 1)

        reportField = QTextEdit()
        #reportField.textChanged.connect(self.setReport)
        self.grid.addWidget(reportField, 8, 1, 1, 2)

        bottomGrid = QGridLayout()
        anestheticLabel = QLabel("Anesthetic: ")
        bottomGrid.addWidget(anestheticLabel, 1, 1)
        self.anestheticBox = QComboBox()
        self.anestheticBox.addItems(allAnesthetics)
        self.anestheticBox.currentIndexChanged.connect(self.setAnesthetic)
        bottomGrid.addWidget(self.anestheticBox, 1, 2)

        toleranceLabel = QLabel("Patient Tolerance: ")
        bottomGrid.addWidget(toleranceLabel, 1, 3)
        self.toleranceBox = QComboBox()
        self.toleranceBox.addItems(["1","2","3","4","5","6","7","8","9"])
        self.toleranceBox.currentIndexChanged.connect(self.setTolerance)
        bottomGrid.addWidget(self.toleranceBox, 1, 4)

        rxLabel = QLabel("Rx: ")
        bottomGrid.addWidget(rxLabel, 3, 1)
        self.rxBox = QComboBox()
        self.rxBox.addItems(allPrescriptions)
        self.rxBox.currentIndexChanged.connect(self.setRx)
        bottomGrid.addWidget(self.rxBox, 3, 2)

        self.grid.addLayout(bottomGrid, 9, 1, 1, 2)

        self.implantImage = QLabel()
        self.implantImage.mousePressEvent = self.setImage


        saveButton = QPushButton("Save", self)
        saveButton.clicked.connect(self.save)
        self.grid.addWidget(saveButton, 20, 1)

        selectImageButton = QPushButton("Seclect Image", self)
        selectImageButton.clicked.connect(self.setImage)
        self.grid.addWidget(selectImageButton, 20, 2)

        backButton = QPushButton("Back", self)
        backButton.clicked.connect(self.backBtn)
        self.grid.addWidget(backButton, 21, 1)



        self.grid.setAlignment(Qt.AlignTop)
        self.setLayout(self.grid)


    def backBtn(self):
        global newWindow

        # TODO : QMessageBox

        newWindow = HomePage(self)
        newWindow.show()
        # gallery.setHidden(False)
        self.destroy()
        # self.setHidden(False)

    def save(self):

        print('firstName',self.name)
        print('chartNumber',self.chartNumber)
        print('surgeonName',self.surgeonName)
        print('date',self.date)
        print('uncoverDate',self.uncoverDate)
        print('restoreDate',self.restoreDate)

        print('implantType',self.implantType)
        print('implantTooth',self.implantTooth)
        print('healingCapSize',self.healingCapSize)
        print('healingCapTooth',self.healingCapTooth)

        print('restorativePartOrder',self.restorativePartOrder)

        print("report",self.report)

        print('anesthetic',self.anesthetic)
        print('tolerance',self.tolerance)
        print('rx',self.rx)

        print('imagePath',self.imagePath)


        template = "implant_report.docx"

        document = MailMerge(template)

        document.merge(
            patient=self.name,
            chart=self.chartNumber,
            surgeon=self.surgeonName,
            date=self.date,
            uncover_date=self.uncoverDate,
            restore_date=self.restoreDate,
            implant=self.implantType,
            healing_cap=self.healingCapSize,
            restorative_parts=self.restorativePartOrder,
            report=self.report,
            restore='',#self.restore,
            anesthetic=self.anesthetic,
            tolerance=self.tolerance,
            prescriptions=self.rx)

        document.write('test-output.docx')





        #for x in mycol.find():
        #    print(x)

    def setFirstName(self, text):

        self.name = text


    def setChartNum(self, text):

        self.chartNumber = text

    def setSurgeon(self, i):

        if i == len(allDoctors)-1:
            name, _ = QInputDialog.getText(self, "Input Dialog", "Surgeon Name: ")
            if name == "" or name == " ":
                self.surgeonBox.setCurrentIndex(0)
                return
            allDoctors.insert(i, name)
            self.surgeonBox.removeItem(i)
            self.surgeonBox.addItem(name)
            self.surgeonBox.addItem("Add new doctor")
            self.surgeonBox.setCurrentIndex(i)
        self.surgeonName = allDoctors[i]

    def setDate(self, d):

        self.date = d.toString()
        # print(date)

    def setUncoverDate(self, d):

        self.uncoverDate = d.toString()

    def setRestoreDate(self, d):

        self.restoreDate = d.toString()

    def setImplant(self, i):

        self.implantType = self.implantTypeBox.itemText(i)
        self.setImplantNumber()

    def setImplantNumber(self, event=None):

        num, _ = QInputDialog.getInt(self, "Input Dialog", "Tooth Number: ")
        if num == "" or num == " ":
            self.implantToothNum.setText("# 0")
            return
        self.implantToothNum.setText("# "+str(num))
        self.implantTooth = str(num)

    def setHealingCap(self, i):

        self.healingCapSize = self.healingCapBox.itemText(i)
        self.setHealingCapNumber()

    def setHealingCapNumber(self, event=None):

        num, _ = QInputDialog.getInt(self, "Healing Cap Size", "Tooth Number: ")
        if num == "" or num == " ":
            self.healingCapNum.setText("# 0")
            return
        self.healingCapNum.setText("# "+str(num))
        self.healingCapTooth = str(num)

    def setRestoritivePartOrder(self, text):

        self.restorativePartOrder = text

    def setReport(self, text):

        self.report = text

    def setAnesthetic(self, i):

        if i == 1:
            anestheticName, _ = QInputDialog.getText(self, "New Anesthetic", "Anesthetic Name: ")
            if anestheticName == "" or anestheticName == " ":
                self.anestheticBox.setCurrentIndex(0)
                return
            allAnesthetics.append(anestheticName)
            self.anestheticBox.addItem(anestheticName)
            self.anestheticBox.setCurrentIndex(len(allAnesthetics)-1)
            self.anesthetic = anestheticName
        else:
            self.anesthetic = self.anestheticBox.itemText(i)

    def setTolerance(self, i):

        self.tolerance = self.toleranceBox.itemText(i)

    def setRx(self, i):

        if i == 1:
            prescriptionName, _ = QInputDialog.getText(self, "New Prescription", "Prescription Name: ")
            if prescriptionName == "" or prescriptionName == " ":
                self.rxBox.setCurrentIndex(0)
                return
            allPrescriptions.append(prescriptionName)
            self.rxBox.addItem(prescriptionName)
            self.rxBox.setCurrentIndex(len(allPrescriptions)-1)
            self.rx = prescriptionName
        else:
            self.rx = self.rxBox.itemText(i)

    def setImage(self, event=None):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "JPG Files (*.jpg);;All Files (*)", options=options)

        if fileName:
            pixmap = QPixmap(fileName)
            if pixmap.height() > resolution[1]:
                pixmap = pixmap.scaledToHeight(resolution[0])
            if pixmap.width() > resolution[0]*3:
                pixmap = pixmap.scaledToWidth(resolution[1])
            self.implantImage.setPixmap(pixmap)
            self.grid.addWidget(self.implantImage, 1, 3, 15, 1)
            self.imagePath = fileName

class ViewReports(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Home")

        def deleteReport(self, report):
            return


class EditReport(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Home")


class CreateImplant(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Home")


class ViewImplants(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Home")

        def deleteReport(self, report):
            return


class EditImplant(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Home")


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")
        self.changeStyle('Windows')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Group 2")

        defaultPushButton = QPushButton("Default Push Button")
        defaultPushButton.setDefault(True)

        togglePushButton = QPushButton("Toggle Push Button")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                               QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n"
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n"
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
