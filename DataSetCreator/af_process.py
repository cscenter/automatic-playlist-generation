import json
import os
import fileinput


# без duration, т.к. слишком большое число. про нормализацию тех,
# которые не от 0 до 1, тоже подумать:  loudness, key, tempo, time_signature

a_f = ["danceability", "energy", "key", "loudness", "mode", "speechiness",
       "acousticness", "instrumentalness", "liveness", "valence",
       "tempo", "time_signature"]


# обработать каталог с выкачанными spotify id,
# оставлять один id (пока), составить список

# path -- директория с выкачанными spotify_id, json для каждого трека



def find_id(path, artist, title):

    ids = []

    artist = artist.lower()
    title = title.lower()

    files = os.listdir(path)
    file_name = artist + " " + title + ".json"

    if file_name in files:
        full_path = path + file_name
        f_open = open(full_path)
        data = json.load(f_open)

        items = data["tracks"]["items"]

        l = len(items)

        for i in range(l):
            if (items[i]["name"].lower() == title):     # название трека
                artists = items[i]["artists"]           # массив исполнителей
                if (artists[0]["name"].lower() == artist):
                    ids.append(items[i]["id"])

        f_open.close()

    return ids


# file_in -- построчно записано artist<tab>title
# file_out -- построчно artist<tab>title<tab>id -- чтобы удобнее выкачивать audio_features


def ids_to_file(file_in, file_out):

    f_out = open(file_out, "w")
    with fileinput.input(files = file_in) as f:


        for line in f:

            tab_sep = line.split('\t')
            artist = tab_sep[0]
            title = tab_sep[1].split("\n")[0]

            track_id = find_id(path, artist, title)
            if (len(track_id) > 0):

                tmp_line = artist + "\t" + title + "\t" + track_id[0] + "\n"
                f_out.write(tmp_line)

            else:
                print("no id for:", artist, title)


    return



# file_in -- построчно записаны id spotify: artist<tab>title<tab>id
# file_out словарь artist:[track:id, ...] -- чтобы удобнее искать id трека
# path -- где выкачаны spotify_id

def ids_to_json(file_in, file_out):

    f_out = open(file_out, "w")

    with fileinput.input(files = file_in) as f:

        dict_out = {}

        for line in f:
            tmp_dict = {}

            tab_sep = line.split('\t')
            artist = tab_sep[0]
            title = tab_sep[1]
            id = tab_sep[2].split("\n")[0]

            if artist not in dict_out:
                dict_out[artist] = []

            tmp_dict[title] = id

            dict_out[artist].append(tmp_dict)

    with open(file_out, "w") as f_out:
        json.dump(dict_out, f_out)


    return



a_f_0 = ["key", "loudness", "mode","tempo", "time_signature"]
a_f_1 = ["danceability", "energy","speechiness", "acousticness", "instrumentalness", "liveness", "valence"]

# умножать на 100: danceability, energy, speechiness, acousticness,
# instrumentalness, liveness, valence


def get_af(file_name):

    af_list = []

    features = json.load(open(file_name))

    af_dict = features[0]

    for a_feature in a_f_0:
        af_list.append(round(af_dict[a_feature]))

    for a_feature in a_f_1:
        af_list.append(round(100*af_dict[a_feature]))


    return af_list



# path -- директория с выкачанными audio-features, название spotify_af, имя файла -- id трека
# file_in1 -- список построчно artist<tab>title<tab>idx
# file_in2 -- словарь spotify_ids
# file_out -- массив векторов из audio features


def af_to_file(path, file_in1, file_in2, file_out):

    track_list = open(file_in1)
    data = json.load(open(file_in2))

    big_list = []


    for line in track_list:

        tab_sep = line.split("\t")
        artist = tab_sep[0]
        title = tab_sep[1]

        vect = [0]*12

        if artist in data:

            tracks = data[artist]
            l_t = len(tracks)

            for i in range(l_t):

                track = tracks[i]
                title_i = list(track.keys())[0]

                if (title == title_i):
                    track_id = track[title_i]
                    file_name = path + track_id + ".json"
                    try:
                        vect = get_af(file_name)
                    except:
                        print("no id")

        big_list.append(vect)

    print(len(big_list))

    with open(file_out, "w") as f_out:
        json.dump(big_list, f_out)


    return



