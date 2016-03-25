# encoding: utf-8
import shutil
import urllib.request
from itertools import cycle
from urllib.error import HTTPError

from parsers import coroutine


@coroutine
def download_mp3():
    while True:
        url = (yield)[7:]
        try:
            with urllib.request.urlopen(url) as response:
                file_name = url.split('/')[-1].split('?')[0]
                with open(file_name, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                    print(file_name)
        except HTTPError:
            continue

queue = cycle([download_mp3(), download_mp3(),
               download_mp3(), download_mp3()])

with open('audios4360861.html') as audio:
    for line in audio:
        ind = line.find('value="http')
        while ind >= 0:
            next_closing = line.find('">', ind)
            next_downloader = next(queue)
            next_downloader.send(line[ind:next_closing])
            ind = line.find('value="http', next_closing)
