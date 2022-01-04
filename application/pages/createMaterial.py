import os.path

from PyQt5.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget)

class MaterialPage(QWidget):

    def __init__(self):
        super(MaterialPage, self).__init__()

        self.setWindowTitle("Bone Materials")
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

        self.layout = QGridLayout()

        self.layout.setRowStretch(50,2)

        self.setLayout(self.layout)
        self.materialLayout = QGridLayout()
        self.membraneLayout = QGridLayout()
        self.layout.addWidget(QLabel("Materials", font=self.myFontBold), 0, 0)
        self.layout.addWidget(QLabel("Membranes", font=self.myFontBold), 0, 1)
        self.layout.addLayout(self.materialLayout, 1, 0)
        self.layout.addLayout(self.membraneLayout, 1, 1)
        self.createMatBtn = QPushButton(text="Add Material", font=self.myFont)
        self.createMatBtn.clicked.connect(self.createMaterial)
        self.layout.addWidget(self.createMatBtn, 2, 0)
        self.createMemBtn = QPushButton(text="Add Membrane", font=self.myFont)
        self.createMemBtn.clicked.connect(self.createMembrane)
        self.layout.addWidget(self.createMemBtn, 2, 1)


        # Functions
        self.readMaterials()

    def readMaterials(self):
        # Read Bone Materials
        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\materials.txt')
        with open(path_to_dat, "r") as content:
            lines = content.readlines()

        self.materials = []
        self.membranes = []

        for line in lines:
            parts = line.split("_", 1)
            if len(parts) < 2:
                continue
            if parts[0] == "mat":
                self.materials.append(parts[1].strip())
            elif parts[0] == "mem":
                self.membranes.append(parts[1].strip())

        i = 0
        for mat in self.materials:
            matLabel = QLabel(mat, font=self.myFont)
            deleteBtn = QPushButton("Delete", font=self.myFont)
            deleteBtn.setObjectName(mat)
            deleteBtn.clicked.connect(self.deleteMaterial)
            self.materialLayout.addWidget(matLabel, i, 0)
            self.materialLayout.addWidget(deleteBtn, i, 1)

            i += 1

        j = 0
        for mem in self.membranes:
            memLabel = QLabel(mem, font=self.myFont)
            deleteBtn = QPushButton("Delete", font=self.myFont)
            deleteBtn.setObjectName(mem)
            deleteBtn.clicked.connect(self.deleteMembrane)
            self.membraneLayout.addWidget(memLabel, j, 0)
            self.membraneLayout.addWidget(deleteBtn, j, 1)

            j += 1

    def deleteMaterial(self):
        removedMat = self.sender().objectName()
        self.materials.remove(removedMat)

        self.updateFile()

    def createMaterial(self):
        def getNewMat():
            newMat = edit.text()
            self.materials.append(newMat)
            d.deleteLater()

        d = QDialog()
        d.setWindowTitle("New Material")
        l = QVBoxLayout()
        d.setLayout(l)
        edit = QLineEdit(font=self.myFont)

        l.addWidget(edit)
        addBtn = QPushButton("Add", font=self.myFont)
        addBtn.clicked.connect(getNewMat)
        l.addWidget(addBtn)
        d.exec_()

        self.updateFile()

    def deleteMembrane(self):
        removedMem = self.sender().objectName()
        self.membranes.remove(removedMem)

        self.updateFile()

    def createMembrane(self):
        def getNewMem():
            newMem = edit.text()
            self.membranes.append(newMem)
            d.deleteLater()

        d = QDialog()
        d.setWindowTitle("New Membrane")
        l = QVBoxLayout()
        d.setLayout(l)
        edit = QLineEdit(font=self.myFont)

        l.addWidget(edit)
        addBtn = QPushButton("Add", font=self.myFont)
        addBtn.clicked.connect(getNewMem)
        l.addWidget(addBtn)
        d.exec_()

        self.updateFile()

    def updateFile(self):

        labeledMats = []
        for mat in self.materials:
            labeledMats.append(("mat_" + mat + "\n"))
        labeledMems = []
        for mem in self.membranes:
            labeledMems.append(("mem_" + mem + "\n"))

        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\materials.txt')
        with open(path_to_dat, "w") as content:
            content.writelines(labeledMats)
            content.writelines(labeledMems)

        for i in reversed(range(self.materialLayout.count())):
            self.materialLayout.itemAt(i).widget().deleteLater()
        for j in reversed(range(self.membraneLayout.count())):
            self.membraneLayout.itemAt(j).widget().deleteLater()
        self.readMaterials()