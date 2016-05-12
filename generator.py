from collections import defaultdict
from DataSetCreator.dataproviders import HardDriveProvider


def flatten_dataset(json_data):
    result = defaultdict(lambda: None)
    if 'id3' in json_data:
        id3_data = json_data['id3']
        result['id3_title'] = id3_data.get('title', None)
        result['id3_album'] = id3_data.get('album', None)
        result['id3_artist'] = id3_data.get('artist', None)
        result['id3_artist2'] = id3_data.get('artist2', None)
        result['id3_artist3'] = id3_data.get('artist3', None)
        result['id3_artist4'] = id3_data.get('artist4', None)
        result['id3_genre'] = id3_data.get('genre', None)
        result['id3_genre2'] = id3_data.get('genre2', None)
        result['id3_lyrics'] = id3_data.get('lyrics', None)
        # result['id3_length'] = id3_data.get('length', None)
        # result['id3_track_number'] = id3_data.get('track number', None)
        # result['id3_composer'] = id3_data.get('composer', None)
        # result['id3_text_writer'] = id3_data.get('text_writer', None)
        # result['id3_year'] = id3_data.get('year', None)
    if 'lastfm' in json_data:
        last_data = json_data['lastfm']
        result['last_artist'] = last_data.get('artist', None)
        result['last_artistsimilar'] = last_data.get('artistsimilar', None)
        result['last_artisttags'] = last_data.get('artisttags', None)
        # result['last_artistwiki'] = last_data.get('artistwiki', None)
        # result['last_artistwikisumm'] =
        #   last_data.get('artistwikisumm', None)
        result['last_album'] = last_data.get('album', None)
        result['last_albumlisteners'] = last_data.get('albumlisteners', None)
        result['last_albumplaycount'] = last_data.get('albumplaycount', None)
        result['last_albumtags'] = last_data.get('albumtags', None)
        # result['last_artistwiki'] = last_data.get('artistwiki', None)
        # result['last_albumwikisumm'] = last_data.get('albumwikisumm', None)
        result['last_track'] = last_data.get('track', None)
        result['last_tracklisteners'] = last_data.get('tracklisteners', None)
        result['last_trackplaycount'] = last_data.get('trackplaycount', None)
        result['last_tracktags'] = last_data.get('tracktags', None)
        result['last_tracksimilar'] = last_data.get('tracksimilar', None)
        # result['last_trackwiki'] = last_data.get('trackwiki', None)
        # result['last_trackwikisumm'] = last_data.get('trackwikisumm', None)
        result['last_tracksimtags'] = last_data.get('tracksimtags', None)
    if 'echo_nest' in json_data:
        echo_data = json_data['echo_nest']
        result['echo_artist_id'] = echo_data.get('artist_id', None)
        result['echo_artist'] = echo_data.get('artist', None)
        # result['echo_bios'] = echo_data.get('bios', None)
        # result['echo_blogs'] = echo_data.get('blogs', None)
        result['echo_doc_counts'] = echo_data.get('doc_counts', None)
        result['echo_a_familiarity'] = echo_data.get('a_familiarity', None)
        result['echo_a_hotttnesss'] = echo_data.get('a_hotttnesss', None)
        # result['echo_news'] = echo_data.get('news', None)
        # result['echo_reviews'] = echo_data.get('reviews', None)
        # result['echo_urls'] = echo_data.get('urls', None)
        # result['echo_years_active'] = echo_data.get('years_active', None)
        result['echo_similar'] = echo_data.get('similar', None)
        result['echo_summary'] = echo_data.get('summary', None)
        result['echo_s_hotttnesss'] = echo_data.get('s_hotttnesss', None)
        result['echo_s_discovery'] = echo_data.get('s_discovery', None)
        result['echo_analysis'] = echo_data.get('analysis', None)
        result['echo_basic_list'] = echo_data.get('basic_song_list', None)
        result['echo_basic_list'] = echo_data.get('basic_artist_list', None)
    return result

dp = HardDriveProvider('music')
for song_path in dp.data:
    song = flatten_dataset(dp.get_by_id(song_path))
