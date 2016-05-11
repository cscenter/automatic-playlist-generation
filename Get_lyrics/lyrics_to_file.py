import sys
import re
import json

from nltk.corpus import stopwords


path_json = "music2.json"

with open(path_json) as data_file:    
    data = json.load(data_file)


f = open("lyrics_all.tsv", 'w')

tmp = "%s \t %s \n" % ("name", "lyrics")
f.write(tmp)

for key in data:
    tmp =  data[key]
    if "id3" in tmp:
        id = tmp["id3"]
        if ("artist" in id) and ("title" in id):
            artist_name =  id["artist"]
            title_name = id["title"]

            nm = artist_name + ':' + title_name
            lyr = id["lyrics"]

            lyr = re.sub("[^a-zA-Z]"," ", lyr)
            words = lyr.lower().split()

            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]

            tmp = '"%s" \t %s \n' % (nm, words)
            f.write(tmp)
