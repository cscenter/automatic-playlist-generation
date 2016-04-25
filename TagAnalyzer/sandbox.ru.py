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
    most_tags = Counter()
    for k, v in count.most_common(3):
        most_tags[k] += v
    return count - Counter(single_tags)  # - Counter(most_tags)

filtered_counters = dict((k, get_tags(song_tags[k]))
                         for k in song_tags)
filtered_tags = dict((k, list(filtered_counters[k].keys()))
                     for k in filtered_counters)

tags = [[tag.lower() for tag in tag_list]
        for tag_list in filtered_tags.values()]
id2word = corpora.Dictionary(tags)
mm = [id2word.doc2bow(tag) for tag in tags]
thresholds_lda = [None] * 20
thresholds_lsi = [None] * 20
thresholds_lem = [None] * 20
thresholds_hdp = [None] * 20
thresholds_rp = [None] * 20
thresholds_tfid = [None] * 20
for i in range(2, len(thresholds_lsi)):
    lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=i,
                                   update_every=1, chunksize=10000, passes=1)
    lsi = models.LsiModel(corpus=mm, id2word=id2word, num_topics=i,
                          chunksize=10000)
    lem = models.LogEntropyModel(corpus=mm, id2word=id2word)
    hdp = models.HdpModel(corpus=mm, id2word=id2word, chunksize=10000)
    rp = models.RpModel(corpus=mm, id2word=id2word)
    tfid = models.TfidfModel(corpus=mm, id2word=id2word)

    corpus = lda[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_lda[i] = abs(sum(scores) / len(scores))
    corpus = lsi[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_lsi[i] = abs(sum(scores) / len(scores))
    corpus = lem[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_lem[i] = abs(sum(scores) / len(scores))
    corpus = hdp[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_hdp[i] = abs(sum(scores) / len(scores))
    corpus = rp[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_rp[i] = abs(sum(scores) / len(scores))
    corpus = tfid[mm]
    scores = list(chain(*[[score for topic_id, score in topic]
                          for topic in [doc for doc in corpus]]))
    thresholds_tfid[i] = abs(sum(scores) / len(scores))
    print(i)
print(thresholds_lda)
print(thresholds_lsi)
print(thresholds_lem)
print(thresholds_hdp)
print(thresholds_rp)
print(thresholds_tfid)
# LdaModel
# [None, 1.0, 0.50185112172347246, 0.37102117690690567, 0.32754541315319685,
# 0.27994819275644189, 0.29434507120337638, 0.25852333441578412,
# 0.24296340025661164, 0.26793261866599827, 0.30434812815457662,
# 0.30758615422589169, 0.28047219146589708, 0.25287908852821783,
# 0.24293008986954681, 0.27578446186589273, 0.2508726112260441,
# 0.24455020952038972, 0.25014859299155795, 0.27160119369295266]
# LsiModel
# [None, 15.942648137621468, 7.8980041848550515, 5.4546075079901897,
# 3.8171227146557976, 3.3216862720407097, 2.631634559673425,
# 2.2259715580470343, 1.8406300532488904, 1.7149004289682368,
# 1.6563132120598703, 1.5491354107014874, 1.3742701148276499,
# 1.298356134767733, 1.1448051520804472, 1.1293213975023044,
# 1.011956792840242, 0.91503472366352878, 0.96295887869177099,
# 0.83320234375382718]
# LogEntropyModel
# [None, 0.030213841236012517, 0.030213841236012517, 0.030213841236012517,
# 0.030213841236012517, 0.030213841236012517, 0.030213841236012517,
# 0.030213841236012517, 0.030213841236012517, 0.030213841236012517,
# 0.030213841236012517, 0.030213841236012517, 0.030213841236012517,
# 0.030213841236012517, 0.030213841236012517, 0.030213841236012517,
# 0.030213841236012517, 0.030213841236012517, 0.030213841236012517,
# 0.030213841236012517]
# RpModel
# [None, 0.023650641895355054, -0.021141726603634385, 0.03829050107711446,
# -0.010466970389653496, 0.004466004085307028, -0.002255663695246276,
# -0.09860087494476572, -0.03699258709957529, 0.008808481515794327,
# 0.08268715921158676, 0.044739284680453455, -0.07066948803926842,
# -0.014647845286061995, -0.08072000910174265, 0.02252911011129369,
# -0.0625467364731131, 0.007121270892606006, 0.02133085479124043,
# -0.010965839717908571]
# TfidfModel
# [None, 0.030168186365403877, 0.030168186365403877, 0.030168186365403877,
# 0.030168186365403877, 0.030168186365403877, 0.030168186365403877,
# 0.030168186365403877, 0.030168186365403877, 0.030168186365403877,
# 0.030168186365403877, 0.030168186365403877, 0.030168186365403877,
# 0.030168186365403877, 0.030168186365403877, 0.030168186365403877,
# 0.030168186365403877, 0.030168186365403877, 0.030168186365403877,
# 0.030168186365403877]
# No 3 popular tags
# [None, None, 0.52536011455432641, 0.35200686200283982, 0.32630439422912205,
# 0.28441259551419934, 0.31270963761918458, 0.26351811853936319,
# 0.23073741499925113, 0.23389335207637635, 0.27046204894807419,
# 0.30468095613023616, 0.24952002837002746, 0.24583560652900174,
# 0.31035491077788363, 0.2858432641789031, 0.2509649888866895,
# 0.26204875111007492, 0.26365234743065946, 0.28601171975018347]
# [None, None, 8.0989167033304046, 5.5984519039134275, 4.1892430039150836,
# 3.4514981671328244, 2.6281401638703641, 2.3616888324656511,
# 2.1383079153373181, 1.908272134571021, 1.5187303952912965,
# 1.5282955303560264, 1.3124448154521635, 1.1594203524821538,
# 1.1113485657557121, 1.1211079005107425, 1.0507190896009351,
# 1.0072553376481794, 0.86459835173994981, 0.76962143090410662]
# [None, None, 0.030384782390191226, 0.030384782390191226,
# 0.030384782390191226, 0.030384782390191226, 0.030384782390191226,
# 0.030384782390191226, 0.030384782390191226, 0.030384782390191226,
# 0.030384782390191226, 0.030384782390191226, 0.030384782390191226,
# 0.030384782390191226, 0.030384782390191226, 0.030384782390191226,
# 0.030384782390191226, 0.030384782390191226, 0.030384782390191226,
# 0.030384782390191226]
# [None, None, 0.49541806288799428, 0.49545597248663592, 0.4236800586284043,
# 0.41953005348807842, 0.39625775900399457, 0.45832298794954685,
# 0.44322519769228358, 0.47971293243741275, 0.4299839052668904,
# 0.40372862351395539, 0.46412731748662445, 0.36684198376151794,
# 0.43439133108924249, 0.46492821087040681, 0.44026631185309056,
# 0.47799242377311552, 0.44487691376302319, 0.48510028157224055]
# [None, None, 0.06639232465983934, 0.009731403783895608, 0.04552789655951802,
# 0.052893076107676566, 0.10274235418710675, 0.025670990029886823,
# 0.09109132673925553, 0.04174651359137136, 0.035685139708619966,
# 0.020992912085702774, 0.06591583130136838, 0.016695627551638097,
# 0.029646831740749755, 0.04192094143553673, 0.05822816699676532,
# 0.005579588581653547, 0.08812569907625305, 0.09910876800421514]
# [None, None, 0.030339483263164387, 0.030339483263164387,
# 0.030339483263164387, 0.030339483263164387, 0.030339483263164387,
# 0.030339483263164387, 0.030339483263164387, 0.030339483263164387,
# 0.030339483263164387, 0.030339483263164387, 0.030339483263164387,
# 0.030339483263164387, 0.030339483263164387, 0.030339483263164387,
# 0.030339483263164387, 0.030339483263164387, 0.030339483263164387,
# 0.030339483263164387]
# [None, None, 0.52940441321157228, 0.38760132906926698, 0.30019562061973804, 0.2508943225116117, 0.28258273977935983, 0.26618798670631738, 0.24486275303796032, 0.22860939173348088, 0.29817470950294744, 0.24410900615532261, 0.26476347050415505, 0.21929450428645433, 0.28736453456803013, 0.30047259794194953, 0.2460330811336934, 0.21117748708984516, 0.23454387098420279, 0.27161553758574392]
# [None, None, 8.0446441889004756, 5.0760647251139552, 3.8171214891886018, 3.3216865281700314, 2.5493720992360589, 2.1701685991832593, 2.0628354803414388, 1.815150369158316, 1.6812120021992385, 1.4066052644639382, 1.2798096890271975, 1.2077334069878811, 1.1682416832996474, 1.0490299375730798, 1.0600583597794584, 0.99260509869906022, 0.86438264816739852, 0.81332447058568891]
# [None, None, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273, 0.030213841236013273]
# [None, None, 0.45195734255680997, 0.42557944019157529, 0.31156872529329238, 0.41611087554666698, 0.37038160891101052, 0.45534465980809768, 0.42410208011131784, 0.43534756931883672, 0.38876974385451402, 0.41928957149898616, 0.4820236861286461, 0.41459513721943692, 0.35339318800824138, 0.44292979878269095, 0.4044147167051248, 0.45354300049532892, 0.4390092445799525, 0.42473884595520323]
# [None, None, 0.0764838322161096, 0.012256607866233496, 0.08007033095789438, 0.013413448663524166, 0.09077953747770827, 0.014355249160909312, 0.058327222274954786, 0.057061804863024986, 0.014080983163383026, 0.03175021615910337, 0.013649371487154864, 0.04361982863835617, 0.05740834543042602, 0.04296253836460023, 0.08404562470776925, 0.003265251884527594, 0.04259966253188474, 0.009069299813719341]
# [None, None, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405, 0.03016818636540405]
