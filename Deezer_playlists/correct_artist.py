import json
import urllib.request
import time

path_before_artist = 'http://ws.audioscrobbler.com/2.0/?method=artist.getcorrection&artist='

path_after_artist = '&api_key=API_KEY&format=json'

path = '/mnt/hdd3/7_9k_s.json'

tmp_json = 'tmp.json'

artists = set()



with open(path) as data_file:
        data_d = json.load(data_file)


        

for key in data_d:
    playlist = key

    tracklist = playlist['tracks']
    for track in tracklist:

        artist = track['artist_name']

        if not(artist in artists):
        
            url_name = path_before_artist + artist + path_after_artist

            try:

                urllib.request.urlretrieve(url_name, tmp_json)

                with open(tmp_json) as corr_json:
                    corr = json.load(corr_json)

                corr_data = corr['corrections']['correction']['artist']

                if 'name' in corr_data:
                    artists.add(corr_data['name'])
                    
                corr_json.close()
            
            except:
                print("urllib error for:", artist)

        
            time.sleep(0.25)

data_file.close()

with open('/mnt/hdd3/tmp_artists.txt', 'w') as data_write:
    data_write.write("\n".join(artists))
        
print(len(artists))
