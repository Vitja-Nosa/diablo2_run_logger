from tinydb import TinyDB
from tinydb import Query
import re
from datetime import datetime

class Database(TinyDB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.COLS = ['date', 'runName', 'itemName', 'soldFor']
        self.protoDB = self.all()

    def DbSearch(self, query):
        Table = Query()
        results = self.search(Table.date.matches(query, flags=re.IGNORECASE))
        results += self.search(Table.runName.matches(query, flags=re.IGNORECASE)) 
        results += self.search(Table.itemName.matches(query, flags=re.IGNORECASE)) 
        results += self.search(Table.soldFor.matches(query, flags=re.IGNORECASE))
        return results

    #this function get called whenever tableWidget item gets changed
    def updateItem(self, item):
        print('updating item')
        # doc_id begins at 1 and not 0 so I +1
        id = item.row()+1
        new_value = item.text()
        self.update({self.COLS[item.column()]: new_value} ,doc_ids=[id])
        return new_value

    def createRow(self, runName, itemName, soldFor):
        date = datetime.now()    
        date = date.strftime('%d/%m/%Y %H:%M')

        row = {
            "date": date,
            "runName": runName, 
            "itemName": itemName,
            "soldFor": soldFor
        }
        self.insert(row)

    def deleteRows(self):
        print('test')