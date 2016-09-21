import pylast
import time
import urllib.request
from urllib.parse import quote


LAST_FM_USER = ""
LAST_FM_PASSWORD = ""
LAST_FM_API_KEY = ""
LAST_FM_API_SECRET = ""

username = LAST_FM_USER
password_hash = pylast.md5(LAST_FM_PASSWORD)
network = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY, api_secret=LAST_FM_API_SECRET, username=username, password_hash=password_hash)



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
