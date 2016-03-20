import json
import os

from pymongo import MongoClient


class AbstractDataProvider:
    def get_all(self):
        assert False

    def save_data(self):
        assert False

    def get_by_id(self, song_id):
        assert False


class HardDriveProvider(AbstractDataProvider):
    def __init__(self, p):
        self.path = p
        if os.path.exists(self._get_data_file_path()):
            self.data = json.load(self._get_data_file_path())
        else:
            self.data = {}
            for root, _, files in os.walk(self.path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    file_json = {'path': file_path}
                    self.data[file_path] = file_json

    def _get_data_file_path(self):
        return os.path.join(self.path, 'data.json')

    def get_all(self):
        return self.data

    def save_data(self):
        with open(self._get_data_file_path(), 'w') as writer:
            writer.write(json.dumps(self.data))

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

    def save_data(self):
        pass

    def get_by_id(self, song_id):
        pass
