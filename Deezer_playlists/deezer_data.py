import json
from os import listdir


path = "/mnt/hdd3/70k/"


def extract_data(path_in):

    with open(path_in) as data_file:
        data_d = json.load(data_file)

    pl_dict = {}



    pl_dict["playlist_id"] = data_d["id"]
    pl_dict["playlist_title"] = data_d["title"]
    pl_dict["playlist_description"] = data_d["description"]

    pl_dict["tracks"] = []


    tracks = data_d["tracks"]

    tr_data = tracks["data"]

    l = len(tr_data)




    for i in range(l):

        track_dict = {}

        tmp = tr_data[i]

        track_dict["track_title"] = tmp["title"]
        track_dict["track_rank"] = tmp["rank"]

        artist_tr = tmp["artist"]

        track_dict["artist_name"] =  artist_tr["name"]
        #track_dict["artist_id"] = artist_tr["id"]


        album_tr = tmp["album"]

        #track_dict["album_id"] = album_tr["id"]
        track_dict["album_title"] = album_tr["title"]

        pl_dict["tracks"].append(track_dict)
        data_file.close()

    return pl_dict





files = [f for f in listdir(path)]

big_json = []

for f in files:

    filename = path + f
    tmp_dict = extract_data(filename)
    big_json.append(tmp_dict)
    
    
with open('/mnt/hdd3/70k.json', 'w') as data_write:
    data_write.write(json.dumps(big_json))
