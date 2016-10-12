import json
from os import listdir


path = "/mnt/hdd3/1_5M/"
path_out = "/mnt/hdd3/1_5M.txt"


def extract_data(path_in):

    with open(path_in) as data_file:
        data_d = json.load(data_file)

    pl_dict = {}



    pl_dict["playlist_id"] = data_d["id"]
    pl_dict["tracks"] = []


    tracks = data_d["tracks"]
    tr_data = tracks["data"]

    l = len(tr_data)

    for i in range(l):
        track_dict = {}
        tmp = tr_data[i]
        track_dict["track_title"] = tmp["title"]
        artist_tr = tmp["artist"]
        track_dict["artist_name"] =  artist_tr["name"]

        pl_dict["tracks"].append(track_dict)
        data_file.close()

    return pl_dict


files = [f for f in listdir(path)]

big_json = []

f_out = open(path_out, 'w')

for f in files:

    filename = path + f
    print(f)
    tmp_dict = extract_data(filename)    
    f_out.write(json.dumps(tmp_dict))
    f_out.write('\n')

