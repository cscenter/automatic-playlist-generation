import json
import os
from mutagen.id3 import ID3, MutagenError
from pymongo import MongoClient


class AbstractDataProvider:
    def get_all(self):
        assert False

    def save_data(self):
        assert False

    def get_by_id(self, song_id):
        assert False


class HardDriveProvider(AbstractDataProvider):
    def __init__(self, p, force_upd=False):
        self.path = p
        self.force_update = force_upd

        self.data = {}
        if os.path.exists(self._get_data_file_path()):
            with open(self._get_data_file_path()) as r:
                self.data = json.load(r)
        if self.data and not self.force_update:
            return
        for root, _, files in os.walk(self.path):
            for filepath in files:
                file_path = os.path.join(root, filepath)
                if not self.filter_mp3(file_path) or file_path in self.data:
                    continue
                file_json = {'path': file_path}
                self.data[file_path] = file_json

    def _get_data_file_path(self):
        return os.path.join(self.path, '{}.json'.format(
            os.path.basename(os.path.normpath(self.path))))

    @staticmethod
    def filter_mp3(file_path):
        file_name, _ = os.path.splitext(file_path)
        if file_name.find('\\._') >= 0:
            return False
        try:
            _ = ID3(file_path)
        except MutagenError as e:
            return False
        except FileNotFoundError:
            pass
        else:
            return True

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
