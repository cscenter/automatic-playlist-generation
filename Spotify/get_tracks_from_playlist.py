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




def get_playlists_ids(file_input):           # id плейлистов из выдачи по категории или ключевому слову

    playlists = []
    data_pl = json.load(open(file_input))
    items = data_pl["playlists"]["items"]

    l_i = len(items)

    for i in range(l_i):
        tmp_list = []

        tmp_list.append(items[i]["owner"]["id"])
        tmp_list.append(items[i]["id"])

        playlists.append(tmp_list)

    return playlists


pl_list = get_playlists_ids("jazz.json")

l = len(pl_list)

for i in range(l):
    get_playlist_tracks(pl_list[i][0], pl_list[i][1])
