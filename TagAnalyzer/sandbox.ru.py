from collections import defaultdict

from dataproviders import HardDriveProvider

dp = HardDriveProvider('music')
artist_tags = defaultdict(lambda: [])
song_tags = defaultdict(lambda: [])
for song_path in dp.get_all():
    song = dp.get_by_id(song_path)

    song_id3 = song['id3']
    if song_id3:
        artist_title = song_id3['artist']
        s_tags = [tag_str.strip() for tag_str in
                  song_id3['genre'].split(';')]
        song_tags[song_path].extend(s_tags)
        artist_tags[artist_title].extend(s_tags)

    song_fm = song['lastfm']
    for t in song_fm:
        artist_title = song_fm['artist']
        artist_tags[artist_title].extend(song_fm['artisttags'])
        artist_tags[artist_title].extend(song_fm['albumtags'])
        artist_tags[artist_title].extend(song_fm['artistsimilar'])
        song_tags[song_path].extend(song_fm['tracktags'])
        song_tags[song_path].extend(song_fm['tracksimtags'])
        song_tags[song_path].extend(song_fm['tracksimilar'])

# '''
# trackplaycount
# tracklisteners
# albumlisteners
# albumplaycount
# '''
