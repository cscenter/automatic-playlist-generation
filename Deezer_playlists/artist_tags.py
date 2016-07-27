import json
import pylast
import time

path_in = '/mnt/hdd3/7_16k_artists.txt'


LAST_FM_USER = ""
LAST_FM_PASSWORD = ""
LAST_FM_API_KEY = ""
LAST_FM_API_SECRET = ""

username = LAST_FM_USER
password_hash = pylast.md5(LAST_FM_PASSWORD)
network = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY, api_secret=LAST_FM_API_SECRET, username=username, password_hash=password_hash)


def lastfm_tags(artist):
    
    tag_dict = {}

    try:
        artist_data = network.get_artist(artist)
        tag = [t[0].get_name() for t in artist_data.get_top_tags()]
        cnt = [t[1] for t in artist_data.get_top_tags()]
        tag_dict = dict(zip(tag, cnt))
    except:
        print("No tags for", artist)
        
    time.sleep(0.25)

    return tag_dict




artists = [line.rstrip('\n') for line in open(path_in)]

artists_dict = dict((el, {}) for el in artists)


for artist in artists:
    tmp_dict = lastfm_tags(artist)
    artists_dict[artist] = tmp_dict


path_out = '/mnt/hdd3/artist_29k.json'


with open(path_out, 'w') as data_write:
    data_write.write(json.dumps(artists_dict))

