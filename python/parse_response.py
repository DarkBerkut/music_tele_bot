import fileinput
import sys
from common import normalize_name
from parse_request import try_get_song_from_db

# def match(query, target):
#     query = normalize_name(query)
#     query_parts = query.split()
#     target_parts = target.parts()
#     matched = 0
#


def get_track(track_id):
    track = try_get_song_from_db(track_id)
    return track.artists[0].aliases, track.track_name_aliases, []

def is_response_correct(track_artist_aliases, track_name_aliases, query_text):
    is_artist_good = any(
        [query_text == alias for alias in track_artist_aliases]
    )
    is_track_good = any(query_text == alias for alias in track_name_aliases)
    return is_artist_good, is_track_good


def get_reaction(query_text, similar_artists):
    return "Ты плох и никогда не угадаешь этот трек"


if __name__ == "__main__":
    for query in sys.stdin:  # id трека, user_query
        track_id, is_artist_solved, is_track_name_solved, query_text = query.split("\t", 3)
        query_text = query_text.strip()
        is_artist_solved, is_track_name_solved = int(is_artist_solved), int(is_track_name_solved)
        track_artist_aliases, track_name_aliases, similar_artists = get_track(
            int(track_id)
        )
        artist_correct, track_name_correct = is_response_correct(track_artist_aliases, track_name_aliases, query_text)
        reaction = "Cool!"
        if not artist_correct and not track_name_correct:
            reaction = get_reaction(query_text, similar_artists)

        spoilers = "{};{} ".format(",".join(track_artist_aliases), ",".join(track_name_aliases))

        print("{}\t{}\t{}\t{}".format(int(artist_correct), int(track_name_correct), reaction, spoilers))