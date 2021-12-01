from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate, QSize
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

class ImplantPage(QWidget):
    def __init__(self):
        super(ImplantPage, self).__init__()
        uic.loadUi('ui/addImplant.ui', self)

        self.setWindowTitle("Implants")

        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint
        )

        # Implant View
        self.showImplantsBox = self.findChild(QCheckBox, "showImplantsBox")
        self.showImplantsBox.toggled.connect(self.showImplants)
        self.implantView = self.findChild(QScrollArea, "implantView")
        self.implantTree = self.findChild(QTreeView, 'implantList')
        self.implantTree.clicked.connect(self.implantChanged)
        self.deleteButton = self.findChild(QPushButton, 'deleteButton')
        self.deleteButton.clicked.connect(self.deleteImplant)
        self.showImplants(False)
        self.makeImplantTree()

        # Add Implant
        self.implantParent = self.findChild(QComboBox, "implantParent")
        self.implantEdit = self.findChild(QLineEdit, "implantEdit")
        self.implantButton = self.findChild(QPushButton, "implantButton")
        self.implantButton.clicked.connect(self.addImplant)
        self.setImplantParents()

        # Add Category
        self.categoryParent = self.findChild(QComboBox, "categoryParent")
        self.categoryEdit = self.findChild(QLineEdit, "categoryEdit")
        self.categoryButton = self.findChild(QPushButton, "categoryButton")
        self.categoryButton.clicked.connect(self.addCategory)
        self.setCategoryParents()

        self.show()

    def showImplants(self, val):
        if val:
            self.implantView.show()
            newSize = QSize(self.width(), self.height() + self.implantView.height())
            self.setFixedSize(newSize)
        else:
            self.implantView.hide()
            newSize = QSize(self.width(), self.height() - self.implantView.height())
            self.setFixedSize(newSize)

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
        #self.implantTree.expandAll()
        self.implantTree.setHeaderHidden(True)

    def implantChanged(self, index):
        self.selectedImplant = self.implantTree.model().itemFromIndex(index)
        self.deleteButton.setText("Delete: " + self.selectedImplant.text())
        self.deleteButton.setEnabled(True)

    def deleteImplant(self):
        with open("data/implants.json", "r") as content:
            implants = json.load(content)


        selected = self.selectedImplant.text()

        for root, child in implants.items():

            try:
                for root2, grandchild in child.items():
                    if selected in grandchild:
                        grandchild.remove(selected)
                    if selected == root2 and len(grandchild) < 1:
                        child.pop(root2)
                        break
                if selected == root and len(child) < 1:
                    implants.pop(root)
                    break


            except AttributeError:
                if selected in child:
                    child.remove(selected)
                if selected == root and len(child) < 1:
                    implants.pop(root)
                    break

        print(implants)
        with open("data/implants.json", "w") as content:
            json.dump(implants, content)

        self.makeImplantTree()
        self.setCategoryParents()
        self.setImplantParents()
        self.deleteButton.setText("Delete: ")
        self.deleteButton.setEnabled(False)

    def addImplant(self):
        with open("data/implants.json", "r") as content:
            implants = json.load(content)

        location = self.implantParent.currentText().split("/")
        print(location)
        if len(location) > 1:
            if self.implantEdit.text() not in implants[location[0]][location[1]]:
                implants[location[0]][location[1]].append(self.implantEdit.text())
                implants[location[0]][location[1]] = sorted(implants[location[0]][location[1]])
        else:
            if self.implantEdit.text() not in implants[location[0]]:
                implants[location[0]].append(self.implantEdit.text())
                implants[location[0]] = sorted(implants[location[0]])

        with open("data/implants.json", "w") as content:
            json.dump(implants, content)

        self.makeImplantTree()

    def setImplantParents(self):

        with open("data/implants.json", "r") as content:
            implants = json.load(content)

        options = []
        for root, child in implants.items():
            #options.append(root)
            #print(root)
            outer = QStandardItem(root)
            #print(child)
            try:
                for root2, grandchild in child.items():
                    options.append(root + "/" + root2)
            except AttributeError:
                options.append(root)


        self.implantParent.clear()
        self.implantParent.addItems(options)

    def addCategory(self):
        with open("data/implants.json", "r") as content:
            implants = json.load(content)

        location = self.categoryParent.currentText()

        if location == "New Branch":
            implants[self.categoryEdit.text()] = {}
        else:
            if self.implantEdit.text() not in implants[location]:
                implants[location][self.categoryEdit.text()] = []
        print(implants)


        with open("data/implants.json", "w") as content:
            json.dump(implants, content)

        self.makeImplantTree()
        self.setCategoryParents()
        self.setImplantParents()

    def setCategoryParents(self):

        with open("data/implants.json", "r") as content:
            implants = json.load(content)

        options = ["New Branch"]
        for root, child in implants.items():

            try:
                for root2, grandchild in child.items():
                    break
                options.append(root)
            except AttributeError:
                if len(child) < 1:
                    options.append(root)


        self.categoryParent.clear()
        self.categoryParent.addItems(options)

