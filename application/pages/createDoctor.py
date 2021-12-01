from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate, QSize, pyqtSignal, pyqtSlot
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

class DoctorPage(QWidget):

    clickToRemove = pyqtSignal(int)

    @pyqtSlot()
    def removeDoc(self, index):
        print(index)

    def __init__(self):
        super(DoctorPage, self).__init__()

        self.setWindowTitle("Doctors")

        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )

        f = open("data/doctors.txt", "r")
        self.doctors = f.readlines()
        self.currentDocs = self.doctors
        f.close()
        self.resize(QSize(500,0))

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.docCount = 0
        for doc in self.doctors:
            self.createDoc(doc)

        self.layout.setRowStretch(20,2)

        addDocBtn = QPushButton("Add Doctor")
        addDocBtn.clicked.connect(self.addDoc)
        self.layout.addWidget(addDocBtn,21,0)

    def addDoc(self):

        def getNewDoc():
            newDoctor = edit.text()
            f = open("data/doctors.txt", "a")
            f.write((newDoctor + "\n"))
            f.close()
            self.createDoc(newDoctor)
            self.doctors.append((newDoctor + "\n"))
            d.deleteLater()
        d = QDialog()
        d.setWindowTitle("New Doctor")
        l = QVBoxLayout()
        d.setLayout(l)
        edit = QLineEdit()

        l.addWidget(edit)
        addBtn = QPushButton("Add")
        addBtn.clicked.connect(getNewDoc)
        l.addWidget(addBtn)
        d.exec_()

    def createDoc(self, name):
        doc = name.replace("\n", "")
        nameLabel = QLabel(doc)
        nameLabel.setObjectName("label" + str(self.docCount))
        self.layout.addWidget(nameLabel, self.docCount, 0)
        removeButton = QPushButton("Remove")
        removeButton.clicked.connect(removeButton.deleteLater)
        removeButton.pressed.connect(nameLabel.deleteLater)
        removeButton.clicked.connect(self.removeDoc)
        self.layout.addWidget(removeButton, self.docCount, 1)
        self.docCount += 1

    def removeDoc(self):
        currentDocs = self.doctors.copy()
        for doc in self.findChildren(QLabel):
            if (doc.text()+"\n") in self.doctors:
                currentDocs.remove((doc.text()+"\n"))

        self.doctors.remove(currentDocs[0])

        f = open("data/doctors.txt", "w")
        f.writelines(self.doctors)
        f.close()



class DoctorItem(QWidget):
    def __init__(self, name):
        super(DoctorItem, self).__init__()

        self.layout = QHBoxLayout()
        self.nameLabel = QLabel(name)
        self.layout.addWidget(self.nameLabel)
        self.removeButton = QPushButton("Remove")
        self.layout.addWidget(self.removeButton)

        self.setLayout(self.layout)