import json
from get_lyrics import get_lyrics_wikia
import time


path = "/mnt/hdd3/music/music.json"
no_lyr = "T [["


with open(path) as data_file:    
    data = json.load(data_file)


for key in data:
    tmp =  data[key]
    if "id3" in tmp:
        id = tmp["id3"]
        if ("artist" in id) and ("title" in id):
            artist_name =  id["artist"]
            title_name = id["title"]

            if id["lyrics"] != "":

                lyr = get_lyrics_wikia(title_name, artist_name, 1)

                if (lyr[0:4] != no_lyr) and (lyr[0:4] != no_lyr.lower()) :
                    id["lyrics"] = lyr

                    
                       
                with open(path, "w") as data_w:
                    data_w.write(json.dumps(data))




