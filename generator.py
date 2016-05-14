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
        dc = echo_data.get('doc_counts', None)
        if dc:
            result['echo_audio_counts'] = dc['audio']
            result['echo_bio_counts'] = dc['biographies']
            result['echo_blogs_counts'] = dc['blogs']
            result['echo_images_counts'] = dc['images']
            result['echo_news_counts'] = dc['news']
            result['echo_reviews_counts'] = dc['reviews']
            result['echo_songs_counts'] = dc['songs']
            result['echo_video_counts'] = dc['video']
        result['echo_a_familiarity'] = echo_data.get('a_familiarity', None)
        result['echo_a_hotttnesss'] = echo_data.get('a_hotttnesss', None)
        # result['echo_news'] = echo_data.get('news', None)
        # result['echo_reviews'] = echo_data.get('reviews', None)
        # result['echo_urls'] = echo_data.get('urls', None)
        # result['echo_years_active'] = echo_data.get('years_active', None)
        result['echo_similar'] = echo_data.get('similar', None)
        ds = echo_data.get('summary', None)
        if ds:
            result['echo_summary_acousticness'] = ds['acousticness']
            # result['echo_summary_analysis_url'] = ds['analysis_url']
            # result['echo_summary_audio_md5'] = ds['audio_md5']
            result['echo_summary_danceability'] = ds['danceability']
            result['echo_summary_duration'] = ds['duration']
            result['echo_summary_energy'] = ds['energy']
            result['echo_summary_instrumentalness'] = ds['instrumentalness']
            # result['echo_summary_key'] = ds['key']
            result['echo_summary_liveness'] = ds['liveness']
            result['echo_summary_loudness'] = ds['loudness']
            # result['echo_summary_mode'] = ds['mode']
            result['echo_summary_speechiness'] = ds['speechiness']
            result['echo_summary_tempo'] = ds['tempo']
            # result['echo_summary_time_signature'] = ds['time_signature']
            result['echo_summary_valence'] = ds['valence']
        result['echo_s_hotttnesss'] = echo_data.get('s_hotttnesss', None)
        result['echo_s_discovery'] = echo_data.get('s_discovery', None)
        result['echo_analysis'] = echo_data.get('analysis', None)
        result['echo_basic_list'] = echo_data.get('basic_song_list', None)
        result['echo_artist_list'] = echo_data.get('basic_artist_list', None)
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