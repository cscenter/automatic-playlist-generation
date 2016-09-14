import json
import time
import urllib.request
from urllib.parse import quote

import pylast

LAST_FM_USER = ""
LAST_FM_PASSWORD = ""
LAST_FM_API_KEY = ""
LAST_FM_API_SECRET = ""

username = LAST_FM_USER
password_hash = pylast.md5(LAST_FM_PASSWORD)
network = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY, api_secret=LAST_FM_API_SECRET, username=username,
                               password_hash=password_hash)

path_before_artist = 'http://ws.audioscrobbler.com/2.0/?method=artist.getcorrection&artist='

path_after_artist = '&api_key=API_KEY&format=json'

path_track_1 = 'http://ws.audioscrobbler.com/2.0/?method=track.getcorrection&artist='

path_track_2 = '&track='

path_track_3 = '&api_key=API_KEY&format=json'


# def intersect_tags(artist_1, artist_2):

def intersect_tags(artist_1, artist_2):
    artist_1_corr = correct_artist(artist_1)

    artist_2_corr = correct_artist(artist_2)

    tags_1 = artist_tags(artist_1_corr)

    tags_2 = artist_tags(artist_2_corr)


    tags = []
    tags.append(tags_1.keys())
    tags.append(tags_2.keys())

    print(tags)





def correct_artist(artist):
    tmp_json = 'tmp_track.json'

    url_artist = path_before_artist + quote(artist) + path_after_artist

    try:

        urllib.request.urlretrieve(url_artist, tmp_json)

        with open(tmp_json) as corr_json:
            corr = json.load(corr_json)

        corr_data = corr['corrections']['correction']['artist']

        if 'name' in corr_data:
            artist_corr = corr_data['name']

        corr_json.close()


    except:
        print("error for:", artist)

        time.sleep(0.25)

    return artist_corr


def correct_title(artist, title):
    tmp_json = 'tmp_track.json'

    url_name = path_track_1 + quote(artist) + path_track_2 + quote(title) + path_track_3

    try:

        urllib.request.urlretrieve(url_name, tmp_json)

        with open(tmp_json) as corr_json:
            corr = json.load(corr_json)

            corr_data = corr['corrections']['correction']['track']

            if 'name' in corr_data:
                title_corr = corr_data['name']

            corr_json.close()
    except:
        print("error for:", artist, "-", title)

    time.sleep(0.25)


    return title_corr


def artist_tags(artist):
    tag_dict = {}

    try:
        artist_data = network.get_artist(artist)
        tag = [t[0].get_name() for t in artist_data.get_top_tags()]
        cnt = [t[1] for t in artist_data.get_top_tags()]
        tag_dict = dict(zip(tag, cnt))
    except:
        print("No tags for artist:", artist)

    time.sleep(0.25)

    return tag_dict


def track_tags(artist, title):
    tag_dict = {}

    try:
        track_data = network.get_track(artist, title)
        tag = [t[0].get_name() for t in track_data.get_top_tags()]
        cnt = [t[1] for t in track_data.get_top_tags()]
        tag_dict = dict(zip(tag, cnt))
    except:
        print("No tags for track:", artist, "-", title)

    time.sleep(0.25)

    return tag_dict
