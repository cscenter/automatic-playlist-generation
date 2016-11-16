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

path = "jazz/"

def get_playlist_tracks(user_id, playlist_id):           # треки из плейлиста по его номеру

    playlist_dict = {}

    playlist = sp.user_playlist(user_id, playlist_id)
    playlist_dict["playlist_id"] = playlist["id"]
    playlist_dict["playlist_descr"] = playlist["description"]
    playlist_dict["playlist_name"] = playlist["name"]

    items = playlist["tracks"]["items"]

    l_i = len(items)

    tracks = []

    for i in range(l_i):
        tmp_dict = {}

        tmp_dict["track_id"] = items[i]["track"]["id"]
        tmp_dict["track_title"] = items[i]["track"]["name"]
        tmp_dict["track_artist"] = items[i]["track"]["artists"][0]["name"]

        tracks.append(tmp_dict)


    playlist_dict["tracks"] = tracks

    file_out = path + playlist_id + ".json"

    with open(file_out, 'w') as tmp_out:
        json.dump(playlist_dict, tmp_out)

    time.sleep(0.2)

    return playlist_dict




def get_playlists_ids(file_input):           # id и владелец плейлистов из файла выдачи по категории или ключевому слову

    playlists = []
    data_pl = json.load(open(file_input))
    items = data_pl["playlists"]["items"]

    l_i = len(items)

    for i in range(l_i):
        playlists.append([items[i]["owner"]["id"], items[i]["id"]])

    return playlists



def get_playlists_by_query(query):       # id и владелец плейлистов по запросу -- выдача всех

    playlists = []

    search_pl = sp.search(q = query, type = "playlist", limit = 50, offset = 0)
    total = search_pl["playlists"]["total"]
    items = search_pl["playlists"]["items"]


    offset = 0

    if (total > 50):

        iterations = total // 50

        for i in range(iterations):
            search_pl = sp.search(q = query, type = "playlist", limit = 50, offset = offset)
            items = search_pl["playlists"]["items"]

            for j in range(50):
                playlists.append([items[j]["owner"]["id"], items[j]["id"]])

            offset += 50
            time.sleep(0.1)


        if (total % 50):
            last_total = total - offset
            search_pl = sp.search(q = query, type = "playlist", limit = 50, offset = offset)
            items = search_pl["playlists"]["items"]

            for j in range(last_total):
                playlists.append([items[j]["owner"]["id"], items[j]["id"]])

    else:
        for j in range(total):
            playlists.append([items[i]["owner"]["id"], items[j]["id"]])


    return playlists

