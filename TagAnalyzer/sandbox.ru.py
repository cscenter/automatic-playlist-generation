import matplotlib.pyplot as plt
from collections import defaultdict
from dataproviders import HardDriveProvider
from scipy import cluster

dp = HardDriveProvider('music')
artist_tags = defaultdict(lambda: [])
song_tags = defaultdict(lambda: [])
artist_plays = defaultdict(lambda: 0)
track_plays = defaultdict(lambda: 0)
track_listeners = defaultdict(lambda: 0)
album_listeners = defaultdict(lambda: 0)
album_plays = defaultdict(lambda: 0)
song_to_album = defaultdict(lambda: '')
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
    if song_fm:
        artist_title = song_fm['artist']
        album_title = song_fm['album']
        song_to_album[song_path] = album_title
        artist_plays[artist_title] += int(song_fm['trackplaycount'])
        track_plays[song_path] += int(song_fm['trackplaycount'])
        track_listeners[song_path] += int(song_fm['tracklisteners'])
        album_listeners[album_title] += int(song_fm['albumlisteners'])
        album_plays[album_title] += int(song_fm['albumplaycount'])
        artist_tags[artist_title].extend(song_fm['artisttags'])
        artist_tags[artist_title].extend(song_fm['albumtags'])
        artist_tags[artist_title].extend(song_fm['artistsimilar'])
        song_tags[song_path].extend(song_fm['tracktags'])
        song_tags[song_path].extend(song_fm['tracksimtags'])
        song_tags[song_path].extend(song_fm['tracksimilar'])

ap = [e for e in artist_plays.values()]
plt.plot(ap)
plt.show()

tp = [e for e in track_plays.values()]
plt.plot(range(len(track_plays)), tp)
plt.show()

trp = [e for e in track_listeners.values()]
plt.plot(range(len(track_plays)), trp)
plt.show()


def show_kmeans(tests):
    plt.plot(tests)
    plt.show()
    initial = [cluster.vq.kmeans(tests, i) for i in range(1, 10)]
    plt.plot([var for (cent,var) in initial])
    plt.show()
