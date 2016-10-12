import json
import urllib.request
import time
from urllib.parse import quote
import fileinput

path_before_artist = 'http://ws.audioscrobbler.com/2.0/?method=artist.getcorrection&artist='
path_after_artist = '&api_key=API_KEY&format=json'

path_track_1 = 'http://ws.audioscrobbler.com/2.0/?method=track.getcorrection&artist='
path_track_2 = '&track='
path_track_3 = '&api_key=API_KEY&format=json'

path = '/mnt/hdd3/small_new.txt'

tmp_json = 'tmp.json'


# на входе json вида {"tracks": [{"track_title": "...", "artist_name": "..."}, ...], "playlist_id": ...}
# коррекция имени исполнителя, потом коррекция назваия композиции с правильным именем исполнителя

def correct_pl(line):
    line_json = json.loads(line)

    track_list = line_json["tracks"]
    l = len(track_list)

    del_list = []

    for i in range(l):
        is_artist_correct = 0

        track = track_list[i]

        artist = track["artist_name"]
        title = track["track_title"]

        track_name = artist + "-" + title

        # correct artist
        url_name_1 = path_before_artist + quote(artist) + path_after_artist

        is_artist_correct = 0

        try:
            urllib.request.urlretrieve(url_name_1, tmp_json)

            with open(tmp_json) as corr_json:
                corr = json.load(corr_json)

            corr_data = corr['corrections']['correction']['artist']

            if 'name' in corr_data:
                artist = corr_data['name']
                track["artist_name"] = artist
                is_artist_correct = 1

            else:
                print('artist not corrected', artist)
                del_list.append(i)

            corr_json.close()


        except:
            print("urllib error for:", artist)
            del_list.append(i)

        time.sleep(0.25)

        # correct track

        if is_artist_correct:

            url_name_2 = path_track_1 + quote(artist) + path_track_2 + quote(title) + path_track_3

            try:

                urllib.request.urlretrieve(url_name_2, tmp_json)

                with open(tmp_json) as corr_json:
                    corr = json.load(corr_json)

                corr_data = corr['corrections']['correction']['track']

                if 'name' in corr_data:
                    title = corr_data['name']
                    track["track_title"] = title
                    track_name = artist + "-" + title

                else:
                    print('title not corrected', title)
                    del_list.append(i)

                corr_json.close()


            except:
                print("urllib error for:", artist, "-", title)
                del_list.append(i)

            time.sleep(0.25)

    for i in sorted(del_list, reverse=True):
        del track_list[i]

    new_line_json = {}

    new_line_json["tracks"] = track_list
    new_line_json["playlist_id"] = line_json["playlist_id"]

    new_line = json.dumps(new_line_json)

    return new_line


path_out = '/mnt/hdd3/small_corr.txt'

f_out = open(path_out, 'w')

with fileinput.input(files = path) as f:
    for line in f:
        new_line = correct_pl(line)
        f_out.write(new_line)
        f_out.write('\n')

        # print(fileinput.lineno()) номер строчки, можно записывать отдельно, чтобы прерывать обработку
