from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QFont, QMouseEvent, QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QInputDialog, QMessageBox, QDateEdit, QFileDialog)
from application.pages import createReport


class HomePage(QDialog):
    def __init__(self, resolution, parent=None):
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
        # hbox.addStretch(1)

        hbox.addWidget(self.createButton)

        # hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        # vbox.addStretch(1)
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