import json

path = "/mnt/hdd3/7_16k.json"

artists = set()

with open(path) as data_file:
        data_d = json.load(data_file)


for key in data_d:
    playlist = key

    tracklist = playlist['tracks']
    for track in tracklist:
        
        artists.add(track['artist_name'])

data_file.close()     

with open('/mnt/hdd3/7_16k_artists.txt', 'w') as data_write:
    data_write.write("\n".join(artists))
        
print(len(artists))
        
