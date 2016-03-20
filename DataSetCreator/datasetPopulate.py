from dataproviders import HardDriveProvider
from parsers import coroutine, id3_v2_update, last_fm_update, STOP


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
dp = HardDriveProvider('VkDataset #1')
for song in dp.get_all():
    song_data = dp.get_by_id(song)
    all_parsers.send(song_data)
    print(song_data)
    stop()

try:
    all_parsers.send(STOP)
except StopIteration:
    pass
dp.save_data()
