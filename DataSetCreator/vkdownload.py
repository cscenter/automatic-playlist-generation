# encoding: utf-8
import shutil
import urllib.request
from functools import wraps
from itertools import cycle


def coroutine(gen):
    @wraps(gen)
    def inner(*args, **kwargs):
        g = gen(*args, **kwargs)
        next(g)
        return g

    return inner


@coroutine
def download_mp3():
    while True:
        url = (yield)[7:]
        with urllib.request.urlopen(url) as response:
            file_name = url.split('/')[-1].split('?')[0]
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
                print(file_name)

queue = cycle([download_mp3(), download_mp3(),
               download_mp3(), download_mp3()])

with open('audios4935.html') as audio:
    for line in audio:
        ind = line.find('value="http')
        while ind >= 0:
            next_closing = line.find('">', ind)
            next_downloader = next(queue)
            next_downloader.send(line[ind:next_closing])
            ind = line.find('value="http', next_closing)
