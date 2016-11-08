import spotipy
import sys
import spotipy.util as util
import json
import time


SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'
SPOTIPY_USERNAME = ''


token = util.prompt_for_user_token(username = SPOTIPY_USERNAME, client_id=SPOTIPY_CLIENT_ID,
                                   client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)


sp = spotipy.Spotify(auth=token)


def get_id(artist, title):

    artist = artist.lower()
    title = title.lower()

    query = artist + " " + title

    search_song = sp.search(q = query, type="track")

    items = search_song["tracks"]["items"]          # массив треков

    l = len(items)

    ids = []

    for i in range(l):
        if (items[i]["name"].lower() == title):     # название трека
            artists = items[i]["artists"]           # массив исполнителей
            if (artists[0]["name"].lower() == artist):
                ids.append(items[i]["id"])

    time.sleep(0.2)

    return ids


def audio_feautures(id_list, file_out):

    features = sp.audio_features(id_list)

    with open(file_out, 'w') as f_out:
        json.dump(features, f_out)

    return





