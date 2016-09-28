
   # коррекция и сбор тегов в playlist_preprocess


    # эпоха

def track_epoch(tags_1, tags_2, tags_1_artist, tags_2_artist):


    epoch_1 = epoch_in_tags(tags_1)
    epoch_2 = epoch_in_tags(tags_2)

    if(epoch_1 == {0}):
        epoch_1 = epoch_in_tags(tags_1_artist)

    if(epoch_2 == {0}):
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
                year = 2000
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

# пол вокалиста

def track_gender(tags_1, tags_2, tags_1_artist, tags_2_artist):

    g_1 = gender_in_tags(tags_1)
    if (g_1 == -1):
        g_1 = gender_in_tags(tags_1_artist)

    g_2 = gender_in_tags(tags_2)
    if (g_1 == -2):
        g_2 = gender_in_tags(tags_2_artist)

    if (g_1 == g_2):
        return 1
    else:
        return 0


def gender_in_tags(tags):

       g = -1

       for key in tags:
           ind_m = key.find('male')
           if (ind_m != -1):
               ind_f = key.find('female')
               if (ind_f != -1):
                   g = 0
               else:
                   g = 1

        return g

# страна. наверное, проще с quantone, там есть конкретно страна, в lastfm её найти тяжело






