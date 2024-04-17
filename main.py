import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow 
from PyQt5.uic import loadUi
from datetime import datetime
from tinydb import TinyDB
from tinydb import Query
import re

db = TinyDB('db.json')

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("designer.ui", self)
        self.loadData()    
        #events for elements
        self.tableWidget.installEventFilter(self)
        self.addLogBtn.clicked.connect(self.addLog)
        self.tableWidget.itemChanged.connect(self.updateItem)  
        # rowsRemoved.connect(self.rows_removed) this is a listener for when a row is removed
    def addLog(self):
        self.createRow(
            self.runNameEl.text(),
            self.itemNameEl.text(),
            self.soldForEl.text()
        )
        self.loadData() #TODO: eeew reloading the entire dataset after add 1 log LMAO
    
    # this function get called whenever you update a cell also when creating row
    def updateItem(self, item): 
        id = item.row()+1

        columns = list(db.get(doc_id=id).keys())
        new_value = item.text()
        db.update({columns[item.column()]: new_value} ,doc_ids=[id])

    def loadData(self, search = None):
        if search is not None:
            Table = Query()
            results = db.search(Table.date.matches(search, flags=re.IGNORECASE))
            results += db.search(Table.runName.matches(search, flags=re.IGNORECASE)) 
            results += db.search(Table.itemName.matches(search, flags=re.IGNORECASE)) 
            results += db.search(Table.soldFor.matches(search, flags=re.IGNORECASE)) 
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

    def createRow(self, runName, itemName, soldFor):
        print('item changed')
        date = datetime.now()    
        date = date.strftime('%d/%m/%Y %H:%M')

        row = {
            "date": date,
            "runName": runName, 
            "itemName": itemName,
            "soldFor": soldFor
        }
        db.insert(row)
    
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

                    for key in map:
                        if len(map[key]) == 4:
                            print('print this 4 times')
                            self.tableWidget.removeRow(key)    
                            #delete the entire row
                            #TODO: order list than you can decrement and remove rows
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