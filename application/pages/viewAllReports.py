import datetime
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTableWidget, QWidget, QTableWidgetItem
from PyQt5 import uic
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
            Qt.WindowCloseButtonHint
        )

        self.searchBar = self.findChild(QLineEdit, "searchBar")
        self.searchBar.returnPressed.connect(self.searchTable)
        self.table = self.findChild(QTableWidget, "reportsTable")
        # self.table = QTableWidget()



        # self.searchBar.editingFinished.connect(self.searchTable)

    def searchTable(self):
        searchText = self.searchBar.text()
        # print(searchText)
        if searchText == "":
            self.table.setSortingEnabled(True)
            self.table.sortItems(3, Qt.DescendingOrder)
            return

        self.table.setSortingEnabled(False)

        foundRows = self.searchByCol(searchText, 1)
        foundRows.extend(self.searchByCol(searchText, 2))
        foundRows.extend(self.searchByCol(searchText, 3))
        foundRows.extend(self.searchByCol(searchText, 4))

        # print(self.table.rowCount())
        #print(foundRows)
        colCount = self.table.columnCount()
        addedRows = len(foundRows)
        currentRow = 0
        for row in foundRows:
            self.table.insertRow(0)
        for row in foundRows:
            buttonItem = self.table.cellWidget(row + addedRows, 0)
            if buttonItem != None:
                self.placeButton(currentRow, buttonItem.filePath)
            for col in range(1, colCount):
                cellItem = self.table.takeItem(row+addedRows, col)
                if cellItem != None:
                    # print(cellItem.text())
                    newItem = QTableWidgetItem(cellItem.text())
                    self.table.setItem(currentRow, col, newItem)
            currentRow += 1

        for row in reversed(sorted(foundRows)):
            self.table.removeRow(row+addedRows)
        # print(self.table.rowCount())

    def searchByCol(self, lookingFor, col):
        rowCount = self.table.rowCount()

        foundRows = []
        for rowNum in range(rowCount):
            try:
                data = self.table.item(rowNum, col).text()
            except:
                continue

            #print(data)
            if lookingFor.lower() in str(data).lower():
                if rowNum not in foundRows:
                    foundRows.append(rowNum)
                    #print(str(data))
        return foundRows


    def generateTable(self):
        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\fileLocations.txt')
        with open(path_to_dat, "r") as content:
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

        df["ImplantDate"] = pd.to_datetime(df["ImplantDate"], infer_datetime_format=True, format="%Y/%m/%d", errors='coerce')

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
        self.table.setColumnWidth(2, 60)
        self.table.setColumnWidth(0, 6)
        self.table.setSortingEnabled(True)
        self.table.sortItems(3, Qt.DescendingOrder)

    def addFileButtons(self):

        bundle_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        path_to_dat = os.path.join(bundle_dir, 'data\\fileLocations.txt')
        with open(path_to_dat, "r") as content:
            lines = content.readlines()
        reportsDir = lines[0][8:].strip()
        if len(reportsDir) < 3:
            return

        reportFilePaths = []
        reportFileNames = []
        for file in os.scandir(reportsDir):
            if file.path.endswith(".docx") and file.is_file():
                #print(file.path)
                reportFilePaths.append(file.path)
                reportFileNames.append(os.path.split(file.path)[1])

        rowCount = self.table.rowCount()

        for row in range(rowCount):

            try:
                patientLF = self.table.item(row, 1).text()
                date = self.table.item(row, 3).text()

                patientLF = str(patientLF).split(",")
                patientLast = patientLF[0].strip()
                patientFirst = patientLF[1].strip()
                dateParts = str(date).split("-")
                if len(dateParts) != 3:
                    continue
                dateStr = dateParts[0].strip()+"_"+dateParts[1].strip()+"_"+dateParts[2].strip()

                fileName = patientLast+"_"+patientFirst+"_"+dateStr
                fileName = fileName.upper()
                fileName = fileName+".docx"

                # print(fileName)
            except:
                continue
            for i, reportFileName in list(enumerate(reportFileNames)):
                if fileName in reportFileName:
                    # print(fileName, row)
                    self.placeButton(row, reportFilePaths[i])

    def placeButton(self, row, filePath):
        fileBtn = QPushButton('W')
        fileBtn.setStyleSheet("background-color: rgb(26, 115, 232);font: bold 12pt 'Arial';color: white;")
        fileBtn.clicked.connect(self.openDocument)

        fileBtn.filePath = filePath
        self.table.setCellWidget(row, 0, fileBtn)

    def openDocument(self):
        # print("open document")
        sender = self.sender()
        # print(sender)
        path = sender.filePath
        # print(path)

        os.startfile(path)


