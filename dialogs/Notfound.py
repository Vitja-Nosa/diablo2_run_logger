from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import sys

class Notfound(QDialog):
    def __init__(self, window):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)   
        loadUi('./uis/notfound.ui', self)

        self.win = window

        self.okBtn.clicked.connect(self.closeDialog)
    
    def closeDialog(self):
        self.close()