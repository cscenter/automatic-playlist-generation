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
                                                 'TLEN', 'TIT1', 'TPE2',
                                                 'TPE3', 'TPE4', 'TCOM',
                                                 'TEXT', 'USLT']:
                    print(t, tags[t])

            def get_tag_or_default(tag):
                return ','.join(map(str, tags[tag].text))\
                    if tag in tags else ""

            json_data['id3']['genre2'] = get_tag_or_default('TIT1')
            json_data['id3']['title'] = get_tag_or_default('TIT2')
            json_data['id3']['artist'] = get_tag_or_default('TPE1')
            json_data['id3']['composer'] = get_tag_or_default('TCOM')
            json_data['id3']['text_writer'] = get_tag_or_default('TEXT')
            json_data['id3']['artist2'] = get_tag_or_default('TPE2')
            json_data['id3']['artist3'] = get_tag_or_default('TPE3')
            json_data['id3']['artist4'] = get_tag_or_default('TPE4')
            json_data['id3']['album'] = get_tag_or_default('TALB')
            json_data['id3']['year'] = get_tag_or_default('TDRC')
            json_data['id3']['genre'] = get_tag_or_default('TCON')
            json_data['id3']['track number'] = get_tag_or_default('TRCK')
            json_data['id3']['length'] = get_tag_or_default('TLEN')
            json_data['id3']['lyrics'] = get_tag_or_default('USLT')

        except ID3NoHeaderError:
            pass
