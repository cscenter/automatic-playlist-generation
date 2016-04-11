import json
import re


path = "musotest.json"

regex_template = "[ \n\?!]+"

with open(path, encoding="utf-8", errors="surrogateescape") as data_file:    
    data = json.load(data_file)

def lyrics_by_artist(artist_name):

    dic_lyr = dict()
    lyr_a = []
    
    for key in data:
        tmp =  data[key]
        if "id3" in tmp:
            id = tmp["id3"]
            if ("artist" in id) and ("lyrics" in id):
                if (id["artist"] == artist_name):
                    tmp_str = id["lyrics"].lower()
                    lyr = re.split(regex_template, tmp_str)
                    lyr_a.extend(lyr)

    for s in lyr_a:
        if s in dic_lyr:
            dic_lyr[s] += 1
        else:
            dic_lyr[s] = 1

    with open(artist_name, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in dic_lyr.items()]

    
    
    return


    

lyrics_by_artist("Limp Bizkit")







