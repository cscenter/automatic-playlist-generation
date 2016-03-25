# import librosa
import pylast
import pyechonest
import time
from functools import wraps
from mutagen.id3 import ID3, ID3NoHeaderError
from passwords import *

STOP = object()


def chunks(l, n):
    """Yield successive n-sized chunks from list.
    :param l: list to be chunked
    :param n: max size of each chunk
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def coroutine(gen):
    @wraps(gen)
    def inner(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g

    return inner


@coroutine
def echo_nest_update():
    """
    Updates the json with all EchoNest data available for this song """
    while True:
        json_data = yield
        if json_data == STOP:
            break
        json_data['echo_nest'] = {}


@coroutine
def essentia_update():
    """
    Updates the json with all Essentia data available for this song """
    while True:
        json_data = yield
        if json_data == STOP:
            break
        json_data['essentia'] = {}


@coroutine
def last_fm_update():
    """
    Updates the json with all Last.FM data available for this song """
    username = LAST_FM_USER
    password_hash = pylast.md5(LAST_FM_PASSWORD)
    network = pylast.LastFMNetwork(api_key=LAST_FM_API_KEY,
                                   api_secret=LAST_FM_API_SECRET,
                                   username=username,
                                   password_hash=password_hash)
    while True:
        json_data = yield
        if json_data == STOP:
            break

        json_data['lastfm'] = {}
        title = json_data['id3'].get('title', '')
        artist_name = json_data['id3'].get('artist', '')
        album_title = json_data['id3'].get('album', '')
        if artist_name:
            artist = network.get_artist(artist_name)
            if artist:
                json_data['lastfm']['artist'] = artist.get_name()
                json_data['lastfm']['artistsimilar'] =\
                    [a.get_name() for a in artist.get_similar()]
                json_data['lastfm']['artisttags'] =\
                    [t.get_name() for t in artist.get_top_tags()]
                json_data['lastfm']['artistwiki'] = artist.get_wiki_content()
                json_data['lastfm']['artistwikisumm'] =\
                    artist.get_wiki_summary()
        time.sleep(1)
        if album_title and artist_name:
            album = network.get_album(artist_name, album_title)
            if album:
                json_data['lastfm']['album'] = album.get_name()
                json_data['lastfm']['albumlisteners'] =\
                    album.get_listener_count()
                json_data['lastfm']['albumplaycount'] = album.get_playcount()
                json_data['lastfm']['albumtags'] =\
                    [t.get_name() for t in album.get_top_tags()]
                json_data['lastfm']['artistwiki'] = album.get_wiki_content()
                json_data['lastfm']['albumwikisumm'] = album.get_wiki_summary()
        time.sleep(1)
        if title and artist_name:
            track = network.get_track(artist_name, title)
            if track:
                sim_tracks = track.get_similar()
                json_data['lastfm']['track'] = track.get_name()
                json_data['lastfm']['tracklisteners'] =\
                    track.get_listener_count()
                json_data['lastfm']['trackplaycount'] = track.get_playcount()
                json_data['lastfm']['tracktags'] =\
                    [t.get_name() for t in track.get_top_tags()]
                json_data['lastfm']['tracksimilar'] =\
                    [a.get_name() for a in sim_tracks]
                json_data['lastfm']['trackwiki'] = track.get_wiki_content()
                json_data['lastfm']['trackwikisumm'] = track.get_wiki_summary()
                time.sleep(1)
                similar_tags = set()
                for chunk in chunks(sim_tracks, 5):
                    for sim_track in chunk:
                        similar_track = network.get_track(
                            sim_track.get_artist(), sim_track.get_name())
                        if similar_track:
                            similar_tags.add(similar_track.get_top_tags())
                    time.sleep(1)
                json_data['lastfm']['tracksimtags'] =\
                    [t.get_name() for t in similar_tags]


@coroutine
def librosa_update():
    """
    Updates the json with all Librosa data available for this song """
    while True:
        json_data = yield
        if json_data == STOP:
            break
        json_data['librosa'] = {}


@coroutine
def lyrics_update():
    """
    TODO: update the json_data object with lyrics
    something like this:
    json_data[...] = get_lyrics(json_data['id']) """
    while True:
        json_data = yield
        if json_data == STOP:
            break
        json_data['lyrics'] = {}


@coroutine
def id3_v2_update():
    """
    Updates the json with all ID3v2 tags available for this song
    mutagen package required """
    while True:
        json_data = yield
        if json_data == STOP:
            break

        json_data['id3'] = {}
        try:
            tags = ID3(json_data['path'])
            for t in tags:
                if 'PRIV' not in t and t not in ['TIT2', 'TPE1', 'TALB',
                                                 'TDRC', 'TCON', 'TRCK',
                                                 'TLEN', 'TIT1', 'TPE2',
                                                 'TPE3', 'TPE4', 'TCOM',
                                                 'TEXT', 'USLT']:
                    print(t, tags[t])

            def get_tag_or_default(tag):
                return ','.join(map(str, tags[tag].text)) \
                    if tag in tags else ""

            json_data['id3']['genre2'] = get_tag_or_default('TIT1')
            json_data['id3']['title'] = get_tag_or_default('TIT2')
            json_data['id3']['artist'] = get_tag_or_default('TPE1')
            json_data['id3']['album'] = get_tag_or_default('TALB')
            json_data['id3']['composer'] = get_tag_or_default('TCOM')
            json_data['id3']['text_writer'] = get_tag_or_default('TEXT')
            json_data['id3']['artist2'] = get_tag_or_default('TPE2')
            json_data['id3']['artist3'] = get_tag_or_default('TPE3')
            json_data['id3']['artist4'] = get_tag_or_default('TPE4')
            json_data['id3']['year'] = get_tag_or_default('TDRC')
            json_data['id3']['genre'] = get_tag_or_default('TCON')
            json_data['id3']['track number'] = get_tag_or_default('TRCK')
            json_data['id3']['length'] = get_tag_or_default('TLEN')
            json_data['id3']['lyrics'] = get_tag_or_default('USLT')

        except ID3NoHeaderError:
            pass
