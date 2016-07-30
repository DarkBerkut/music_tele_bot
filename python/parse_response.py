import sys

def get_track(track_id):
    return ["григорий лепс", "лепс"], ["я уеду жить в лондон"], ["стас михайлов"]


def is_response_correct(track_artist_aliases, track_name_aliases, query_text):
    return True, True


def get_reaction(query_text, similar_artists):
    return "Ты плох и никогда не угадаешь этот трек"


if __name__ == "__main__":
    query = open(sys.stdin).read()  # id трека, user_query
    track_id, is_artist_solved, is_track_name_solved, query_text = query.split("\t", 3)
    track_artist_aliases, track_name_aliases, similar_artists = get_track(
        int(track_id)
    )
    artist_correct, track_name_correct = is_response_correct(track_artist_aliases, track_name_aliases, query_text)
    reaction = None
    if not artist_correct and track_name_correct:
        reaction = get_reaction(query_text, similar_artists)

    print(artist_correct, track_name_correct, reaction)