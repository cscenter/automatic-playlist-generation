import sys
import json
from mutagen.id3 import ID3

path_json = "music2.json"

with open(path_json) as data_file:    
    data = json.load(data_file)



for key in data:
    audio = ID3(key)

    lyr = audio.getall("USLT")
    lyrics_id3 = ""
    
    if len(lyr)>0:           # replace MacOS line separator with normal one
        lyrics_id3 = (lyr[0].text).replace("\r", "\n")
        tmp = data[key]
        id = tmp["id3"]
        id["lyrics"] = lyrics_id3

        with open(path_json, "w") as data_w:
            data_w.write(json.dumps(data))     
