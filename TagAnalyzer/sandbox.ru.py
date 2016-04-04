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
        album_title = song_fm['album']
        if album_title:
            song_to_album[song_path] = album_title
            album_listeners[album_title] += int(song_fm['albumlisteners'])
            album_plays[album_title] += int(song_fm['albumplaycount'])

        artist_title = song_fm['artist']
        if artist_title:
            artist_plays[artist_title] += int(song_fm['trackplaycount'])
            artist_tags[artist_title].extend(song_fm['artisttags'])
            artist_tags[artist_title].extend(song_fm['albumtags'])
            artist_tags[artist_title].extend(song_fm['artistsimilar'])

        track_plays[song_path] += int(song_fm['trackplaycount'])
        track_listeners[song_path] += int(song_fm['tracklisteners'])
        song_tags[song_path].extend(song_fm['tracktags'])
        song_tags[song_path].extend(song_fm['tracksimtags'])
        song_tags[song_path].extend(song_fm['tracksimilar'])


def show_kmeans(tests_dict, title='songs'):
    # plt.plot(tests)
    # plt.show()
    # plt.plot([var for (cent, var) in initial])
    # plt.show()
    # use vq() to get as assignment for each obs.
    tests = list(map(float, tests_dict.values()))
    initial = [cluster.vq.kmeans(tests, i) for i in range(1, 10)]
    cent, var = initial[3]
    assignment, cdist = cluster.vq.vq(tests, cent)
    plt.scatter(range(len(tests)), tests, c=assignment)
    plt.title(title)
    plt.show()

# local vs general on last fm

# ap = list(map(float, artist_plays.values()))
show_kmeans(artist_plays, 'artist_plays')

# tp = list(map(float, track_plays.values()))
show_kmeans(track_plays, 'track_plays')

# trp = list(map(float, track_listeners.values()))
show_kmeans(track_listeners, 'track_listeners')

show_kmeans(album_listeners, 'album_listeners')

show_kmeans(album_plays, 'album_plays')
