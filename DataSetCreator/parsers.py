# import librosa
import pylast
import socket
import time
# from essentia.standard import *
from functools import wraps
from mutagen.id3 import ID3, MutagenError
from passwords import *
from pyechonest.util import EchoNestException
from pyechonest import artist, playlist, song, track

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
    Updates the json with all EchoNest data available for this song
    ('Echo Nest API Error 5: bucket - Invalid parameter:
    bucket "id" is not one of "audio", "biographies", "blogs", "doc_counts",
    "familiarity", "familiarity_rank", "genre", "hotttnesss",
    "hotttnesss_rank", "discovery", "discovery_rank", "images",
    "artist_location", "news", "reviews", "songs", "terms", "urls", "video",
    "years_active", "id:7digital-US", "id:7digital-AU", "id:7digital-UK",
    "id:facebook", "id:fma", "id:emi_bluenote", "id:emi_artists",
    "id:twitter", "id:spotify-WW", "id:seatwave",
    "id:lyricfind-US", "id:jambase", "id:musixmatch-WW", "id:rdio-US",
    "id:rdio-AT", "id:rdio-AU", "id:rdio-BR", "id:rdio-CA", "id:rdio-CH",
    "id:rdio-DE", "id:rdio-DK", "id:rdio-ES", "id:rdio-FI", "id:rdio-FR",
    "id:rdio-IE", "id:rdio-IT", "id:rdio-NL", "id:rdio-NO", "id:rdio-NZ",
    "id:rdio-PT", "id:rdio-SE", "id:emi_electrospective", "id:rdio-EE",
    "id:rdio-LT", "id:rdio-LV", "id:rdio-IS", "id:rdio-BE", "id:rdio-MX",
    "id:seatgeek", "id:rdio-GB", "id:rdio-CZ", "id:rdio-CO", "id:rdio-PL",
    "id:rdio-MY", "id:rdio-HK", "id:rdio-CL", "id:twitter_numeric",
    "id:7digital-ES", "id:openaura", "id:spotify", "id:spotify-WW",
    "id:tumblr", or "id:<CATALOG ID>"
    """

    from pyechonest import config
    config.ECHO_NEST_API_KEY = ECHO_NEST_API_KEY
    config.CALL_TIMEOUT = 60
    while True:
        json_data = yield
        if json_data == STOP:
            break
        if json_data.get('echo_nest', ''):
            continue
        json_data['echo_nest'] = {}
        track_title = ''
        artist_name = ''
        if json_data['lastfm']:
            track_title = json_data['lastfm'].get('track', '')
            artist_name = json_data['lastfm'].get('artist', '')
        if not track_title:
            track_title = json_data['id3'].get('title', '')
        if not artist_name:
            artist_name = json_data['id3'].get('artist', '')

        try:
            if artist_name:
                a = artist.Artist(artist_name,
                                  buckets=['biographies', 'blogs',
                                           'doc_counts', 'familiarity',
                                           'familiarity_rank', 'genre',
                                           'hotttnesss', 'hotttnesss_rank',
                                           'artist_location', 'news',
                                           'reviews', 'terms', 'urls',
                                           'years_active'])
                json_data['echo_nest']['artist_id'] = a.id
                json_data['echo_nest']['artist'] = a.name
                json_data['echo_nest']['bios'] = a.biographies
                json_data['echo_nest']['blogs'] = a.blogs
                json_data['echo_nest']['doc_counts'] = a.doc_counts
                json_data['echo_nest']['familiarity'] = a.familiarity
                json_data['echo_nest']['familiarity_rank'] = a.familiarity
                json_data['echo_nest']['hotttnesss'] = a.hotttnesss
                json_data['echo_nest']['hotttnesss_rank'] = a.hotttnesss_rank
                json_data['echo_nest']['location'] = a.artist_location
                json_data['echo_nest']['news'] = a.news
                json_data['echo_nest']['reviews'] = a.reviews
                json_data['echo_nest']['terms'] = a.terms
                json_data['echo_nest']['urls'] = a.urls
                json_data['echo_nest']['years_active'] = a.years_active
                time.sleep(1)
                json_data['echo_nest']['similar'] = a.get_similar()
                json_data['echo_nest']['genre'] = a.list_genres()
        except EchoNestException as e:
            print(e)
        except socket.timeout:
            pass
        else:
            time.sleep(1)

        if artist_name or track_title:
            try:
                json_data['echo_nest']['basic_artist_list'] =\
                    playlist.basic(artist=artist_name, song=track_title)
                json_data['echo_nest']['basic_song_list'] =\
                    playlist.basic(type='song-radio',
                                   artist=artist_name, song=track_title)
            except EchoNestException as e:
                print(e)
            except socket.timeout:
                pass
            else:
                time.sleep(1)

        if artist_name and track_title:
            results = song.search(artist=artist_name, title=track_title,
                                  buckets=['audio_summary', 'song_hotttnesss',
                                           'artist_familiarity',
                                           'song_discovery', 'song_currency'])
            if results:
                try:
                    json_data['echo_nest']['id'] = results[0].id
                    json_data['echo_nest']['summary'] =\
                        results[0].audio_summary
                    json_data['echo_nest']['hotttnesss'] =\
                        results[0].song_hotttnesss
                    json_data['echo_nest']['artist_familiarity'] =\
                        results[0].artist_familiarity
                    json_data['echo_nest']['discovery'] =\
                        results[0].song_discovery
                    json_data['echo_nest']['currency'] =\
                        results[0].song_currency
                except EchoNestException as e:
                    print(e)
                except socket.timeout:
                    pass
                else:
                    time.sleep(1)

            if json_data['echo_nest']['id']:
                try:
                    tr = track.track_from_id(json_data['echo_nest']['id'])
                    tr.get_analysis()
                    json_data['echo_nest']['analysis'] = {}
                    json_data['echo_nest']['analysis']['acousticness'] =\
                        tr.acousticness
                    json_data['echo_nest']['analysis']['analysis_url'] =\
                        tr.analysis_url
                    json_data['echo_nest']['analysis']['danceability'] =\
                        tr.danceability
                    json_data['echo_nest']['analysis']['duration'] =\
                        tr.duration
                    json_data['echo_nest']['analysis']['energy'] = tr.energy
                    json_data['echo_nest']['analysis']['key'] = tr.key
                    json_data['echo_nest']['analysis']['liveness'] =\
                        tr.liveness
                    json_data['echo_nest']['analysis']['loudness'] =\
                        tr.loudness
                    json_data['echo_nest']['analysis']['mode'] = tr.mode
                    json_data['echo_nest']['analysis']['speechiness'] =\
                        tr.speechiness
                    json_data['echo_nest']['analysis']['tempo'] =\
                        tr.tempo
                    json_data['echo_nest']['analysis']['time_signature'] =\
                        tr.time_signature
                    json_data['echo_nest']['analysis']['valence'] = tr.valence
                    json_data['echo_nest']['analysis']['analysis_channels'] =\
                        tr.analysis_channels
                    json_data['echo_nest']['analysis']['bars'] = tr.bars
                    json_data['echo_nest']['analysis']['beats'] = tr.beats
                    json_data['echo_nest']['analysis']['start_of_fade_out'] =\
                        tr.start_of_fade_out
                    json_data['echo_nest']['analysis']['end_of_fade_in'] =\
                        tr.end_of_fade_in
                    json_data['echo_nest']['analysis']['key_confidence'] =\
                        tr.key_confidence
                    json_data['echo_nest']['analysis']['meta'] = tr.meta
                    json_data['echo_nest']['analysis']['mode_confidence'] =\
                        tr.mode_confidence
                    json_data['echo_nest']['analysis']['num_samples'] =\
                        tr.num_samples
                    json_data['echo_nest']['analysis']['sections'] =\
                        tr.sections
                    json_data['echo_nest']['analysis']['segments'] =\
                        tr.segments
                    json_data['echo_nest']['analysis']['synchstring'] =\
                        tr.synchstring
                    json_data['echo_nest']['analysis']['tatums'] =\
                        tr.tatums
                    json_data['echo_nest']['analysis']['tempo_confidence'] =\
                        tr.tempo_confidence
                    json_data['echo_nest']['analysis']['sign_confidence'] =\
                        tr.time_signature_confidence
                except EchoNestException as e:
                    print(e)
                except socket.timeout:
                    pass
                except:
                    pass
                else:
                    time.sleep(1)


@coroutine
def essentia_update():
    """
    Updates the json with all Essentia data available for this song """
    pass
    # w = Windowing(type='blackman-harris')
    # fft = FFT()
    # extractors = {
    #     'mfcc': MFCC(),
    #     'dct': DCT(),
    #     'envelope': Envelope(),
    #     'peakdetection': PeakDetection(),
    #     'replaygain': ReplayGain(),
    #     'autocorrelation': AutoCorrelation(),
    #     'mean': Mean(),
    #     'geometricmean': GeometricMean(),
    #     'powermean': PowerMean(),
    #     'median': Median(),
    #     'energy': Energy()
    #     'rms': RMS(),
    #     'centralmoments': CentralMoments(),
    #     'rawmoments': RawMoments(),
    #     'variance': Variance(),
    #     'skewness': Skewness(),
    #     'kurtosis': Kurtosis(),
    #     'flatness': Flatness(),
    #     'crest': Crest(),
    #     'instantpower': InstantPower(),
    #     'iir': IIR(),
    #     'lowpass': LowPass(),
    #     'bandpass': BandPass(),
    #     'highpass': HighPass(),
    #     'bandreject': BandReject(),
    #     'equalloudness': EqualLoudness(),
    #     'barkbands': BarkBands(),
    #     'melbands': MelBands(),
    #     'erbbands': ERBBands(),
    #     'mfcc': MFCC(),
    #     'gfcc': GFCC(),
    #     'lpc': LPC(),
    #     'hfc': HFC(),
    #     'spectralcontrast': SpectralContrast(),
    #     'inharmonicity': Inharmonicity(),
    #     'dissonance': Dissonance(),
    #     'spectralwhitening': SpectralWhitening(),
    #     'panning': Panning(),
    #     'zcr': ZCR(),
    #     'leq': Leq(),
    #     'larm': LARM(),
    #     'loudness': Loudness(),
    #     'loudnessvicker': LoudnessVicker(),
    #     'pitchsaliencefunction': PitchSalienceFunction(),
    #     'predominantmelody': PredominantMelody(),
    #     'pitchyinfft': PitchYinFFT(),
    #     'hpcp': HPCP(),
    #     'tuningfrequency': TuningFrequency(),
    #     'key': Key(),
    #     'chordsdetection': ChordsDetection(),
    #     'chordsdescriptors': ChordsDescriptors(),
    #     'beattrackerdegara': BeatTrackerDegara(),
    #     'beattrackermultifeature': BeatTrackerMultiFeature(),
    #     'rhythmextractor2013': RhythmExtractor2013(),
    #     'bpmhistogramdescriptors': BpmHistogramDescriptors(),
    #     'noveltycurve': NoveltyCurve(),
    #     'onsetdetection': OnsetDetection(),
    #     'onsetdetectionglobal': OnsetDetectionGlobal(),
    #     'onsets': Onsets(),
    #     'rhythmtransform': RhythmTransform(),
    #     'beatsloudness': BeatsLoudness(),
    #     'logattacktime': LogAttackTime(),
    #     'maxtototal': MaxToTotal(),
    #     'mintototal': MinToTotal(),
    #     'pitchsalience': PitchSalience(),
    #     'tctototal': TCToTotal(),
    #     'danceability': Danceability(),
    #     'dynamiccomplexity': DynamicComplexity(),
    #     'fadedetection': FadeDetection(),
    #     'sbic': SBic(),
    #     'pca': PCA()
    # }
    #
    # while True:
    #     json_data = yield
    #     if json_data == STOP:
    #         break
    #     if json_data.get('essentia', ''):
    #         continue
    #     json_data['essentia'] = {}
    #     try:
    #         loader = MonoLoader(filename=json_data['path'])
    #         audio = loader()
    #         for frame in FrameGenerator(audio, frameSize=1024, hopSize=512):
    #             filtered = fft(w(frame))
    #             for extr in extractors:
    #                 json_data['essentia'][extr] = extractors[extr](filtered)
    #     except:
    #         pass


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
        if json_data.get('lastfm', ''):
            continue

        try:
            json_data['lastfm'] = {}
            title = json_data['id3'].get('title', '')
            artist_name = json_data['id3'].get('artist', '')
            album_title = json_data['id3'].get('album', '')
            if not artist_name:
                continue
            try:
                artist = network.get_artist(artist_name)
                if artist:
                    json_data['lastfm']['artist'] = artist.get_name()
                    json_data['lastfm']['artistsimilar'] =\
                        [a[0].get_name() for a in artist.get_similar()]
                    json_data['lastfm']['artisttags'] =\
                        [t[0].get_name() for t in artist.get_top_tags()]
                    json_data['lastfm']['artistwiki'] =\
                        artist.get_wiki_content()
                    json_data['lastfm']['artistwikisumm'] =\
                        artist.get_wiki_summary()
            except pylast.WSError as e:
                print(e)
            else:
                time.sleep(1)

            if album_title:
                try:
                    album = network.get_album(artist_name, album_title)
                    if album:
                        json_data['lastfm']['album'] = album.get_name()
                        json_data['lastfm']['albumlisteners'] =\
                            album.get_listener_count()
                        json_data['lastfm']['albumplaycount'] =\
                            album.get_playcount()
                        json_data['lastfm']['albumtags'] =\
                            [t[0].get_name() for t in album.get_top_tags()]
                        json_data['lastfm']['artistwiki'] =\
                            album.get_wiki_content()
                        json_data['lastfm']['albumwikisumm'] =\
                            album.get_wiki_summary()
                except pylast.WSError as e:
                    print(e)
                else:
                    time.sleep(1)

            if title:
                try:
                    trackinfo = network.get_track(artist_name, title)
                    if trackinfo:
                        sim_tracks = trackinfo.get_similar()
                        json_data['lastfm']['track'] = trackinfo.get_name()
                        json_data['lastfm']['tracklisteners'] =\
                            trackinfo.get_listener_count()
                        json_data['lastfm']['trackplaycount'] =\
                            trackinfo.get_playcount()
                        json_data['lastfm']['tracktags'] =\
                            [t[0].get_name() for t in trackinfo.get_top_tags()]
                        json_data['lastfm']['tracksimilar'] =\
                            [a[0].get_name() for a in sim_tracks]
                        json_data['lastfm']['trackwiki'] =\
                            trackinfo.get_wiki_content()
                        json_data['lastfm']['trackwikisumm'] =\
                            trackinfo.get_wiki_summary()
                        time.sleep(1)
                        similar_tags = set()
                        for chunk in chunks(sim_tracks, 5):
                            for sim_track in chunk:
                                try:
                                    similar_track = network.get_track(
                                        sim_track[0].get_artist(),
                                        sim_track[0].get_name())
                                    if similar_track:
                                        for tt in similar_track.get_top_tags():
                                            similar_tags.add(tt)
                                except pylast.WSError as e:
                                    print(e)
                            time.sleep(1)
                        json_data['lastfm']['tracksimtags'] =\
                            [t[0].get_name() for t in similar_tags]
                except pylast.WSError as e:
                    print(e)
        except pylast.NetworkError as e:
            print(e)
        except pylast.MalformedResponseError as e:
            print(e)


@coroutine
def librosa_update():
    """
    Updates the json with all Librosa data available for this song """
    while True:
        json_data = yield
        if json_data == STOP:
            break
        if json_data.get('librosa', ''):
            continue
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
        if json_data.get('lyrics', ''):
            continue
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

        if json_data.get('id3', ''):
            continue
        json_data['id3'] = {}
        try:
            json_data['path'] = json_data['path'].replace('._', '')
            print(json_data['path'])
            tags = ID3(json_data['path'])

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

        except MutagenError as e:
            print(e)
        except FileNotFoundError:
            pass
