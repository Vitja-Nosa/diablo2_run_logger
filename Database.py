from tinydb import TinyDB
from tinydb import Query
import re
from datetime import datetime

class Database(TinyDB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.COLS = ['date', 'runName', 'itemName', 'soldFor']
        self.changes = False

    def DbSearch(self, query):
        Table = Query()
        results = self.search(Table.date.matches(query, flags=re.IGNORECASE))
        results += self.search(Table.runName.matches(query, flags=re.IGNORECASE)) 
        results += self.search(Table.itemName.matches(query, flags=re.IGNORECASE)) 
        results += self.search(Table.soldFor.matches(query, flags=re.IGNORECASE))
        return results

    def DbSave(self, data):
        self.changes = False
        self.truncate()
        self.insert_multiple(data)