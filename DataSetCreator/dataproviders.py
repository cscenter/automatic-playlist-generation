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
            with open(self._get_data_file_path()) as r:
                self.data = json.load(r)
        else:
            self.data = {}
            for root, _, files in os.walk(self.path):
                for filepath in filter(self.filter_mp3, files):
                    file_path = os.path.join(root, filepath)
                    file_json = {'path': file_path}
                    self.data[file_path] = file_json

    def _get_data_file_path(self):
        return os.path.join(self.path, '{}.json'.format(
            os.path.basename(os.path.normpath(self.path))))

    @staticmethod
    def filter_mp3(filepath):
        _, file_extension = os.path.splitext(filepath)
        return 'mp3' in file_extension

    def get_all(self):
        return dict((k, v) for k, v in self.data.items()
                    if self.filter_mp3(k))

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
