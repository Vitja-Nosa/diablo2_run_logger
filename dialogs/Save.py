from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.uic import loadUi

class Save(QDialog):
    def __init__(self, window):
        super().__init__()
        loadUi('./uis/save.ui', self) 

        self.window = window 
        saveButton = self.buttonBox.button(QDialogButtonBox.Save)
        discardButton = self.buttonBox.button(QDialogButtonBox.Discard)
        cancelButton = self.buttonBox.button(QDialogButtonBox.Cancel)

        saveButton.clicked.connect(self.save)
        discardButton.clicked.connect(self.discard)
        cancelButton.clicked.connect(self.cancel)
        
    def save(self):
        self.window.saveTable()
        self.close()
        self.window.close() 

    def discard(self):
        self.close()
        self.window.close()

    def cancel(self):
        print('cancel')
        self.close() 