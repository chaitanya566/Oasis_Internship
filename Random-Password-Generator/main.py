import os
import sys

from src.ui_RRG import *

from PyQt5.QtWidgets import QApplication, QMainWindow

from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/style.json"
            }) 
        self.show() 

        QAppSettings.updateAppSettings(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setMinimumSize(1200, 850)
    window.show()
    sys.exit(app.exec_())
