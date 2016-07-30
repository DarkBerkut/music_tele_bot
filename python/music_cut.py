import requests
from pydub import AudioSegment

TIME_IN_SECONDS = 15 * 1000
song_name = 'wuyexyc1lzmo'
r = requests.get("http://f.muzis.ru/{}.mp3".format(song_name))
with open("data/music/{}.mp3".format(song_name), 'wb') as file:
    file.write(r.content)

song = AudioSegment.from_mp3("data/music/{}.mp3".format(song_name))
cut_song = song[:TIME_IN_SECONDS]
cut_song.export("data/music/cut_{}.mp3".format(song_name), format='mp3')
