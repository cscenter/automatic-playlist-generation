import fileinput
import json

dict_100 = {}
list_100 = []

path100 = "" # список композиций тестового множества
path = "" # полный список плейлистов формата p_id: [track1, track2,... ] построчно
out1 = "" # плейлисты, содержащие хотя бы 2 композиции из тестового множества

# считать топ 100
i = 0

with fileinput.input(files = path100) as f:
    for line in f:
        line_split = line.split("\t")
        title = line_split[0] + "\t" + line_split[1]
        list_100.append(title)
        dict_100[title] = i
        i += 1


# игнорировать всё, что не попало в список. что в списке -- присваивать
# номер и если больше 2 треков в плейлисте из топа, дампить

out_f = open(out1, 'w')

with fileinput.input(files = path) as f:
    tmp_pl = {}
    for line in f:
        try:
            tmp_pl = json.loads(line)
            p_id = list(tmp_pl.keys())[0]
            tracks = tmp_pl[p_id]
            tmp_list = []

            l = len(tracks)

            for i in range(l):
                track = tracks[i][0] + "\t" + tracks[i][1]
                if track in dict_100:
                    tmp_list.append(dict_100[track])


            if (len(tmp_list) > 1):
                json.dump(tmp_list, out_f)
                out_f.write("\n")
        except:
            print("bad line:", line)

out_f.close()