import json


def tag_lowering(tag_dict):  # на вход --словарь тегов с подсчётом использований

    new_dict = {}

    for tag in tag_dict:  # сначала добавить все islower
        if tag.islower():
            new_dict[tag] = tag_dict[tag]

    for tag in tag_dict:  # пройтись ещё раз
        if not (tag.islower()):
            tag_l = tag.lower()

            if tag_l in new_dict:

                cnt1 = new_dict[tag_l]
                cnt2 = tag_dict[tag]

                if (cnt1 + cnt2) < 100:
                    new_dict[tag_l] += cnt2
                else:
                    new_dict[tag_l] = 100

            else:
                new_dict[tag_l] = tag_dict[tag]

    return new_dict



# предварительно, потом к ним ещё относить разное

tag_list = ["00s", "10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90s",
            "male vocalists", "female vocalists", "usa", "uk", "german", "french",
            "spanish", "italian", "english", "oldies", "piano", "germany", "france",
            "blues", "country", "americana", "bluegrass", "rockabilly", "folk",
            "reggae", "jazz", "bossa nova", "funk", "swing", "easy listening",
            "chillout", "lounge", "new age", "ambient", "relax", "breakbeat",
            "disco", "downtempo", "acid jazz", "drum and bass", "rhythm and blues",
            "guitar", "club", "dub", "dubstep", "electronica", "electronic", "electro",
            "house", "idm", "glitch", "synthpop", "techno", "trance", "trip-hop",
            "hip-hop", "rap", "pop", "rock", "alternative", "indie", "grunge",
            "industrial", "britpop", "post-rock", "shoegaze", "hardcore", "metal",
            "progressive rock", "psychedelic rock", "punk", "rock and roll",
            "art rock", "pop rock", "experimental", "garage rock", "glam rock",
            "hard rock", "classic rock", "new wave", "acoustic", "classical",
            "dance", "soul", "instrumental", "rnb", "latin"]


def tag_reduce(tag_dict):  # на вход --словарь тегов с подсчётом использований

    new_dict = {}

    for tag in tag_dict:

        if tag in tag_list:
            new_dict[tag] = tag_dict[tag]


    return new_dict



# без нормализации числа вхождений
def tag_vector(tag_dict):   # уже reduced теги -- только те, что есть в массиве
    l_t = len(tag_list)

    vect = [0]*l_t

    for i in range(l_t):
        if tag_list[i] in tag_dict:
            vect[i] = tag_dict[tag_list[i]]

    return vect



def test_set(file_in, file_out1, file_out2):   # пока только теги треков

    # сопоставить треки номерам и записать это в файл
    data = json.load(open(file_in))

    idx = 0
    f_out1 = open(file_out1, "w")              # номера треков
    f_out2 = open(file_out2, "w")              # массив векторов, соотв. отобранным признакам. порядок согласован с номерами треков
    big_list = []

    for artist in data:
        tracks = data[artist]
        l_t = len(tracks)

        for i in range(l_t):

            track = tracks[i]
            title = list(track.keys())[0]
            tmp_line = str(idx) + "\t" + artist + "\t" + title + "\n"
            f_out1.write(tmp_line)             # номера в файле
            idx += 1

            tags = track[title]

            t1 = tag_lowering(tags)
            t2 = tag_reduce(t1)
            t3 = tag_vector(t2)

            big_list.append(t3)

    with open(file_out2, "w") as f_out2:
        json.dump(big_list, f_out2)

    return




def train_set_to_vect(file_in, file_out):   # пока только теги треков

    # вывод в виде словаря, чтобы было быстрее сопоставлять с номерами плейлистов
    data = json.load(open(file_in))


    for artist in data:
        tracks = data[artist]
        l_t = len(tracks)

        for i in range(l_t):

            track = tracks[i]
            title = list(track.keys())[0]

            tags = track[title]

            t1 = tag_lowering(tags)
            t2 = tag_reduce(t1)
            t3 = tag_vector(t2)
            track[title] = t3


    with open(file_out, "w") as f_out:
        json.dump(data, f_out)

    return




def train_set(file_pl, file_vect, file_out):

    # file_pl -- построчно p_id<tab>artist<tab>title
    # file_vect -- словарь artist:[track1:tags, track2:tags], где tags -- численные векторы

    pl = open(file_pl)

    vect_dict = json.load(open(file_vect))

    f_out = open(file_out, "w")

    for line in pl:
            tab_sep = line.split('\t')
            p_id = tab_sep[0]
            artist = tab_sep[1]
            title = tab_sep[2].split('\n')[0]

            if artist in vect_dict:
                tracks = vect_dict[artist]
                l_t = len(tracks)



                for i in range(l_t):
                    tmp_title = list(tracks[i].keys())[0]

                if (title == tmp_title):
                    new_line = p_id + "\t" + str(tracks[i][tmp_title])
                    f_out.write(new_line)
                    f_out.write("\n")



    return





