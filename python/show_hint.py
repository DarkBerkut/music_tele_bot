import sys
from common import normalize_name
from parse_request import try_get_song_from_db
from parse_response import match

__author__ = 'jambo'


for query in sys.stdin:
    track_id = int(query.strip())
    track = try_get_song_from_db(track_id)
    if not track:
        print("TEXT\tЯ ничего не знаю про этот трек")
    if track.artists[0].photo:
        print("IMG\t" + track.artists[0].photo)
    if track.artists[0].best_tracks:
        best_tracks = ["загаданный трек" if any([match(normalize_name(best_track).split(), alias) for alias in track.track_name_aliases]) else best_track for best_track in track.artists[0].best_tracks]
        print("TEXT\t{}".format("Самые известные треки данного исполнителя: {}".format(", ".join(best_tracks))))
    if not track.artists[0].photo and not track.artists[0].best_tracks:
        print("TEXT\tУ меня нет подсказок про данного артиста")
