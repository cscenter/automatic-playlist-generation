import json
import os
import fileinput

# всё к нижнему регистру, суммировать вхождения, но чтобы не более 100
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



# эпохи, пол

def tag_epoch(tag_dict):

    new_dict = {}
    epochs = {}
    epochs_new = {}
    list0 = ["00s","10s","20s","30s","40s","50s","60s","70s","80s","90s"]

    epochs_ap = {}
    epochs_ap_new = {}
    list1 = ["00's","10's","20's","30's","40's","50's","60's","70's","80's","90's"]

    for tag in tag_dict:

        if (tag.find("0s") != -1):
            epochs[tag] = tag_dict[tag]
        elif (tag.find("0's") != -1):
            epochs_ap[tag] = tag_dict[tag]
        else:
            new_dict[tag] = tag_dict[tag]


    for epoch in list0:
        if epoch not in epochs:
            epochs[epoch] = 0

        cnt1 = epochs[epoch]

        for tag in epochs:
            if (tag.find(epoch) != -1) and (tag != epoch):
                cnt2 = epochs[tag]

                if (cnt1 + cnt2) < 100:
                    epochs[epoch] += cnt2
                else:
                    epochs[epoch] = 100

    for epoch in list1:
        if epoch not in epochs_ap:
            epochs_ap[epoch] = 0

        cnt1 = epochs_ap[epoch]

        for tag in epochs_ap:
            if (tag.find(epoch) != -1) and (tag != epoch):
                cnt2 = epochs_ap[tag]

                if (cnt1 + cnt2) < 100:
                    epochs_ap[epoch] += cnt2
                else:
                    epochs_ap[epoch] = 100


    for i in range(10):
        cnt1 = epochs[list0[i]]
        cnt2 = epochs_ap[list1[i]]

        if (cnt1 + cnt2) < 100:
            new_dict[list0[i]] = cnt1 + cnt2
        else:
            new_dict[list0[i]] = 100


    return new_dict




def tag_gender(tag_dict):

    new_dict = {}

    males = {}
    females = {}

    for tag in tag_dict:
        if (tag.find("male ") != -1):

            if (tag.find("female ") != -1):
                females[tag] = tag_dict[tag]
            else:
                males[tag] = tag_dict[tag]

        else:
            new_dict[tag] = tag_dict[tag]

    sum_m = sum(males.values())
    sum_f = sum(females.values())

    if (sum_m < 100):
        new_dict["male vocalist"] = sum_m
    else:
        new_dict["male vocalist"] = 100

    if (sum_f < 100):
        new_dict["female vocalist"] = sum_f
    else:
        new_dict["female vocalist"] = 100

    return new_dict



tag_list = ["00s", "10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90s",
            "male vocalist", "female vocalist",
            "blues", "blues rock", "rhythm and blues",  "rnb", "soul", "funk",
            "jazz", "acid jazz", "nu jazz", "jazz funk", "bossa nova", "swing",
            "country", "country rock", "alt country", "americana",
            "folk", "folk rock", "indie folk",
            "easy listening", "chillout", "lounge", "new age", "ambient", "relax",
            "electronic", "breakbeat", "disco", "downtempo", "drum and bass",
            "club", "dub", "dubstep", "house", "idm", "glitch", "synthpop",
            "new wave", "techno", "trance", "trip hop", "electropop", "dancehall",
            "eurodance", "noise", "hip hop", "rap", "pop", "indie pop",
            "pop rock", "britpop", "dream pop", "power pop", "pop punk", "alternative pop", "dance pop",
            "rock", "alternative", "indie", "grunge", "industrial", "post rock", "shoegaze", "hardcore", "garage rock",
            "metal", "heavy metal", "thrash metal", "metalcore", "progressive metal",
            "black metal", "alternative metal", "nu metal", "power metal", "doom metal", "melodic metal", "gothic metal",
            "progressive rock", "progressive", "experimental", "psychedelic", "art rock", "glam rock", "hard rock",
            "classic rock", "soft rock", "punk", "punk rock", "post-punk", "hardcore punk", "ska punk", "ska",
            "rockabilly", "rock and roll", "latin", "reggae", "acoustic",
            "classical", "piano", "guitar", "chanson", "emo", "celtic", "mpb"
            ]



