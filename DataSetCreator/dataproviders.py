from pymongo import MongoClient


class AbstractDataProvider:
    def save_data(self, json):
        assert False

    def get_by_id(self, song_id):
        assert False


class HardDriveProvider(AbstractDataProvider):
    def save_data(self, json):
        pass

    def get_by_id(self, song_id):
        pass


class MongoDBProvider(AbstractDataProvider):
    def save_data(self, json):
        pass

    def get_by_id(self, song_id):
        pass

"""
Copy-paste example from here
https://analytiksblog.wordpress.com/2014/12/25/mongodb-installation-on-windows-and-access-through-pycharm-python/
"""
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
