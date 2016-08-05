import json
import pylast
import time

path = '/mnt/hdd3/tmp_tracks.json'


LAST_FM_USER = ""
LAST_FM_PASSWORD = ""
LAST_FM_API_KEY = ""
LAST_FM_API_SECRET = ""

username = LAST_FM_USER
password_hash = pylast.md5(LAST_FM_PASSWORD)
network = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY, api_secret=LAST_FM_API_SECRET, username=username, password_hash=password_hash)

tags_list = []

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



with open(path) as data_file:
        data_d = json.load(data_file)

     
for artist in data_d:
    tracks = data_d[artist]

    if (tracks != []):
        tmp_dict = {}
        tmp_dict['artist_name'] = artist
        tmp_dict['artist_tags'] = artist_tags(artist)
        tmp_dict['tracks'] = []
        
        for track in tracks:
            track_dict = {}
            track_dict['title'] = track
            track_dict['track_tags'] = track_tags(artist, track)
            tmp_dict['tracks'].append(track_dict)

            print(artist, "-", track)

        tags_list.append(tmp_dict)
            
data_file.close()

            
path_out = '/mnt/hdd3/tmp_tags.json'


with open(path_out, 'w') as data_write:
    data_write.write(json.dumps(tags_list))

