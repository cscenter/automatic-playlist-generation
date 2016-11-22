import json
import os
import math


def get_artist_tags(path, path_out):

    path_full = path + "artist_tags/"

    files = os.listdir(path_full)

    dict_write = {}

    for file in files:
        file_in = open(path_full + file)

        data = json.load(file_in)
        artist = data["toptags"]["@attr"]["artist"]
        tags = data["toptags"]["tag"]      

        tmp_dict = {}

        for tag in tags:
            name = tag["name"]
            tmp_dict[name] = tag["count"]

        dict_write[artist] = tmp_dict

    json_out = path_out
    with open(json_out, 'w') as f_out:
        json.dump(dict_write, f_out)

    return




def get_track_tags(path, path_out):

    path_full = path + "track_tags/"

    files = os.listdir(path_full)

    dict_write = {}

    for file in files:
        file_in = open(path_full + file)

        data = json.load(file_in)

        artist = data["toptags"]["@attr"]["artist"]

        if artist not in dict_write:
            dict_write[artist] = []

        title = data["toptags"]["@attr"]["track"]
        tags = data["toptags"]["tag"]

        tmp_dict = {}
        track_dict = {}

        for tag in tags:
            name = tag["name"]
            tmp_dict[name] = tag["count"]

        track_dict[title] = tmp_dict

        dict_write[artist].append(track_dict)

    json_out = path_out
    with open(json_out, 'w') as f_out:
        json.dump(dict_write, f_out)

    return



def get_artist_similar(path, path_out):

    path_full = path + "artist_similar/"

    files = os.listdir(path_full)

    dict_write = {}

    for file in files:
        file_in = open(path_full + file)


        data = json.load(file_in)

        artist = data["similarartists"]["@attr"]["artist"]
        similar = data["similarartists"]["artist"]

        tmp_dict = {}

        for sim_art in similar:
            name = sim_art["name"]
            tmp_dict[name] = sim_art["match"]

        dict_write[artist] = tmp_dict

    json_out = path_out
    with open(json_out, 'w') as f_out:
        json.dump(dict_write, f_out)

    return



def get_track_similar(path, path_out):            # почему-то в выдаче нет имени трека, надо выковыривать из названия файла

    path_full = path + "track_similar/"

    files = os.listdir(path_full)

    dict_write = {}

    for file in files:
        file_in = open(path_full + file)

        file_name = file.split(".json")[0]

        title = file_name.split(" - ")[1]

        data = json.load(file_in)

        artist = data["similartracks"]["@attr"]["artist"]

        if artist not in dict_write:
            dict_write[artist] = []

        #title = data["similartracks"]["@attr"]["track"]
        tracks = data["similartracks"]["track"]


        track_dict = {}
        track_dict[title] = []

        for track in tracks:
            tmp_dict = {}
            track_name = track["name"]
            artist_name = track["artist"]["name"]
            match = track["match"]

            tmp_dict["artist"] = artist_name
            tmp_dict["title"] = track_name
            tmp_dict["match"] = match

            track_dict[title].append(tmp_dict)

        dict_write[artist].append(track_dict)

    json_out = path_out
    with open(json_out, 'w') as f_out:
        json.dump(dict_write, f_out)

    return



def get_artist_tracks(path, path_out):

    path_full = path + "artist_tracks/"

    files = os.listdir(path_full)

    dict_write = {}

    for file in files:
        file_in = open(path_full + file)

        data = json.load(file_in)
        artist = data["toptracks"]["@attr"]["artist"]
        tracks = data["toptracks"]["track"]

        tmp_dict = {}

        for track in tracks:
            name = track["name"]
            rank = int(track["@attr"]["rank"]) - 1

            tmp_dict[name] = math.exp(-rank/10.0)



        dict_write[artist] = tmp_dict

    json_out = path_out
    with open(json_out, 'w') as f_out:
        json.dump(dict_write, f_out)

    return



