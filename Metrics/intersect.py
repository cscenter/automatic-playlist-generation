from scipy import spatial
from correction import *
from lastfm_tags import *


def intersect_track_tags(tags_1, tags_2):

    # коррекция и сбор тегов в playlist_preprocess

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


