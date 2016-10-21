import json
import urllib.request
import time
from urllib.parse import quote
import fileinput

path_before_artist = 'http://ws.audioscrobbler.com/2.0/?method=artist.getcorrection&artist='
path_after_artist = '&api_key=8c6726b0d09be11902f257f3f8341c99&format=json'

path_track_1 = 'http://ws.audioscrobbler.com/2.0/?method=track.getcorrection&artist='
path_track_2 = '&track='
path_track_3 = '&api_key=8c6726b0d09be11902f257f3f8341c99&format=json'

path = '/mnt/hdd3/1_5M.txt'

tmp_json = 'tmp.json'

artist_bad = set()       # не требуют коррекции
artist_good = set()      # коррекция не поможет
artist_rename = {}       # словарь перехода к правильному названию


def correct_artist(artist):
    tmp_json = 'tmp_track.json'

    url_artist = path_before_artist + quote(artist) + path_after_artist

    artist_corr = ""

    try:

        urllib.request.urlretrieve(url_artist, tmp_json)

        with open(tmp_json) as corr_json:
            corr = json.load(corr_json)

        corr_data = corr['corrections']['correction']['artist']

        if 'name' in corr_data:
            artist_corr = corr_data['name']

        corr_json.close()


    except:
        print("error for:", artist)

        time.sleep(0.25)

    return artist_corr




def correct_title(artist, title):
    tmp_json = 'tmp_track.json'

    url_name = path_track_1 + quote(artist) + path_track_2 + quote(title) + path_track_3

    title_corr = ""

    try:

        urllib.request.urlretrieve(url_name, tmp_json)

        with open(tmp_json) as corr_json:
            corr = json.load(corr_json)

            corr_data = corr['corrections']['correction']['track']

            if 'name' in corr_data:
                title_corr = corr_data['name']

            corr_json.close()
    except:
        print("error for:", artist, "-", title)

    time.sleep(0.25)


    return title_corr





# на входе json вида {"tracks": [{"track_title": "...", "artist_name": "..."}, ...], "playlist_id": ...}
# коррекция имени исполнителя, потом коррекция названия композиции с правильным именем исполнителя

def correct_pl(line):
    line_json = json.loads(line)

    track_list = line_json["tracks"]
    l = len(track_list)

    del_list = []          # не получается сделать коррекцию, элементы с этим индексом нужно удалить

    for i in range(l):

        track = track_list[i]

        artist = track["artist_name"]
        title = track["track_title"]

        track_name = artist + "-" + title


        if (artist in artist_good):
            track_corr = correct_title(artist, title)
            if (track_corr == ""):
                del_list.append(i)
            else:
                track["track_title"] = track_corr

        elif (artist in artist_bad):
            del_list.append(i)

        elif (artist in artist_rename):
            artist_corr = artist_rename["artist"]
            track["artist_name"] = artist_corr
            track_corr = correct_title(artist, title)
            if (track_corr == ""):
                del_list.append(i)
            else:
                track["track_title"] = track_corr

        else:
            artist_corr = correct_artist(artist)

            if (artist_corr == ""):
                del_list.append(i)
                artist_bad.add(artist)
            else:
                if (artist == artist_corr):
                    artist_good.add(artist)
                else:
                    artist_good.add(artist_corr)
                    artist_rename["artist"] = artist_corr
                    track["artist_name"] = artist_corr


            track_corr = correct_title(artist_corr, title)
            if ((track_corr == "") and (i not in del_list)):
                del_list.append(i)
            else:
                track["track_title"] = track_corr


    for i in sorted(del_list, reverse=True):
        del track_list[i]

    new_l = len(track_list)

    lines_tsv = []

    for i in range(new_l):
        track = track_list[i]
        tmp_str = track["artist_name"] + '\t' + track["track_title"]
        lines_tsv.append(tmp_str)


    return lines_tsv


path_out = '/mnt/hdd3/1_5M_corr.txt'

f_out = open(path_out, 'w')

with fileinput.input(files = path) as f:
    for line in f:
        #if (fileinput.lineno() < 825):
        #    continue
        new_lines = correct_pl(line)
        l_n = len(new_lines)
        for i in range(l_n):
            f_out.write(new_lines[i])
            f_out.write('\n')

        print(fileinput.lineno())
