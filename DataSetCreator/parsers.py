import eyed3


def coroutine(gen):
    @wraps(gen)
    def inner(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g

    return inner


@coroutine
def echo_nest_update(json_data):
    """
    Updates the json with all EchoNest data available for this song
    :param json_data: json object to update """
    pass


@coroutine
def essentia_update(json_data):
    """
    Updates the json with all Essentia data available for this song
    :param json_data: json object to update """
    pass


@coroutine
def last_fm_update(json_data):
    """
    Updates the json with all Last.FM data available for this song
    :param json_data: json object to update """
    pass


@coroutine
def lyrics_update(json_data):
    """
    TODO: update the json_data object with lyrics
    something like this:
    json_data[...] = get_lyrics(json_data['id'])
    :param json_data: json object to update """
    pass


@coroutine
def id3_v2_update(json_data):
    """
    Updates the json with all ID3v2 tags available for this song
    import eyed3 required
    :param json_data: json object to update """
    pass