tag_list_enlarged = ["00s", "10s", "20s", "30s", "40s", "50s", "60s", "70s", "80s", "90s",
                     "male vocalist", "female vocalist",
                     "blues", "blues rock", "rhythm and blues",  "rnb", "soul", "funk",
                     "jazz", "acid jazz", "nu jazz", "jazz funk", "bossa nova", "swing",
                     "country", "country rock", "alt country", "americana",
                     "folk", "folk rock", "indie folk",
                     "easy listening", "chillout", "lounge", "new age", "ambient", "relax",
                     "electronic", "breakbeat", "disco", "downtempo", "drum and bass",
                     "club", "dub", "dubstep", "house", "idm", "glitch", "synthpop",
                     "new wave", "techno", "trance", "trip hop", "electropop", "dancehall",
                     "eurodance", "noise", "hip hop", "rap", "pop", "indie pop",
                     "pop rock", "britpop", "dream pop", "power pop", "pop punk", "alternative pop", "dance pop",
                     "rock", "alternative", "indie", "grunge", "industrial", "post rock", "shoegaze", "hardcore", "garage rock",
                     "metal", "heavy metal", "thrash metal", "metalcore", "progressive metal",
                     "black metal", "alternative metal", "nu metal", "power metal", "doom metal", "melodic metal", "gothic metal",
                     "progressive rock", "progressive", "experimental", "psychedelic", "art rock", "glam rock", "hard rock",
                     "classic rock", "soft rock", "punk", "punk rock", "post-punk", "hardcore punk", "ska punk", "ska",
                     "rockabilly", "rock and roll", "latin", "reggae", "acoustic",
                     "classical", "piano", "guitar", "chanson", "emo", "celtic", "mpb",
                     "bluesrock", "blues-rock", "rhythm & blues", "r&b", "r and b", "funky",
                     "jazzy", "jazz fusion", "vocal jazz", "contemporary jazz", "jazz vocal",
                     "nujazz", "nu-jazz", "funky jazz", "jazz-funk", "country-rock",
                     "folk-rock", "bossanova",  "alternative country", "alt-country",
                     "chill", "chill out", "relaxing", "electro", "electronica",
                     "drum n bass", "dnb", "deep house", "electro house",
                     "synth pop", "synth-pop", "triphop", "trip-hop",
                     "hiphop", "hip-hop", "underground rap", "gangsta rap", "east coast rap",
                     "indiepop", "indie-pop", "poprock", "pop-rock", "brit pop",
                     "dreampop", "dream-pop", "powerpop", "power-pop", "dance-pop",
                     "punk pop", "dance-pop", "alternative rock",  "indie rock", "nu-metal",
                     "garage", "psychedelic", "punkrock", "punk-rock", "rock n roll", "rock'n'roll",
                     "chanson francaise"
                    ]



