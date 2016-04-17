import sys
import json
from collections import Counter
from get_lyrics import get_lyrics_wikia


path = "music.json"

def lyrics_to_list(txt):
    
    txt = txt.replace(",", "")
    txt = txt.replace(".", "")   
    txt = txt.replace("?", "")
    txt = txt.replace("-", "")   
    text = txt.split()

    return text



with open(path) as data_file:    
    data = json.load(data_file)


def lyrics_by_artist(artist_name):

    lyr_list = ""
    
    for key in data:
        tmp =  data[key]
        if "id3" in tmp:
            id = tmp["id3"]
            if ("artist" in id) and ("lyrics" in id):
                if (id["artist"] == artist_name):
                    lyr_lower = id["lyrics"].lower()
                    lyr_list = lyrics_to_list(lyr_lower)

    count_lyr = Counter(lyr_list)
                    
                    
    with open(artist_name, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in count_lyr.items()]

    
    
    return





lyrics_by_artist("Limp Bizkit")
