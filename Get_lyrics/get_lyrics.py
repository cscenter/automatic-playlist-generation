from bs4 import BeautifulSoup
import urllib.request



def get_lyrics_wikia(title_name, artist_name):

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



# http://search.azlyrics.com temporarily unavaible


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

        for script in lyrics_soup(["script", "style"]):
            script.extract()   

        text = lyrics_soup.get_text()

        lines = (line.strip() for line in text.splitlines())

        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

        text = '\n'.join(chunk for chunk in chunks if chunk)

        ind_start = text.find('Print') + 6
        ind_end = text.find('Submit Corrections') - 1

        lyrics = text[ind_start:ind_end]

    else:
        lyrics = ""

    return lyrics



