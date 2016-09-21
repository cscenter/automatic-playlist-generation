import json
import time
import urllib.request
from urllib.parse import quote


path_before_artist = 'http://ws.audioscrobbler.com/2.0/?method=artist.getcorrection&artist='

path_after_artist = '&api_key=API_KEY&format=json'

path_track_1 = 'http://ws.audioscrobbler.com/2.0/?method=track.getcorrection&artist='

path_track_2 = '&track='

path_track_3 = '&api_key=API_KEY&format=json'



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
