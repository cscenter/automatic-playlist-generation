import json
import urllib.request
import time
import os
from urllib.parse import quote
import fileinput

path = '/mnt/hdd3/small/'    # директория, соотв-ая набору плейлистов

API_KEY = ''


def artist_tags(artist):
    subdir = path + 'artist_tags/'

    if not os.path.exists(subdir):
        os.makedirs(subdir)

    json_out = subdir + artist + ".json"
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=' + quote(artist) + \
          '&api_key=' + API_KEY + '&format=json'

    try:
         urllib.request.urlretrieve(url, json_out)
    except:
        print("No artist tags for:", artist)

    time.sleep(0.2)
    return



def track_tags(artist, title):
    subdir = path + 'track_tags/'

    if not os.path.exists(subdir):
        os.makedirs(subdir)

    json_out = subdir + artist + " - " + title + ".json"
    url = 'http://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist=' + quote(artist) + \
          '&track=' + quote(title) + '&api_key=' + API_KEY + '&format=json'
    try:
         urllib.request.urlretrieve(url, json_out)
    except:
        print("No track tags for track:", artist, "-", title)

    time.sleep(0.2)
    return



def artist_similar(artist):
    subdir = path + 'artist_similar/'

    if not os.path.exists(subdir):
        os.makedirs(subdir)

    json_out = subdir + artist + ".json"
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=' + quote(artist) + \
          '&api_key=' + API_KEY + '&format=json'

    try:
         urllib.request.urlretrieve(url, json_out)
    except:
        print("No similar artist for:", artist)

    time.sleep(0.2)
    return


def track_similar(artist, title):
    subdir = path + 'track_similar/'

    if not os.path.exists(subdir):
        os.makedirs(subdir)

    json_out = subdir + artist + " - " + title + ".json"
    url = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist=' + quote(artist) + \
          '&track=' + quote(title) + '&api_key=' + API_KEY + '&format=json'
    try:
         urllib.request.urlretrieve(url, json_out)
    except:
        print("No similar tracks for:", artist, '-', title)

    time.sleep(0.2)
    return


def artist_tracks(artist):
    subdir = path + 'artist_tracks/'

    if not os.path.exists(subdir):
        os.makedirs(subdir)

    json_out = subdir + artist + ".json"
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=' + quote(artist) + \
          '&api_key=' + API_KEY + '&format=json'

    try:
         urllib.request.urlretrieve(url, json_out)
    except:
        print("No tracks for:", artist)

    time.sleep(0.2)
    return



path_in = 'small_lines.txt'     # каждая строка -- словарь вида ARTIST: [TRACK1, TRACK2, ...]

with fileinput.input(files = path_in) as f:
    for line in f:
        print(fileinput.lineno())

        line_dict = json.loads(line)

        artist = list(line_dict.keys())[0]

        artist_tags(artist)
        artist_similar(artist)
        artist_tracks(artist)

        tracks = line_dict[artist]

        for title in tracks:
            track_tags(artist, title)
            track_similar(artist, title)

