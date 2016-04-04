from bs4 import BeautifulSoup
import urllib.request
import sys
import json


path = "music.json"
no_lyr = "T [["


def get_lyrics(title_name, artist_name):

    api_url = "http://lyrics.wikia.com/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles="

    title_good = (title_name.title()).replace(" ", "_")
    artist_good = (artist_name.title()).replace(" ", "_")
    track_name = artist_good + ":" + title_good

    search_str = api_url + track_name
    search_page = urllib.request.urlopen(search_str)
    search_soup = BeautifulSoup(search_page)

    text_soup = search_soup.get_text()
    ind_start = text_soup.find("<lyrics>") + 9
    ind_end = text_soup.find("</lyrics>") - 1

    lyrics = text_soup[ind_start:ind_end]

    return lyrics



def get_lyrics_az(title_name, artist_name):
    track_query =(artist_name.lower()).replace(" ", "+") + "+" + (title_name.lower()).replace(" ", "+")

    search_common = "http://search.azlyrics.com/search.php?q="
    search_str = search_common + track_query
    search_page = urllib.request.urlopen(search_str)
    search_soup = BeautifulSoup(search_page)

    find_ref = "http://www.azlyrics.com/lyrics/"

    # return first ref with lyrics from azlyrics.com

    lyrics_ref = None

    for link in search_soup.findAll('a'):
        ref_str = link.get('href')
        if (ref_str.find(find_ref) != -1):
            lyrics_ref = ref_str
            break


    if (lyrics_ref != None):
    
        lyrics_page = urllib.request.urlopen(lyrics_ref)
        lyrics_soup = BeautifulSoup(lyrics_page)

        # getting text, http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
    
        # kill all script and style elements
        for script in lyrics_soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = lyrics_soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each


        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        ind_start = text.find('Print') + 6
        ind_end = text.find('Submit Corrections') - 1

        lyrics = text[ind_start:ind_end]

    else:
        lyrics = ""

    return lyrics





with open(path, encoding="utf-8", errors="surrogateescape") as data_file:    
    data = json.load(data_file)


for key in data:
    tmp =  data[key]
    if "id3" in tmp:
        id = tmp["id3"]
        if ("artist" in id) and ("title" in id):
            artist_name =  id["artist"]
            title_name = id["title"]

            lyr = get_lyrics(title_name, artist_name)

            if lyr[0:4] != no_lyr:
                id["lyrics"] = lyr
                
            else:
                lyr_2 = get_lyrics_az(title_name, artist_name)
 
                if lyr_2 != "":
                    id["lyrics"] = lyr_2
        
            with open(path, 'w', encoding="utf-8", errors="surrogateescape") as data_w:
                data_w.write(json.dumps(data))
