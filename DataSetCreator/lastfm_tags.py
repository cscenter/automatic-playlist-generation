import pylast
import json
import time
import math
import urllib.request

LAST_FM_USER = ""
LAST_FM_PASSWORD = ""
LAST_FM_API_KEY = ""
LAST_FM_API_SECRET = ""

username = LAST_FM_USER
password_hash = pylast.md5(LAST_FM_PASSWORD)
network = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY, api_secret=LAST_FM_API_SECRET, username=username,
                               password_hash=password_hash)


def track_tags(artist, title):
    tag_dict = {}

    try:
        track_data = network.get_track(artist, title)
        tag = [t[0].get_name() for t in track_data.get_top_tags()]
        cnt = [int(t[1]) for t in track_data.get_top_tags()]
        tag_dict = dict(zip(tag, cnt))
    except:
        print("No tags for track:", artist, "-", title)

    time.sleep(0.201)

    return tag_dict



def artist_tags(artist):

    tag_dict = {}

    try:
        artist_data = network.get_artist(artist)
        tag = [t[0].get_name() for t in artist_data.get_top_tags()]
        cnt = [int(t[1]) for t in artist_data.get_top_tags()]
        tag_dict = dict(zip(tag, cnt))
    except:
        print("No tags for", artist)

    time.sleep(0.201)

    return tag_dict



def track_similar(artist, title):

    track_dicts = []

    try:
        track_data = network.get_track(artist, title)
        track_list = track_data.get_similar()

        for track in track_list:
            tmp_dict = {}
            artist_s = str(track[0].get_artist())
            title_s = track[0].get_name()
            match = track[1]
            tmp_dict["artist"] = artist_s
            tmp_dict["title"] = title_s
            tmp_dict["match"] = match
            track_dicts.append(tmp_dict)

    except:
        print("No similar for track:", artist, "-", title)

    time.sleep(0.201)
    return track_dicts



def artist_similar(artist):

    artist_dict = {}

    try:
        artist_data = network.get_artist(artist)
        artist_list = artist_data.get_similar()

        for name in artist_list:
            artist_s = name[0].get_name()
            match = name[1]
            artist_dict[artist_s] = match


    except:
        print("No similar for:", artist)

    time.sleep(0.1)
    return artist_dict




def track_popularity(artist):

    tracks = []
    tracks_pop = {}

    try:
        artist_data = network.get_artist(artist)
        artist_top = artist_data.get_top_tracks()

        l_t = len(artist_top)

        for i in range(l_t):
            track = artist_top[i][0]
            tracks.append(track.get_name())

    except:
        print("No top tracks for:", artist)

    l_t = len(tracks)

    for i in range(l_t):
        tracks_pop[tracks[i]] = math.exp(-i/10.0)

    return tracks_pop


for i in range(15):
    print(math.exp(-i/10.0))
