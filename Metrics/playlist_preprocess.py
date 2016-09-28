from correction import *
from lastfm_tags import *


# плейлист формата pl = [[artist_1, title_1], [artist_2, title_2], ... ]
# коррекция плейлиста, затем сбор для него тегов lastfm:
# artist_ tags = [[tags for artist_1], [tags for artist_2], ...]. аналогично track_tags
# если теги уже есть, подгрузить их


def correct_playlist(playlist):

    l_pl = len(playlist)

    for i in range(l_pl):
        track = playlist[i]
        track[0] = correct_artist(track[0])
        track[1] = correct_title(track[0], track[1])

        playlist[i] = track
        
    return playlist


def tag_track(playlist, in_file = 0):

    if in_file:
        print("later")
        # обработка json, когда будет понятен формат записи

    else:

        l_pl = len(playlist)
        tr_tags = [""] * l_pl
    
        for i in range(l_pl):

            track = playlist[i]
            print(track, track[0], track[1])
            tags = track_tags(track[0], track[1])

            tr_tags[i] = tags
                  
    return tr_tags




def tag_artist(playlist, in_file = 0):

    if in_file:
        print("later")
        # обработка json, когда будет понятен формат записи

    else:

        l_pl = len(playlist)
        art_tags = [""] * l_pl
    
        for i in range(l_pl):

            track = playlist[i]
            tags = artist_tags(track[0])

            art_tags[i] = tags
                 
    return art_tags

