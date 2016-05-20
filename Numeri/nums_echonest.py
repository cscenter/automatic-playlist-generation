import json
import time


path = "music.json"

echo_tags = ['key', 'energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'danceability', 'time_signature', 'duration', 'loudness', 'valence', 'mode']

names = []
nums = []


f = open("echo.txt", 'w')

with open(path) as data_file:    
    data = json.load(data_file)


for key in data:
    tmp =  data[key]
    if "echo_nest" in tmp:
        id = tmp["id3"]
        echon = tmp["echo_nest"]
        if "summary" in echon:
            echo_sum = echon["summary"]
            nn = []
            for tag in echo_tags:
                nn.append(echo_sum[tag])

            nums.append(nn)
            name = id["artist"] + ":" + id["title"]
            names.append(name)


for i in range(len(nums)):
    tmp = "%s \t %s\n" % (names[i], str(nums[i]))
    f.write(tmp)
