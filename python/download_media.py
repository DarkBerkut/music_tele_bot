import requests
from pydub import AudioSegment


def download_and_cut_song(song_name, begin=0, end=15*1000):
    r = requests.get("http://f.muzis.ru/{}".format(song_name))
    with open("data/music/full/{}".format(song_name), 'wb') as file:
        file.write(r.content)
    song = AudioSegment.from_mp3("data/music/full/{}".format(song_name))
    cut_song = song[begin:end]
    cut_song.export("data/music/cut/cut_{}".format(song_name), format='mp3')


def download_photo(photo_name):
    r = requests.get("http://f.muzis.ru/{}".format(photo_name))
    with open("data/photo/{}".format(photo_name), 'wb') as file:
        file.write(r.content)

if __name__ == "__main__":
    download_and_cut_song('wuyexyc1lzmo.mp3')
    download_photo("iwbfg69nl60u.jpg")
