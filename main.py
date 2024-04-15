import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow 
from PyQt5.uic import loadUi
import csv
from datetime import datetime

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("designer.ui", self)
        self.loadData()    
        #events for elements
        self.tableWidget.installEventFilter(self)
        self.addLogBtn.clicked.connect(self.addLog)
    
    def addLog(self):
        self.createRow(
            self.runNumbEl.text(),
            self.runNameEl.text(),
            self.itemNameEl.text(),
            self.soldForEl.text()
        )
        self.loadData()
    
    def loadData(self):
        with open("data.csv", "r") as file:
            table = csv.reader(file)
            table = list(table)
            table.reverse()
            self.tableWidget.setRowCount(len(table))
            i = 0
            for row in table:
                date = QtWidgets.QTableWidgetItem(row[0])
                date.setFlags(date.flags() ^ Qt.ItemIsEditable)
                self.tableWidget.setItem(i, 0, date)
                self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(row[4]))
                i += 1
    
    def createRow(self, runNumb, runName, itemName, soldFor):
        date = datetime.now()    
        date = date.strftime('%d/%m/%Y %H:%M')
        row = [date, runNumb, runName, itemName, soldFor]
        with open("data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
    
    def eventFilter(self, obj, event):
        if obj == self.tableWidget and event.type() == QEvent.KeyPress:
            key = event.key()
            print(key)
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