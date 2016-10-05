from correction import *
from lastfm_tags import *



class Track(object):

    def __init__(self, artist, title):
        self.artist = artist
        self.title = title


    def correction(self):
        self.artist = correct_artist(self.artist)
        # artist уже поменялся или по выходу только?
        self.title = correct_title(self.title)


# как-то надо добавлять теги из разных источников:
# artistTag, trackTag с lastfm,
# список SimilarTracks
# теги других сайтов



# несколько экземпляров класса Track -- это плейлист
    


class Metric(object):

    # это должны быть экземпляры класса Track
    def __init__(self, track1, track2):
        self.track1 = track1
        self.track2 = track2


    def score(self):
        # перечислить все какие есть, на каждую своя функция?

    def calc_all(self, playlist):

        # среднее попарных расстояний для плейлиста. как передавать плейлист?



class MetricBuilder(object):

    # список используемых метрик
    
    def __init__(self):
        self = []

    def add_metric(self, name, func):
        # некоторый append

    def score_all(self):
        # возможно, посчитать calc_all для всех метрик. как-то его обработать к одному числу и выдать
