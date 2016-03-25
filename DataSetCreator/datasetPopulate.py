from dataproviders import HardDriveProvider
from parsers import coroutine, echo_nest_update, id3_v2_update,\
    last_fm_update, librosa_update, STOP


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

all_parsers = broadcast([id3_v2_update(), last_fm_update()])
#                          , echo_nest_update(), librosa_update()])
for dataset_path in ['VkDataset #1']:
    dp = HardDriveProvider(dataset_path)
    for i, song in enumerate(dp.get_all()):
        song_data = dp.get_by_id(song)
        all_parsers.send(song_data)
        if i and not (i % 100):
            dp.save_data()
        print(song)

    try:
        all_parsers.send(STOP)
    except StopIteration:
        pass
    dp.save_data()