# всё сводить к первому в списке
tag_mrg = [["blues rock", "bluesrock", "blues-rock"],
             ["rhythm and blues", "rhythm & blues"],
             ["rnb", "r&b", "r and b"],
             ["funk", "funky"],
             ["jazz", "jazzy", "jazz fusion", "vocal jazz", "contemporary jazz", "jazz vocal"],
             ["nu jazz", "nujazz", "nu-jazz"],
             ["jazz funk", "funky jazz", "jazz-funk"],
             ["country rock", "country-rock"],
             ["folk rock", "folk-rock"],
             ["bossa nova", "bossanova"],
             ["alt country", "alternative country", "alt-country"],
             ["chillout", "chill", "chill out"],
             ["relax", "relaxing"],
             ["electronic", "electro", "electronica"],
             ["drum and bass", "drum n bass", "dnb"],
             ["house", "deep house", "electro house"],
             ["synthpop", "synth pop", "synth-pop"],
             ["trip hop", "triphop", "trip-hop"],
             ["hip hop", "hiphop", "hip-hop"],
             ["rap", "underground rap", "gangsta rap", "east coast rap"],
             ["indie pop", "indiepop", "indie-pop"],
             ["pop rock", "poprock", "pop-rock"],
             ["britpop", "brit pop"],
             ["dream pop", "dreampop", "dream-pop"],
             ["power pop", "powerpop", "power-pop"],
             ["dance pop", "dance-pop"],
             ["pop punk", "punk pop"],
             ["dance pop", "dance-pop"],
             ["alternative", "alternative rock"],
             ["indie", "indie rock"],
             ["nu metal", "nu-metal"],
             ["garage rock", "garage"],
             ["psychedelic rock", "psychedelic"],
             ["punk rock", "punkrock", "punk-rock"],
             ["rock and roll", "rock n roll", "rock'n'roll"],
             ["chanson", "chanson francaise"]
             ]


mrg = [item[0] for item in tag_mrg]


def tag_reduce(tag_dict):  # на вход --словарь тегов с подсчётом использований

    new_dict = {}


    for tag in tag_dict:

        if tag in tag_list_enlarged:
            new_dict[tag] = tag_dict[tag]


    return new_dict



def tag_merge(tag_dict):   # уже reduced теги по расширенному массиву

    new_dict = {}
    to_mrg = {}

    for tag in tag_dict:

        if tag in tag_list:
            new_dict[tag] = tag_dict[tag]

        else:              # надо мерджить все остальные
            to_mrg[tag] = tag_dict[tag]

    for tag in mrg:
        if tag not in new_dict:
            new_dict[tag] = 0


    for i in range(len(tag_mrg)):
        cnt = 0

        for j in range(len(tag_mrg[i])):
            tag = tag_mrg[i][j]
            if tag in to_mrg:
                cnt += to_mrg[tag]
        curr_tag = tag_mrg[i][0]
        new_dict[curr_tag] += cnt
        if (new_dict[curr_tag] > 100):
            new_dict[curr_tag] = 100


    return new_dict





# без нормализации числа вхождений.
# нормализацию лучше после считывания делать,
# чтобы меньше места при хранении использовалось

def tag_vector(tag_dict):   # уже reduced теги -- только те, что есть в массиве
    l_t = len(tag_list)

    vect = [0]*l_t

    for i in range(l_t):
        if tag_list[i] in tag_dict:
            vect[i] = tag_dict[tag_list[i]]

    return vect




# отличие test set от train set в том, что train set должен идти в том порядке, в каком плейлисты (повторы могут быть)


# на вход всегда файл, где построчно artist<tab>title<tab>index, индекс равен номеру строки
# для train set файл с повторами, уже всё разложено по плейлистами
# на выходе -- массив векторов встречаемости тегов
# audio_features отдельно, потом их склеить


def lastfm_vect(file_in1, file_in2, file_out):

    track_list = open(file_in1)

    data = json.load(open(file_in2))

    big_list = []

    for line in track_list:
        tab_sep = line.split("\t")
        artist = tab_sep[0]
        title = tab_sep[1]

        l = len(tag_list)

        vect = [0]*l

        if artist in data:

            tracks = data[artist]
            l_t = len(tracks)

            for i in range(l_t):

                track = tracks[i]
                title_i = list(track.keys())[0]

                if (title == title_i):

                    tags = track[title_i]

                    t1 = tag_lowering(tags)
                    t2 = tag_epoch(t1)
                    t3 = tag_gender(t2)
                    t4 = tag_reduce(t3)
                    t5 = tag_merge(t4)
                    vect = tag_vector(t5)

        big_list.append(vect)


    with open(file_out, "w") as f_out:
        json.dump(big_list, f_out)

    return


