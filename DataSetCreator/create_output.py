import json
from lastfm_tags import track_tags, artist_tags, track_similar, artist_similar, track_popularity

# формат входного файла: {ARTIST1: [TRACK1, TRACK2, ... ], ARTIST2: [TRACK1, TRACK2, ... ], ...}

file_in = ""
file_out = ""


# формат вывода: {ARTIST1: [ {TRACK1: {tag1: count1, tag2: count2, ...}},
#                            {TRACK2: {tag1: count1, tag2: count2, ...}}, ...],
#                 ARTIST2: [ {TRACK1: {tag1: count1, tag2: count2, ...}},
#                            {TRACK2: {tag1: count1, tag2: count2, ...}}, ...]
def track_tags_out(file_in, file_out):

    with open(file_in, 'r') as f_in:
        data = json.load(f_in)

    tagged_data = {}

    for artist in data:
        tracks = data[artist]
        l_t = len(tracks)

        tagged_tracks = []

        for i in range(l_t):
            tmp_dict = {}
            title = tracks[i]
            tmp_dict[title] = track_tags(artist, title)
            tagged_tracks.append(tmp_dict)

        tagged_data[artist] = tagged_tracks


    with open(file_out, 'w') as f_out:
        json.dump(tagged_data, f_out)

    f_in.close()
    f_out.close()

    return



# формат вывода: {ARTIST1: {tag1: count1, tag2: count2, ...}, ARTIST2: {tag1: count1, tag2: count2, ...}, ...}
def artist_tags_out(file_in, file_out):

    with open(file_in, 'r') as f_in:
        data = json.load(f_in)

    tagged_data = {}

    for artist in data:
        tagged_data[artist] = artist_tags(artist)

    with open(file_out, 'w') as f_out:
        json.dump(tagged_data, f_out)

    f_in.close()
    f_out.close()

    return


#формат вывода: {ARTIST1: [{TRACK1: [{"artist": artist1, "title": title1, "match": match1}, {"artist": artist2, "title": title2, "match": match2}, ...]},
#                          {TRACK2: [{"artist": artist1, "title": title1, "match": match1}, {"artist": artist2, "title": title2, "match": match2}, ...]}, ...],
#                ARTIST2: [{TRACK1: [{"artist": artist1, "title": title1, "match": match1}, {"artist": artist2, "title": title2, "match": match2}, ...]},
#                          {TRACK2: [{"artist": artist1, "title": title1, "match": match1}, {"artist": artist2, "title": title2, "match": match2}, ...]}, ...], ...}
def track_similar_out(file_in, file_out):

    with open(file_in, 'r') as f_in:
        data = json.load(f_in)

    tagged_data = {}

    for artist in data:
        tracks = data[artist]
        l_t = len(tracks)

        tagged_tracks = []

        for i in range(l_t):
            tmp_dict = {}
            title = tracks[i]
            tmp_dict[title] = track_similar(artist, title)
            tagged_tracks.append(tmp_dict)

        tagged_data[artist] = tagged_tracks

    with open(file_out, 'w') as f_out:
        json.dump(tagged_data, f_out)

    f_in.close()
    f_out.close()

    return



# формат вывода:  {ARTIST1: {artist_similar1: match1, artist_similar2: match2, ...}, ARTIST2: {artist_similar1: match1, artist_similar2: match2, ...}, ...}
def artist_similar_out(file_in, file_out):

    with open(file_in, 'r') as f_in:
        data = json.load(f_in)

    tagged_data = {}

    for artist in data:
        tagged_data[artist] = artist_similar(artist)

    with open(file_out, 'w') as f_out:
        json.dump(tagged_data, f_out)

    f_in.close()
    f_out.close()

    return



# формат вывода: {ARTIST1: {TRACK1: popularity1, TRACK2: popularity2, ...}, ARTIST2: {TRACK1: popularity1, TRACK2: popularity2, ...}, ...}
def track_popularity_out(file_in, file_out):

    with open(file_in, 'r') as f_in:
        data = json.load(f_in)

    tagged_data = {}

    for artist in data:
        tagged_data[artist] = track_popularity(artist)

    with open(file_out, 'w') as f_out:
        json.dump(tagged_data, f_out)

    f_in.close()
    f_out.close()

    return
