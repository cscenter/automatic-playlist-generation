import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from dataproviders import HardDriveProvider
from gensim import corpora, models
from itertools import chain
from scipy import cluster

dp = HardDriveProvider('music')
artist_tags = defaultdict(lambda: Counter())
song_tags = defaultdict(lambda: Counter())

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
        song_tags[song_path].update(s_tags)
        artist_tags[artist_title].update(s_tags)

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
            artist_tags[artist_title].update(song_fm['artisttags'])
            artist_tags[artist_title].update(song_fm['albumtags'])
            artist_tags[artist_title].update(song_fm['artistsimilar'])

        track_plays[song_path] += int(song_fm['trackplaycount'])
        track_listeners[song_path] += int(song_fm['tracklisteners'])
        song_tags[song_path].update(song_fm['tracktags'])
        song_tags[song_path].update(song_fm['tracksimtags'])
        song_tags[song_path].update(song_fm['tracksimilar'])


def show_kmeans(tests_dict, title='songs'):
    # plt.plot(tests)
    # plt.show()
    # plt.plot([var for (cent, var) in initial])
    # plt.show()
    # use vq() to get as assignment for each obs.
    tests = list(map(float, tests_dict.values()))
    initial = [cluster.vq.kmeans(tests, k_count) for k_count in range(1, 10)]
    cent, var = initial[3]
    assignment, cdist = cluster.vq.vq(tests, cent)
    plt.scatter(range(len(tests)), tests, c=assignment)
    plt.title(title)
    plt.show()
# local vs general on last fm
# plt.scatter(list(map(float, track_plays.values())),
#             list(map(float, track_listeners.values())))
# plt.title('TracksPlays to Listeners')
# plt.show()
# plt.scatter(list(map(float, album_listeners.values())),
#             list(map(float, album_plays.values())))
# plt.title('Albums Plays to Listeners')
# plt.show()
# We should use plays
# ap = list(map(float, artist_plays.values()))
# show_kmeans(artist_plays, 'artist_plays')
# tp = list(map(float, track_plays.values()))
# show_kmeans(track_plays, 'track_plays')
# trp = list(map(float, track_listeners.values()))
# show_kmeans(track_listeners, 'track_listeners')
# show_kmeans(album_listeners, 'album_listeners')
# show_kmeans(album_plays, 'album_plays')


def get_tags(count):
    single_tags = [key for key, val in count.items() if val == 1]
    return count - Counter(single_tags)

filtered_counters = dict((k, get_tags(song_tags[k]))
                         for k in song_tags)
filtered_tags = dict((k, list(filtered_counters[k].keys()))
                     for k in filtered_counters)

tags = [[tag.lower() for tag in tag_list]
        for tag_list in filtered_tags.values()]
id2word = corpora.Dictionary(tags)
mm = [id2word.doc2bow(tag) for tag in tags]
thresholds_lsi = [None] * 20
thresholds_lem = [None] * 20
thresholds_rp = [None] * 20
thresholds_tfid = [None] * 20
for i in range(1, len(thresholds_lsi)):
    # lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=i,
    #                                update_every=1, chunksize=10000, passes=1)
    lsi = models.LsiModel(corpus=mm, id2word=id2word, num_topics=i,
                          chunksize=10000)
    lem = models.LogEntropyModel(corpus=mm, id2word=id2word)
    hdp = models.HdpModel(corpus=mm, id2word=id2word, chunksize=10000)
    rp = models.RpModel(corpus=mm, id2word=id2word)
    tfid = models.TfidfModel(corpus=mm, id2word=id2word)
    # for top in lda.print_topics():
    #     print(top)
    corpus = lsi[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_lsi[i] = sum(scores) / len(scores)
    corpus = lem[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_lem[i] = sum(scores) / len(scores)
    corpus = rp[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_rp[i] = sum(scores) / len(scores)
    corpus = tfid[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_tfid[i] = sum(scores) / len(scores)
    print(i)
print(thresholds_lsi)
print(thresholds_lem)
print(thresholds_rp)
print(thresholds_tfid)
# LdaModel
# [None, 1.0, 0.50185112172347246, 0.37102117690690567, 0.32754541315319685,
# 0.27994819275644189, 0.29434507120337638, 0.25852333441578412,
# 0.24296340025661164, 0.26793261866599827, 0.30434812815457662,
# 0.30758615422589169, 0.28047219146589708, 0.25287908852821783,
# 0.24293008986954681, 0.27578446186589273, 0.2508726112260441,
# 0.24455020952038972, 0.25014859299155795, 0.27160119369295266]
# [None, 15.942648137621468, 7.8980041848550515, 5.4546075079901897, 3.8171227146557976, 3.3216862720407097, 2.631634559673425, 2.2259715580470343, 1.8406300532488904, 1.7149004289682368, 1.6563132120598703, 1.5491354107014874, 1.3742701148276499, 1.298356134767733, 1.1448051520804472, 1.1293213975023044, 1.011956792840242, 0.91503472366352878, 0.96295887869177099, 0.83320234375382718]
# [None, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517]
# [None, 0.023650641895355054, -0.021141726603634385, 0.03829050107711446, -0.010466970389653496, 0.004466004085307028, -0.002255663695246276, -0.09860087494476572, -0.03699258709957529, 0.008808481515794327, 0.08268715921158676, 0.044739284680453455, -0.07066948803926842, -0.014647845286061995, -0.08072000910174265, 0.02252911011129369, -0.0625467364731131, 0.007121270892606006, 0.02133085479124043, -0.010965839717908571]
# [None, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877]

