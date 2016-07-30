import fileinput
import sys
from common import normalize_name, lev_distance
from parse_request import try_get_song_from_db

def match(query_parts, target):
    target_parts = target.split()
    matched = 0
    targe_parts_len = len(target_parts)
    for query_part in query_parts:
        if matched == targe_parts_len:
            return True
        if lev_distance(query_part, target_parts[matched]) <= max(1, len(query_part) / 4):
            matched += 1
    return matched == targe_parts_len


def get_track(track_id):
    track = try_get_song_from_db(track_id)
    return track

def is_response_correct(track_artist_aliases, track_name_aliases, query_text):
    query_text = normalize_name(query_text).split()
    is_artist_good = any(
        [match(query_text, alias) for alias in track_artist_aliases]
    )
    is_track_good = any(match(query_text, alias) for alias in track_name_aliases)
    return is_artist_good, is_track_good


def get_reaction(query_text, similar_artists):
    return "Ты плох и никогда не угадаешь этот трек"


if __name__ == "__main__":
    for query in sys.stdin:  # id трека, user_query
        track_id, is_artist_solved, is_track_name_solved, query_text = query.split("\t", 3)
        query_text = query_text.strip()
        is_artist_solved, is_track_name_solved = int(is_artist_solved), int(is_track_name_solved)
        track = get_track(
            int(track_id)
        )
        artist_correct, track_name_correct = is_response_correct(track.artists[0].aliases, track.track_name_aliases, query_text)
        artist_reaction = ""
        track_reaction = ""
        if artist_correct and not is_artist_solved:
            artist_reaction = "разгадал артиста: {}".format(track.artists[0].name)
        if track_name_correct and not is_track_name_solved:
            track_reaction = "разгадал название трека: «{}»".format(track.track_name)
        reaction = " и ".join([_ for _ in (artist_reaction, track_reaction) if _])
        if not artist_correct and not track_name_correct:
            reaction = get_reaction(query_text, [])

        spoilers = "{};{} ".format(",".join(track.artists[0].aliases), ",".join(track.track_name_aliases))

        print("{}\t{}\t{}\t{}".format(int(artist_correct), int(track_name_correct), reaction, spoilers))