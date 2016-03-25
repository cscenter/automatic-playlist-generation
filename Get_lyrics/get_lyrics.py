from bs4 import BeautifulSoup
import urllib.request
import sys


track_name = input()
track_name_low = track_name.lower()
track_query = ""

for c in track_name_low:
    if c == ' ':
        c = '+'
    track_query = track_query + c


search_common = "http://search.azlyrics.com/search.php?q="
search_str = search_common + track_query
search_page = urllib.request.urlopen(search_str)
search_soup = BeautifulSoup(search_page)

find_ref = "http://www.azlyrics.com/lyrics/"

# return first ref with lyrics from azlyrics.com

lyrics_ref = None

for link in search_soup.findAll('a'):
    ref_str = link.get('href')
    if ref_str.find(find_ref) != -1:
        lyrics_ref = ref_str
        break


if lyrics_ref:
    lyrics_page = urllib.request.urlopen(lyrics_ref)
    lyrics_soup = BeautifulSoup(lyrics_page)
    # getting text, http://stackoverflow.com/q/1936466/213550
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

    file_lyrics = open(track_name, 'w')
    file_lyrics.write(text[ind_start:ind_end])

else:
    print('Improper trackname')
