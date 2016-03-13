'''
Copy-paste example from here
https://analytiksblog.wordpress.com/2014/12/25/mongodb-installation-on-windows-and-access-through-pycharm-python/
'''

from pymongo import MongoClient

connection = MongoClient()
db = connection.test
collection = db.collect
age = 30
entry = {"Name": "Ralph",
         "Address": "16, Av Foch",
         "Age in Years": age}
collection.insert(entry)
print(list(collection.find()))
connection.close()