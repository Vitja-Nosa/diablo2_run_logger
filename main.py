from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
from datetime import datetime
from Database import Database
import sys

db = Database('db.json')

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("designer.ui", self)
        self.loadData()    
        #events for elements
        self.tableWidget.installEventFilter(self)
        self.addLogBtn.clicked.connect(self.addLog)
        self.tableWidget.itemChanged.connect(db.updateItem)  
        # rowsRemoved.connect(self.rows_removed) this is a listener for when a row is removed

    def addLog(self):
        next_row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(next_row)

        date = datetime.now()    
        date = date.strftime('%d/%m/%Y %H:%M')
        values = [date, self.runNameEl.text(), self.itemNameEl.text(), self.soldForEl.text()]

        row = {}
        if len(values) != len(db.COLS):
            return False
        for i, col in enumerate(db.COLS): 
            row[col] = values[i] 
        db.insert(row)

        for col, value in enumerate(values):
            item = QTableWidgetItem(value)
            self.tableWidget.setItem(next_row, col, item)
    
    def loadData(self, search = None):
        if search is not None:
            results = db.DbSearch(search)
        else:
            results = db.all()    

        self.tableWidget.setRowCount(len(results))
        i = 0
        for row in results:
            date = QtWidgets.QTableWidgetItem(row["date"])
            date.setFlags(date.flags() ^ Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 0, date)
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row["runName"]))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(row["itemName"]))
            self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(row["soldFor"]))
            i += 1
    
    def eventFilter(self, obj, event):
        if obj == self.tableWidget and event.type() == QEvent.KeyPress:
            key = event.key()
            # delete key: 16777223
            if key == 16777223:
                items = self.tableWidget.selectedIndexes()
                if len(items) > 0:
                    map = {}
                    for item in items:
                        row = item.row()
                        col = item.column()
                        if row not in map:
                            map[row] = []
                        map[row].append(col)
                    map = {k: map[k] for k in sorted(map, reverse=True)}
                    for key in map:
                        if len(map[key]) == len(db.COLS):
                            #delete the entire row
                            self.tableWidget.removeRow(key)
                            print(key)    
                            db.remove(doc_ids=[3])
                        else:
                            #empty item
                            for col in map[key]:
                                if db.COLS[col] != 'date':
                                    new_item = QtWidgets.QTableWidgetItem('')
                                    self.tableWidget.setItem(key, col, new_item)

                    print(map)            

                #delete rows here
            return True

        return super().eventFilter(obj, event)

app = QApplication(sys.argv)
window = Window()

widget = QtWidgets.QStackedWidget() 
widget.addWidget(window)
widget.setFixedHeight(400)
widget.setFixedWidth(1000)
widget.show()

app.exec_()