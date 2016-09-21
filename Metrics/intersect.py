from scipy import spatial
from correction import *
from lastfm_tags import *


def intersect_track_tags(artist_1, title_1, artist_2, title_2, correction = 1):

    if correction:
        artist_1 = correct_artist(artist_1)
        artist_2 = correct_artist(artist_2)
        title_1 = correct_title(artist_1_corr, title_1)
        title_2 = correct_title(artist_2_corr, title_2)   

    tags_1 = track_tags(artist_1, title_1)
    tags_2 = track_tags(artist_2, title_2)

    tags = set()
    tags.update(tags_1.keys())
        
    for key in tags_2: 
        tags.add(key)
    
    l_t = len(tags)

    vector_1 = [0]*l_t
    vector_2 = [0]*l_t

    i = 0
    
    for tag in tags:
        try:
            vector_1[i] = int(tags_1[tag])

        except:
            vector_1[i] = 0
            
        try:
            vector_2[i] = int(tags_2[tag])

        except:
            vector_2[i] = 0

        i += 1

    res = 1 - spatial.distance.cosine(vector_1, vector_2)

    return res


    

def intersect_artist_tags(artist_1, artist_2, correction = 1):
    if correction:
        artist_1 = correct_artist(artist_1)
        artist_2 = correct_artist(artist_2)

    tags_1 = artist_tags(artist_1)
    tags_2 = artist_tags(artist_2)

    tags = set()
    tags.update(tags_1.keys())
        
    for key in tags_2:  
        tags.add(key)
    
    l_t = len(tags)

    vector_1 = [0]*l_t
    vector_2 = [0]*l_t


    i = 0
    for tag in tags:
        try:
            vector_1[i] = int(tags_1[tag])

        except:
            vector_1[i] = 0
            
        try:
            vector_2[i] = int(tags_2[tag])

        except:
            vector_2[i] = 0

        i += 1

    res = 1 - spatial.distance.cosine(vector_1, vector_2)

    return res
 

