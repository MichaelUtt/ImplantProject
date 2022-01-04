import os.path

from PyQt5.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget)

class PrescriptionPage(QWidget):

    def __init__(self):
        super(PrescriptionPage, self).__init__()

        self.setWindowTitle("Prescriptions")
        self.setWindowIcon(QIcon('data/favicon.ico'))

        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )

        # Display
        self.myFont = QFont("MS Shell Dlg 2", 12)
        self.myFontBold = QFont("MS Shell Dlg 2", 12, QFont.Bold)

        self.layout = QVBoxLayout()

        self.setLayout(self.layout)
        self.rxLayout = QGridLayout()
        self.layout.addWidget(QLabel("Prescriptions", font=self.myFontBold), 0)
        self.layout.addLayout(self.rxLayout, 1)
        self.createRxBtn = QPushButton(text="Add Prescription", font=self.myFont)
        self.createRxBtn.clicked.connect(self.createRx)
        self.layout.addWidget(self.createRxBtn, 2)

        self.layout.insertStretch(3, 2)
        # Functions
        self.readRx()

    def readRx(self):
        # Read Prescriptions
        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\prescriptions.txt')
        with open(path_to_dat, "r") as content:
            lines = content.readlines()

        self.rx = []

        for line in lines:
            if len(line) > 2:
                self.rx.append(line.strip())

        i = 0
        for r in self.rx:
            rxLabel = QLabel(r, font=self.myFont)
            deleteBtn = QPushButton("Delete", font=self.myFont)
            deleteBtn.setObjectName(r)
            deleteBtn.clicked.connect(self.deleteRx)
            self.rxLayout.addWidget(rxLabel, i, 0)
            self.rxLayout.addWidget(deleteBtn, i, 1)

            i += 1


    def deleteRx(self):
        removedRx = self.sender().objectName()
        self.rx.remove(removedRx)

        self.updateFile()

    def createRx(self):
        def getNewRx():
            newRx = edit.text()
            self.rx.append(newRx)
            d.deleteLater()

        d = QDialog()
        d.setWindowTitle("New Prescription")
        l = QVBoxLayout()
        d.setLayout(l)
        edit = QLineEdit(font=self.myFont)

        l.addWidget(edit)
        addBtn = QPushButton("Add", font=self.myFont)
        addBtn.clicked.connect(getNewRx)
        l.addWidget(addBtn)
        d.exec_()

        self.updateFile()

    def updateFile(self):

        labeledRx = []
        for rx in self.rx:
            labeledRx.append((rx + "\n"))

        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\prescriptions.txt')
        with open(path_to_dat, "w") as content:
            content.writelines(labeledRx)

        for i in reversed(range(self.rxLayout.count())):
            self.rxLayout.itemAt(i).widget().deleteLater()

        self.readRx()