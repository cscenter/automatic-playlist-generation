import json
import time


path = "music.json"

last_tags = []
names = []


f = open("lastfm.txt", 'w')

with open(path) as data_file:    
    data = json.load(data_file)


for key in data:
    tmp =  data[key]
    if "lastfm" in tmp:
        id = tmp["id3"]
        lf = tmp["lastfm"]
        l_t = []
        if "artistsimilar" in lf:
            l_t = l_t + lf["artistsimilar"]
        if "artisttags" in lf:
            l_t = l_t + lf["artisttags"]
        if "tracktags" in lf:
            l_t = l_t + lf["tracktags"]
            
        if ("artist" in id) and ("title" in id):
            name = id["artist"] + ":" + id["title"]
            names.append(name)

            l_low = []
            for s in l_t:
                l_low.append(s.lower())
            last_tags.append(l_low)          


for i in range(len(names)):
    tmp = "%s \t %s\n" % (names[i], str(last_tags[i]))
    f.write(tmp)
