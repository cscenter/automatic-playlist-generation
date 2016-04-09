from dataproviders import HardDriveProvider
from parsers import coroutine, echo_nest_update, id3_v2_update,\
    last_fm_update, STOP


@coroutine
def broadcast(targets):
    while True:
        message = yield
        for it in targets:
            try:
                it.send(message)
            except StopIteration:
                targets.remove(it)
                continue
        if message == STOP:
            break

# songs_to_print = set()
for dataset_path in ['music']:
    dp = HardDriveProvider(dataset_path)
    # print(len(dp.get_all()))
    # print(sum(1 if song['id3'] else 0
    # for song in map(dp.get_by_id, dp.get_all())))
    # for song in dp.get_all():
    #     song_data = dp.get_by_id(song)
    #     if song_data['id3']:
    #         pass
    #     exit()
    all_parsers = broadcast([id3_v2_update(), last_fm_update(),
                             echo_nest_update()])
    # , ])
    # , librosa_update()])
    for i, song in enumerate(dp.get_all(), 1):
        song_data = dp.get_by_id(song)
        # songs_to_print.add((song_data['id3']['artist'],
        #                     song_data['id3']['album'],
        #                     song_data['id3']['title']))
        all_parsers.send(song_data)
        if not (i % 50):
            dp.save_data()
            print(i)
    try:
        all_parsers.send(STOP)
    except StopIteration:
        pass
    dp.save_data()
    print('{} songs updated'.format(len(dp.get_all())))

# for i in sorted(songs_to_print):
#     print("{} - {} - {}".format(i[0], i[1], i[2]))
