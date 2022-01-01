from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QCheckBox, QComboBox, QLineEdit, QPushButton, QWidget, QListView, QFrame
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5 import uic

class PartPage(QWidget):
    def __init__(self):
        super(PartPage, self).__init__()
        uic.loadUi('ui/addPart.ui', self)

        self.setWindowTitle("Restorative Parts")
        self.setWindowIcon(QIcon('data/favicon.ico'))

        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )


        # Restorative Parts View
        self.showPartsBox = self.findChild(QCheckBox, "showPartsBox")
        self.showPartsBox.toggled.connect(self.showParts)
        self.partView = self.findChild(QFrame, "partViewer")
        self.partList = self.findChild(QListView, 'partList')
        self.partList.clicked.connect(self.partChanged)
        self.deleteButton = self.findChild(QPushButton, 'deleteButton')
        self.deleteButton.clicked.connect(self.deletePart)

        self.makePartList()
        self.showParts(False)

        # Add Part
        self.partParent = self.findChild(QComboBox, "partParent")
        self.partEdit = self.findChild(QLineEdit, "partEdit")
        self.partButton = self.findChild(QPushButton, "partButton")
        self.partButton.clicked.connect(self.addPart)
        self.setPartParents()

        # Add Category
        self.categoryEdit = self.findChild(QLineEdit, "categoryEdit")
        self.categoryButton = self.findChild(QPushButton, "categoryButton")
        self.categoryButton.clicked.connect(self.addCategory)

        self.show()

    def showParts(self, val):

        self.partViewHeight = self.partView.height()
        if val:
            self.partView.show()
            newSize = QSize(self.width(), self.height() + self.partViewHeight)
            self.setFixedSize(newSize)
        else:
            self.partView.hide()
            newSize = QSize(self.width(), self.height() - self.partViewHeight)
            self.setFixedSize(newSize)


    def makePartList(self):

        f = open("data/restorativeParts.txt", "r")

        listModel = QStandardItemModel()
        rootNode = listModel.invisibleRootItem()


        for line in f:
            if line[0] == "&":
                myFont = QFont()
                myFont.setBold(True)

                category = QStandardItem(line[1:-1])
                category.setFont(myFont)

                rootNode.appendRow(category)


            else:
                if len(line) > 3:
                    option = QStandardItem(line[0:-1])
                    rootNode.appendRow(option)

        self.partList.setModel(listModel)
        f.close()

    def partChanged(self, index):
        self.selectedPart = self.partList.model().itemFromIndex(index)
        self.deleteButton.setText("Delete: " + self.selectedPart.text())
        self.deleteButton.setFont(self.selectedPart.font())
        self.deleteButton.setEnabled(True)

    def deletePart(self):

        f = open("data/restorativeParts.txt", "r")
        lines = f.readlines()
        f.close()

        selected = self.selectedPart.text()
        #print(selected)
        i = 0
        for line in lines:
            #print(line)
            if line[0] == "&":
                if selected in line[1:-1]:
                    if i+1 < len(lines):
                        if lines[i+1][0] == "&" or i+3 > len(lines):
                            lines.remove(line)
                            break
                    else:
                        lines.remove(line)
                        break

            else:
                if len(line) > 3:
                    if selected in line:
                        lines.remove(line)
                        break
            i += 1

        f = open("data/restorativeParts.txt", "w")
        f.writelines(lines)
        f.close()

        self.makePartList()
        self.setPartParents()
        self.deleteButton.setText("Delete: ")
        self.deleteButton.setEnabled(False)



    def addPart(self):
        with open("data/restorativeParts.txt", "r") as content:
            parts = content.readlines()

        category = self.partParent.currentText()

        startIndex = 0
        categorySelected = False
        endIndex = len(parts)
        i = 0
        for part in parts:
            if part[0] == "&":
                if category in part:
                    categorySelected = True
                    startIndex = i
                elif categorySelected:
                    categorySelected = False
                    endIndex = i
            i += 1

        categoryChildren = []
        for partIndex in range(startIndex,endIndex):
            categoryChildren.append(parts[partIndex])


        if self.partEdit.text() not in parts:
            categoryChildren.append(self.partEdit.text()+"\n")
            categoryChildren = sorted(categoryChildren)

        newParts = parts[:startIndex]
        newParts.extend(categoryChildren)
        newParts.extend(parts[endIndex:])

        with open("data/restorativeParts.txt", "w") as content:
            content.writelines(newParts)

        self.makePartList()

    def setPartParents(self):

        with open("data/restorativeParts.txt", "r") as content:
            parts = content.readlines()

        options = []
        for line in parts:
            if line[0] == "&":
                options.append(line[1:].replace("\n", ""))


        self.partParent.clear()
        self.partParent.addItems(options)

    def addCategory(self):

        with open("data/restorativeParts.txt", "a") as content:
            content.writelines(("&"+self.categoryEdit.text()+"\n"))

        self.makePartList()
        self.setPartParents()


