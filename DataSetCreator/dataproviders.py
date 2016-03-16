import json
import os

from pymongo import MongoClient


class AbstractDataProvider:
    def get_all(self):
        assert False

    def save_data(self, json_data):
        assert False

    def get_by_id(self, song_id):
        assert False


class HardDriveProvider(AbstractDataProvider):
    def __init__(self, p):
        self.path = p
        self.data = {}

    def get_all(self):
        for root, _, files in os.walk(self.path):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_json = {}
                self.data[file_path] = json.dumps(file_json)
        return json.dumps(self.data)

    def save_data(self, json_data):
        pass

    def get_by_id(self, song_path):
        return self.data.get(song_path, None)


class MongoDBProvider(AbstractDataProvider):
    def get_all(self):
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

    def save_data(self, json_data):
        pass

    def get_by_id(self, song_id):
        pass
