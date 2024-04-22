from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.uic import loadUi
import sys

class Save(QDialog):
    def __init__(self, window):
        super().__init__()
        loadUi('./uis/save.ui', self) 

        self.win = window 
        saveButton = self.buttonBox.button(QDialogButtonBox.Save)
        discardButton = self.buttonBox.button(QDialogButtonBox.Discard)
        cancelButton = self.buttonBox.button(QDialogButtonBox.Cancel)

        saveButton.clicked.connect(self.save)
        discardButton.clicked.connect(self.discard)
        cancelButton.clicked.connect(self.cancel)
        
    def save(self):
        self.win.saveTable()
        self.close()
        self.win.destroy() 
        sys.exit()

    def discard(self):
        self.close()
        self.win.destroy()
        sys.exit()

    def cancel(self):
        self.close() 