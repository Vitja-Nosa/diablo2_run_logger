from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from dialogs.Notfound import Notfound 

class Find(QDialog):
    def __init__(self, window):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)   
        loadUi('./uis/find.ui', self)

        self.win = window

        self.table_map = []
        self.map_pos = -1 

        self.nextBtn.clicked.connect(self.following)
        self.prevBtn.clicked.connect(self.previous)

    def following(self):
        if self.map_pos < len(self.table_map)-1:
            self.map_pos += 1
        else:
            self.map_pos = 0
        query = self.queryInput.text().strip()
        data = self.win.tableToObj()
        self.table_map = self.searchTable(data, query)

        if len(self.table_map) > 0:
            row = self.table_map[self.map_pos][0]
            col = self.table_map[self.map_pos][1]
            item = self.win.tableWidget.item(row, col)
            self.win.tableWidget.setCurrentItem(item)

    def previous(self):
        if self.map_pos > 0:
            self.map_pos -= 1
        else:
            self.map_pos = len(self.table_map)-1
        query = self.queryInput.text().strip()
        data = self.win.tableToObj()
        self.table_map = self.searchTable(data, query)

        if len(self.table_map) > 0:
            row = self.table_map[self.map_pos][0]
            col = self.table_map[self.map_pos][1]
            item = self.win.tableWidget.item(row, col)
            self.win.tableWidget.setCurrentItem(item)
        

    def searchTable(self, data, query):
        table_map = []
        for index, dictionary in enumerate(data):
            dict_values = dictionary.values()
            for j, value in enumerate(dict_values): 
                value = value.strip()
                if query == value:
                    table_map.append([index, j]) 
        if len(table_map) == 0:
            self.notfound()
        return table_map
    
    def notfound(self):
        dialog = Notfound(self.win)
        dialog.exec_()