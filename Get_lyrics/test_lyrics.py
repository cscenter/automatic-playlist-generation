import sys
from mutagen.id3 import ID3
from collections import Counter
from get_lyrics import get_lyrics_wikia
import difflib


path = "02_Creep.mp3"


def get_lyrics_id3(path):
    audio = ID3(path)

    lyr = audio.getall("USLT")
    lyrics_id3 = ""
    
    if len(lyr)>0:           # replace MacOS line separator with normal one
        lyrics_id3 = (lyr[0].text).replace("\r", "\n")

    return lyrics_id3


def test_diff(lyrics_1, lyrics_2):

    result = ''.join(difflib.unified_diff(lyrics_1, lyrics_2))  

    if (len(result) < len(lyrics_1)/2):        # number is questionable
        print("OK")
    else:
        print("Not OK")


    return   

def lyrics_to_list(txt):
    
    txt = txt.replace(",", "")
    txt = txt.replace(".", "")   
    txt = txt.replace("?", "")
    txt = txt.replace("-", "")   
    text = txt.split()

    return text
    

def test_count(lyrics_1, lyrics_2):

    lyr_1 = lyrics_to_list(lyrics_1)
    lyr_2 = lyrics_to_list(lyrics_2)
    
    counter_1 = Counter(lyr_1)
    counter_2 = Counter(lyr_2)

    shared = set(counter_1.items()) & set(counter_2.items())
    if (len(counter_1) - len(shared)) < 5:     # number is questionable
        print("OK")
    else:
        print("Not OK")        

        


audio = ID3(path)
artist_name = audio['TPE1'].text[0]
title_name = audio['TIT2'].text[0]

lyrics_w = get_lyrics_wikia(title_name, artist_name)
lyrics_id3 = get_lyrics_id3(path)

test_diff(lyrics_w, lyrics_id3)

test_count(lyrics_w, lyrics_id3)



