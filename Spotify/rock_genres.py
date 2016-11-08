import spotipy
import sys
import spotipy.util as util
import json
import time
import re
from collections import Counter

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'
SPOTIPY_USERNAME = ''

token = util.prompt_for_user_token(username = SPOTIPY_USERNAME, client_id=SPOTIPY_CLIENT_ID,
                                   client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)


sp = spotipy.Spotify(auth=token)

path_dir = "genres/"

genre_count = {}

def get_playlist_by_genre(genre):
    search_pl = sp.search(q = genre, type = "playlist", limit = 50)
    cnt = search_pl["playlists"]["total"]

    genre_count[genre] = cnt

    print("genre:", genre, ", number of playlists:", cnt)


    json_out = path_dir + genre + ".json"

    with open(json_out, 'w') as f_out:
        json.dump(search_pl, f_out)

    time.sleep(0.2)


wiki_rock = [re.sub('[-/]', ' ', line.strip().lower()) for line in open("wiki_rock.txt", "r")]


for genre in wiki_rock:
    get_playlist_by_genre(genre)


other_list = ["Early British Pop", "Garage Rock", "Surf Music", "Folk Rock", "Psychedelic Rock", "Progressive Rock", "Soft Rock", "Hard Rock",
              "Heavy Metal", "Arena Rock", "Punk Rock", "New Wave", "Post Punk", "Glam Metal", "Instrumental Rock", "Alternative Rock",
              "Grunge", "Britpop", "Indie Rock", "Pop Punk", "Post-Grunge", "Nu Metal", "Rapcore", "Emo", "Metalcore"]


print(Counter(genre_count))

tmp_json = path_dir + "0_counter.json"

with open(tmp_json, 'w') as f_out:
    json.dump(genre_count, f_out)

    
for genre in other_list:
    get_playlist_by_genre(genre.lower())


print(Counter(genre_count))
