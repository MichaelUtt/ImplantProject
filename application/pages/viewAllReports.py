from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate, QSize
from PyQt5.QtGui import QFont, QMouseEvent, QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QInputDialog, QMessageBox, QDateEdit, QFileDialog, QScrollArea,
                             QMainWindow, QTreeView, QTableWidgetItem)
from PyQt5.Qt import QStandardItemModel, QStandardItem
from application.pages import home
from mailmerge import MailMerge
from PyQt5 import uic
import json
import pandas as pd

class ViewPage(QWidget):
    def __init__(self):
        super(ViewPage, self).__init__()
        uic.loadUi('ui/viewReports.ui', self)

        self.setWindowTitle("View Reports")
        self.setWindowIcon(QIcon('data/favicon.ico'))

        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint
        )

    def generateTable(self):


        df = pd.read_excel("data/IMPLANTS-DR. DAVID.xlsx")
        if df.size == 0:
            print("NO file")
            return

        df = df.iloc[5: , 1: ]
        df.fillna('', inplace=True)
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        #
        # # returns pandas array object
        # for row in df.iterrows():
        #     values = row[1]
        #     for col_index, value in enumerate(values):
        #         if isinstance(value, (float, int)):
        #             value = '{0:0,.0f}'.format(value)
        #         tableItem = QTableWidgetItem(str(value))
        #         self.table.setItem(row[0], col_index, tableItem)
        #
        # self.table.setColumnWidth(2, 300)
