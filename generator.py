import os
import random
from collections import defaultdict
from DataSetCreator.dataproviders import HardDriveProvider
from mutagen import MutagenError
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4


def flatten_dataset(json_data):
    result = defaultdict(lambda: None)
    result['path'] = json_data['path']
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
        result['id3_length'] = id3_data.get('length', None)
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
        """
        'acousticness' (617595596592) = {float} 0.052235
'analysis_url' (617595596720) = {str} 'http://echonest-analysis.s3.amazonaws.com/TR/gxKjmQF8a0Ew2ZnElpzYAJQFYMx84un3Jq6bTWxKyKmFJRif5pBaedbnYJCmgS7obOcPXoHSXQ8a6d7Dc%3D/3/full.json?AWSAccessKeyId=AKIAJRDFEY23UEVW42BQ&Expires=1461799538&Signature=/GaF%2BABJrcsoQA/2M93Nl2cUXGE%3D'
'audio_md5' (617595596464) = {str} ''
'danceability' (617595625520) = {float} 0.16377
'duration' (617595596400) = {float} 360.68
'energy' (617595609472) = {float} 0.792323
'instrumentalness' (617595606840) = {float} 0.001548
'key' (617595609640) = {int} 1
'liveness' (617595596656) = {float} 0.043472
'loudness' (617595596528) = {float} -4.281
'mode' (617595609584) = {int} 0
'speechiness' (617595596272) = {float} 0.045882
'tempo' (617595609528) = {float} 172.737
'time_signature' (617595596336) = {int} 3
'valence' (617595609696) = {float} 0.319538

'audio' (617595609920) = {int} 24
'biographies' (617595626800) = {int} 12
'blogs' (617595609752) = {int} 8092
'images' (617595609864) = {int} 271
'news' (617595609416) = {int} 3056
'reviews' (617586743312) = {int} 153
'songs' (617595609976) = {int} 219
'video' (617595609808) = {int} 839
        """
    return result

FORMAT_DESCRIPTOR = "#EXTM3U"
RECORD_MARKER = "#EXTINF"

dp = HardDriveProvider('music')
dataset = {}
for song_path in dp.data:
    dataset[song_path] = flatten_dataset(dp.get_by_id(song_path))
all_tracks = list(dataset.keys())
seed_song = dataset[random.choice(all_tracks)]
selected = set()
selected.add(seed_song['path'])
with open('result.m3u', 'w') as fp:
    fp.write(FORMAT_DESCRIPTOR + "\n")
    for _ in range(15):
        audio = None
        track_length = -1
        track = seed_song['path']
        try:
            audio = MP3(track)
        except MutagenError:
            audio = MP4(track)
        track_length = audio.info.length
        artist = seed_song.get('last_artist', seed_song.get('id3_artist', ''))
        title = seed_song.get('last_track', seed_song.get('id3_title', ''))
        if artist and title:
            fp.write("{}:{},{} - {}\n".format(
                RECORD_MARKER, track_length, artist, title))
        else:
            fp.write("{}:{},{} - {}\n".format(
                RECORD_MARKER, track_length, os.path.basename(track)[:-4]))
        fp.write(track + "\n")
        while seed_song['path'] in selected:
            seed_song = dataset[random.choice(all_tracks)]
        selected.add(seed_song['path'])
