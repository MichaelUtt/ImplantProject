from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

class HelpPage(QWidget):

    def __init__(self):
        super(HelpPage, self).__init__()
        uic.loadUi('ui/help.ui', self)

        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon('data/favicon.ico'))

        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )










