import datetime

from PyQt5.QtCore import QDateTime, Qt, QTimer, QDate, QSize
from PyQt5.QtGui import QFont, QMouseEvent, QPixmap, QIcon, QColor
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

        self.searchBar = self.findChild(QLineEdit, "searchBar")
        self.searchBar.returnPressed.connect(self.searchTable)
        self.table = self.findChild(QTableWidget, "reportsTable")

    def searchTable(self):
        pass

    def generateTable(self):
        with open("data/fileLocations.txt", "r") as content:
            lines = content.readlines()
        excelFile = lines[2][6:].strip()
        df = pd.read_excel(excelFile)
        if df.size == 0:
            print("NO file")
            return

        df = df.iloc[5:, :7]
        df.drop([df.columns[5], df.columns[1]], 1, inplace=True)

        df.columns = ["Patient", "Chart", "ImplantDate", "DueForUncover", "Details"]

        df.replace("", float("NaN"), inplace=True)
        df.dropna(subset=["ImplantDate"], inplace=True)
        df["Patient"].fillna(method='ffill', inplace=True)
        df["Chart"].fillna(method='ffill', inplace=True)
        df.replace(float("NaN"), "", inplace=True)

        #print(df.info())
        df["ImplantDate"] = pd.to_datetime(df["ImplantDate"], format="%Y/%m/%d", errors='coerce')
        #print(pd.to_datetime(df["Implant Date"], format="%Y/%m/%d", errors='raise'))
        #print(df.info())
        #print(type(df.ImplantDate))
        print("=======")
        df = df.sort_values(by=["ImplantDate","Patient"], ascending=(False, True))
        #df.sort_values(by="ImplantDate", inplace=True, ascending=True)

        self.createTable(df)

    def createTable(self, data):
        self.table.setRowCount(data.shape[0])
        headers = ["File", "Patient", "Chart", "Implant Date", "Due For Uncover", "Details"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # returns pandas array object
        i = 0
        for row in data.iterrows():
            values = row[1]

            for col_index, value in enumerate(values):

                if isinstance(value, datetime.datetime):
                    try:

                        value = value.strftime("%Y-%m-%d")
                    except:
                        continue
                tableItem = QTableWidgetItem(str(value))

                if str(value) == "":
                    tableItem.setBackground(QColor(220, 220, 220, 255))
                self.table.setItem(i, col_index+1, tableItem)
            i += 1

        self.addFileButtons()
        self.table.resizeColumnsToContents()

    def addFileButtons(self):
        pass