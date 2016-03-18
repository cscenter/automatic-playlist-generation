from mutagen.ID3 import ID3
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


@coroutine
def essentia_update():
    """
    Updates the json with all Essentia data available for this song """
    while True:
        json_data = yield
        if json_data == STOP:
            break


@coroutine
def last_fm_update():
    """
    Updates the json with all Last.FM data available for this song """
    while True:
        json_data = yield
        if json_data == STOP:
            break


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


@coroutine
def id3_v2_update():
    """
    Updates the json with all ID3v2 tags available for this song
    mutagen package required """
    while True:
        json_data = yield
        if json_data == STOP:
            break
        tags = ID3(json_data['path'])
        print(tags)
