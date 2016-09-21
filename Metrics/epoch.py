from correction import *
from lastfm_tags import *


def track_epoch(artist_1, title_1, artist_2, title_2, correction = 1):
    if correction:
        artist_1 = correct_artist(artist_1)
        artist_2 = correct_artist(artist_2)
        title_1 = correct_title(artist_1_corr, title_1)
        title_2 = correct_title(artist_2_corr, title_2)         

    tags_1 = track_tags(artist_1, title_1)
    tags_2 = track_tags(artist_2, title_2)
    epoch_1 = epoch_in_tags(tags_1)
    epoch_2 = epoch_in_tags(tags_2)

    if(epoch_1 == {0}):
        tags_1_artist = artist_tags(artist_1)
        epoch_1 = epoch_in_tags(tags_1_artist)
        

    if(epoch_2 == {0}):
        tags_2_artist = artist_tags(artist_2)
        epoch_2 = epoch_in_tags(tags_2_artist)      


    if ((epoch_1 == {0}) or (epoch_2 == {0})):
        print('No epoch tag for artist')
        res = 0

    else:
        res = 1 - epoch_diff(epoch_1, epoch_2)
        
    return res
    

def epoch_in_tags(tags, to_find = '0s'):

    tags_out = set()

    for key in tags:
        ind = key.find(to_find)
        year = 0
        if (ind != -1):
            first_num = key[ind-1]
            if (first_num == '0'):
                year == 2000
            elif (first_num == '1'):
                year = 2010
            else:
                year = 1900 + 10*int(first_num)
            tags_out.add(year)
    return tags_out



def epoch_diff(epoch_1, epoch_2):
    
    res = 1

    for year_1 in epoch_1:
        for year_2 in epoch_2:
            tmp = abs(year_1 - year_2)/100.0
            if (tmp < res):
                res = tmp
    return res


    
