import json
import operator
from collections import Counter

path = "ArtistTags.dat"


def cooccurrence(tag):                         # без учёта числа вхождений тега для одного исполнителя

    cooc_tags = []

    for d in all_tags:
        if tag in d:
            cooc_tags.extend(list(d.keys()))

    cnt = Counter(cooc_tags)

    print("usage of tag:", tag, ":", cnt[tag])

    del cnt[tag]

    print(tag, "occurs with:", cnt.mpst_common(10))



def cooccurrence_count(tag):                     # с учётом числа вхождений тега для одного исполнителя

    cooc_tags = {}

    for d in all_tags:
        if tag in d:
            for key in d:
                if (key in cooc_tags):
                    cooc_tags[key] = cooc_tags[key] + d[key]
                else:
                    cooc_tags[key] = d[key]


    print("usage of tag:", tag, ":", cooc_tags[tag])

    del cooc_tags[tag]

    cooc_sorted = sorted(cooc_tags.items(), key=lambda x:(-x[1], x[0]))

    print(tag, "occurs with:", cooc_sorted[:10])




f = open(path, 'r')

all_tags = []
line_split = []
tmp_dict = {}
artist = ""
artist_cnt = 0

for line in f:
    line_split = line.split("<sep>")

    if (line_split[1] != artist):
        artist_cnt += 1
        artist = line_split[1]
        all_tags.append(tmp_dict)
        tmp_dict = {}

    tag = line_split[2]
    tag_cnt = int(line_split[3].split("\n")[0])


    tmp_dict[tag] = tag_cnt

print("number of artists:", artist_cnt)

del all_tags[0]           # empty dict

print(all_tags)


path_out = "tags_count.json"

with open (path_out, 'w') as data_write:
    data_write.write(json.dumps(all_tags))

