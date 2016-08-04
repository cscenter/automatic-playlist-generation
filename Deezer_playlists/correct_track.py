import json
import urllib.request
import time

path_before_artist = 'http://ws.audioscrobbler.com/2.0/?method=artist.getcorrection&artist='

path_after_artist = '&api_key=API_KEY&format=json'

path_track_1 = 'http://ws.audioscrobbler.com/2.0/?method=track.getcorrection&artist='

path_track_2 = '&track='

path_track_3 = '&api_key=API_KEY&format=json'


path = '/mnt/hdd3/7_9k_s.json'

tmp_json = 'tmp.json'

artists = set()
tracks = set()

track_list = {}


with open(path) as data_file:
        data_d = json.load(data_file)


        

for key in data_d:
    playlist = key

    tracklist = playlist['tracks']
    for track in tracklist:


        artist = track['artist_name']
        title = track['track_title']

        track_name = artist + "-" + title

        # correct artist

        if not(artist in artists):
        
            url_name_1 = path_before_artist + artist + path_after_artist

            try:

                urllib.request.urlretrieve(url_name_1, tmp_json)

                with open(tmp_json) as corr_json:
                    corr = json.load(corr_json)

                corr_data = corr['corrections']['correction']['artist']

                if 'name' in corr_data:
                    artist = corr_data['name']
                    artists.add(artist)

                    track_list[artist] = []
                    
                corr_json.close()
                
            except:
                print("urllib error for:", artist)

            time.sleep(0.25)
                
        if (artist in artists):

            # correct track

            if not(track_name in tracks):

                url_name_2 = path_track_1 + artist + path_track_2 + title + path_track_3
                try:

                    urllib.request.urlretrieve(url_name_2, tmp_json)

                    with open(tmp_json) as corr_json:
                        corr = json.load(corr_json)

                    corr_data = corr['corrections']['correction']['track']

                    if 'name' in corr_data:
                        title = corr_data['name']
                        track_name = artist + "-" + title

                        tracks.add(track_name)

                        track_list[artist].append(title)

                        print("Added:", track_name)

                    corr_json.close()

                except:
                    print("urllib error for:", artist, "-", title)   
        
                time.sleep(0.25)

data_file.close()

with open('/mnt/hdd3/tmp_tracks.json', 'w') as data_write:
    data_write.write(json.dumps(track_list))
        
print(len(artists))
