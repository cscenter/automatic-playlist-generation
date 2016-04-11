import json
import re


path = "musotest.json"

regex_template = "[ \n\?!]+"

with open(path, encoding="utf-8", errors="surrogateescape") as data_file:    
    data = json.load(data_file)

def lyrics_by_artist(genre_name):

    dic_lyr = dict()
    lyr_a = []
    
    for key in data:
        tmp =  data[key]
        if "id3" in tmp:
            id = tmp["id3"]
            if ("genre" in id) and ("lyrics" in id):
 #               if (id["genre"] == genre_name):
                g = id["genre"]
                if (g.find(genre_name) != -1):
                    tmp_str = id["lyrics"].lower()
                    lyr = re.split(regex_template, tmp_str)
                    lyr_a.extend(lyr)

    for s in lyr_a:
        if s in dic_lyr:
            dic_lyr[s] += 1
        else:
            dic_lyr[s] = 1

    with open(genre_name, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in dic_lyr.items()]

    
    
    return


    

lyrics_by_artist("Alternative")







