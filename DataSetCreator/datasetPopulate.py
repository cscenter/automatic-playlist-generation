import json
from dataproviders import HardDriveProvider
from parsers import coroutine, id3_v2_update, last_fm_update, STOP


@coroutine
def broadcast(targets):
    while True:
        message = yield
        for it in targets:
            it.send(message)

all_parsers = broadcast([id3_v2_update, last_fm_update])
dp = HardDriveProvider('VkDataset #1')
for song in json.loads(dp.get_all()):
    all_parsers.send(song)
all_parsers.send(STOP)