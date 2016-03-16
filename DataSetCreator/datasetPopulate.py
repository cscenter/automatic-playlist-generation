import json

from dataproviders import HardDriveProvider

dp = HardDriveProvider('VkDataset #1')
for song in json.loads(dp.get_all()):
    print(song)
