from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QTableWidgetItem, QAction
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

        #shortcuts
        save_action = QAction('Shortcut', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.saveTable)

    def addLog(self):
        next_row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(next_row)

        date = datetime.now()    
        date = date.strftime('%d/%m/%Y %H:%M')
        values = [date, self.runNameEl.text(), self.itemNameEl.text(), self.soldForEl.text()]

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

    def tableToObj(self):
        data = []
        row_count = self.tableWidget.rowCount()
        for row in range(row_count):
            rowData = {}
            for i, col in enumerate(db.COLS):
                item = self.tableWidget.item(row, i)
                rowData[col] = item.text()
            data.append(rowData)
        return data
    
    def saveTable(self):
        data = self.tableToObj
        db.DbSave(data)

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
                        else:
                            #empty item
                            for col in map[key]:
                                if db.COLS[col] != 'date':
                                    new_item = QtWidgets.QTableWidgetItem('')
                                    self.tableWidget.setItem(key, col, new_item)
            elif key == 83:
                data = self.tableToObj()
                db.DbSave(data)
                print('data saved')
            return True

        def closeEvent(self, event):
            print('hello')
            event.ignore()

        return super().eventFilter(obj, event)

app = QApplication(sys.argv)
window = Window()

widget = QtWidgets.QStackedWidget() 
widget.setWindowTitle('Runner Log')
widget.addWidget(window)
widget.setFixedHeight(400)
widget.setFixedWidth(1000)
widget.show()

app.exec_()