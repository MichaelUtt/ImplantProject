import os.path

from PyQt5.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget)

class AnestheticPage(QWidget):

    def __init__(self):
        super(AnestheticPage, self).__init__()

        self.setWindowTitle("Anesthetic")
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
        self.anesLayout = QGridLayout()
        self.layout.addWidget(QLabel("Anesthetic", font=self.myFontBold), 0)
        self.layout.addLayout(self.anesLayout, 1)
        self.createAnesBtn = QPushButton(text="Add Anesthetic", font=self.myFont)
        self.createAnesBtn.clicked.connect(self.createAnes)
        self.layout.addWidget(self.createAnesBtn, 2)

        self.layout.insertStretch(3, 2)
        # Functions
        self.readAnes()

    def readAnes(self):
        # Read Anesthetics
        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\anesthetics.txt')
        with open(path_to_dat, "r") as content:
            lines = content.readlines()

        self.anes = []

        for line in lines:
            if len(line) > 2:
                self.anes.append(line.strip())

        i = 0
        for a in self.anes:
            anesLabel = QLabel(a, font=self.myFont)
            deleteBtn = QPushButton("Delete", font=self.myFont)
            deleteBtn.setObjectName(a)
            deleteBtn.clicked.connect(self.deleteAnes)
            self.anesLayout.addWidget(anesLabel, i, 0)
            self.anesLayout.addWidget(deleteBtn, i, 1)

            i += 1

    def deleteAnes(self):
        removedAnes = self.sender().objectName()
        self.anes.remove(removedAnes)

        self.updateFile()

    def createAnes(self):
        def getNewAnes():
            newAnes = edit.text()
            self.anes.append(newAnes)
            d.deleteLater()

        d = QDialog()
        d.setWindowTitle("New Anesthetic")
        l = QVBoxLayout()
        d.setLayout(l)
        edit = QLineEdit(font=self.myFont)

        l.addWidget(edit)
        addBtn = QPushButton("Add", font=self.myFont)
        addBtn.clicked.connect(getNewAnes)
        l.addWidget(addBtn)
        d.exec_()

        self.updateFile()

    def updateFile(self):

        labeledAnes = []
        for anes in self.anes:
            labeledAnes.append((anes + "\n"))

        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\anesthetics.txt')
        with open(path_to_dat, "w") as content:
            content.writelines(labeledAnes)

        for i in reversed(range(self.anesLayout.count())):
            self.anesLayout.itemAt(i).widget().deleteLater()

        self.readAnes()