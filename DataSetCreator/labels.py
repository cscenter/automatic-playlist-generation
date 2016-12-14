import json



# file_in1 -- датасет поменьше, можно текстовый файл с индексами
# file_in2 -- датасет побольше, лучше словарь
# file_out -- текстовый -- какие треки есть и там, и там
# с индексами для датасета поменьше

def common_tracks(file_in1, file_in2, file_out):

    f_in = open(file_in1)

    data = json.load(open(file_in2))

    f_out = open(file_out, "w")

    idx = 0

    for line in f_in:
        tab_sep = line.split("\t")

        artist = tab_sep[0]
        title = tab_sep[1]

        if artist in data:

            tracks = data[artist]

            if title in tracks:

                f_out.write(line)
                idx += 1
    print(idx)

    return




# file_in1 -- треки и индексы в тестовом множестве для того, что в пересечении
# file_in2 -- индексы всего в обучающем
# file_out -- построчно: трек, индекс в обучающем

def match_idx(file_in1, file_in2, file_out):

    tracks = []

    f_in1 = open(file_in1)
    f_in2 = open(file_in2)

    f_out = open(file_out, "w")

    for line in f_in1:
        tab_sep = line.split("\t")
        artist = tab_sep[0]
        title = tab_sep[1]
        tracks.append([artist, title])

    for line in f_in2:
        tab_sep = line.split("\t")
        artist = tab_sep[0]
        title = tab_sep[1]
        tmp_list = [artist, title]

        if tmp_list in tracks:
            f_out.write(line)


    return



# file_in -- жанры по тегу-запросу для каждого трека, построчно tag<tab>artist<tab>title
# file_out -- словарь {artist<tab>title: [tags], ...}


def get_tag(file_in, file_out):

    f_in = open(file_in)
    f_out = open(file_out, "w")

    dict_out = {}

    for line in f_in:
        tab_sep = line.split("\t")
        tag = tab_sep[0]
        artist = tab_sep[1]
        title = tab_sep[2].split("\n")[0]

        track = artist + "\t" + title

        if track not in dict_out:
            dict_out[track] = []

        dict_out[track].append(tag)

    json.dump(dict_out, f_out)


    return



# file_in1 -- список lastfm_test, попавших в train с индексами в train
# file_in2 -- словарь {artist<tab>title: [tags], ...}


def get_tag_by_train_id(id, file_in1, file_in2):

    tags = []
    artist = ""
    title = ""

    f_in1 = open(file_in1)
    f_in2 = open(file_in2)

    data = json.load(f_in2)

    for line in f_in1:
        tab_sep = line.split("\t")
        idx = tab_sep[2].split("\n")[0]

        if (idx == str(id)):
            artist = tab_sep[0]
            title = tab_sep[1]

            track = artist + "\t" + title

            if track in data:
                tags = data[track]

            break

    return tags, artist, title
