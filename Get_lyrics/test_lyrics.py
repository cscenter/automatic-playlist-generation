import sys
from mutagen.id3 import ID3
from collections import Counter
from get_lyrics import get_lyrics_wikia, get_lyrics_metro
import difflib


paths = ["01 Black Dog.mp3", "02 A Beautiful Lie.mp3", "02 Edge of the Earth.mp3", "03 The Kill.mp3", "05 The Fantasy.mp3", "10 93 Million Miles.mp3", "1-02 Paint It Black.mp3", "07 bad to the bone.mp3", "11 Wake Me Up When September Ends.mp3" ]


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
        return True
    else:
        return False

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
    max_len = max(len(counter_1), len(counter_2))
    
    if (len(shared)> max_len/3):
        return True
    else:
        return False      

        
for path in paths:

    audio = ID3(path)
    artist_name = audio['TPE1'].text[0]
    title_name = audio['TIT2'].text[0]

    print(artist_name)
    print(title_name)
    
    lyrics_w = get_lyrics_wikia(title_name, artist_name, 1)

    if (lyrics_w == ""):
        lyrics_w = get_lyrics_metro(title_name, artist_name, 1)   
    
    lyrics_id3 = get_lyrics_id3(path)

    if (lyrics_id3 != ""):

        if test_count(lyrics_w, lyrics_id3):
            print("OK")
        elif test_count(lyrics_w, lyrics_id3):
            print("OK")
        else:
            print("Not OK")
    else:
        print("No lyrics at ID3")

