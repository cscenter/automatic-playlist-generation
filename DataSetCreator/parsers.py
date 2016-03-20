from mutagen.id3 import ID3, ID3NoHeaderError
from functools import wraps

STOP = object()


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
        json_data['echo_nest'] = []


@coroutine
def essentia_update():
    """
    Updates the json with all Essentia data available for this song """
    while True:
        json_data = yield
        if json_data == STOP:
            break
        json_data['essentia'] = []


@coroutine
def last_fm_update():
    """
    Updates the json with all Last.FM data available for this song """
    while True:
        json_data = yield
        if json_data == STOP:
            break
        json_data['lastfm'] = []


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
        json_data['lyrics'] = []


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
                                                 'TLEN']:
                    print(t, tags[t])
            json_data['id3']['title'] = tags.get('TIT2', "")
            json_data['id3']['artist'] = tags.get('TPE1', "")
            json_data['id3']['album'] = tags.get('TALB', "")
            json_data['id3']['year'] = tags.get('TDRC', "")
            json_data['id3']['genre'] = tags.get('TCON', "")
            json_data['id3']['track number'] = tags.get('TRCK', "")
            json_data['id3']['length'] = tags.get('TLEN', "")

        except ID3NoHeaderError:
            pass
