import csv
import json
import os
import requests
import time
from common import Artist, Track, get_conn, normalize_name

SIMILAR_ARTISTS_DEFAULT_SIZE = 5

API_ROOT = "http://muzis.ru/api/"
MUSICBRAINS_API_ROOT = "http://musicbrainz.org/ws/2/"
LAST_FM = "http://ws.audioscrobbler.com/2.0/"

FROM_VALUES_API = API_ROOT + "stream_from_values.api"
SIMILAR_PERFORMANCES_API = API_ROOT + "similar_performers.api"

artists = {}
tracks = {}

def file_to_dict(file):
    return {row[1].lower(): row[0] for row in csv.reader(open(file))}

def get_categories():
    categ_dict = {}
    for file in ['data/style.csv', 'data/theme.csv', 'data/time.csv', 'data/language.csv', 'data/tempo.csv']:
        categ_dict.update(file_to_dict(file))
    return categ_dict

def get_indexes(input_str, categ_dict):
    categories = [i.strip() for i in input_str.split(',')]
    indxs = []
    for category in categories:
        ind = categ_dict.get(category.lower())
        if ind:
            indxs.append(ind)
    return indxs

def get_muzis_songs(indxs):
    values = ','.join(['{}:100'.format(i) for i in indxs])
    data = {'values': values, 'size': 20, 'operator': 'AND'}
    r = requests.post(FROM_VALUES_API, data=data)
    return r.json()['songs']


def create_aliases(name):
    pass


def get_musicbrainz_api_response(name):
    code = None
    while code != 200:
        r = requests.get(MUSICBRAINS_API_ROOT + "artist", params={"query": name, "fmt": 'json'})
        code = r.status_code
        if code != 200:
            time.sleep(0.5)
    artist = r.json()["artists"][0]
    type = artist["type"]
    aliases = [alias["name"] for alias in artist.get("aliases", [])]
    return type, aliases


def generate_normalized_aliases(name, aliases, type):
    pass


def get_last_fm_api_response(name):
    r = requests.get(LAST_FM, params=dict(method="artist.gettoptracks", artist=name, api_key="eb7e02525703c69c761d0a17ca11923c", format="json"))
    best_tracks = [t["name"] for t in r.json()["toptracks"]["track"][:3]]
    return best_tracks

def make_artist(id, name, photo, related_names):
    best_tracks = get_last_fm_api_response(name)
    type, aliases = get_musicbrainz_api_response(name)
    return Artist(id,
                  name,
                  generate_normalized_aliases(name, aliases, type),
                  type, related_names, photo,
                  best_tracks)


def get_similar_artists(artist_id):
    r = requests.post(SIMILAR_PERFORMANCES_API,
                      data={"performer_id": artist_id,
                            'size': SIMILAR_ARTISTS_DEFAULT_SIZE}
    )
    performers = r.json()['performers'][0]
    return make_artist(performers['id'], performers['title'], performers['poster'], [])  # TODO similar


def make_track_name_aliases(param):
    return normalize_name(param)


def make_track_from_song(song):
    song_id = song['id']
    artists = song['performers']
    real_artists = [get_similar_artists(artist_id) for artist_id in artists]
    return Track(song_id, real_artists,
          song["track_name"],
          make_track_name_aliases(song["track_name"]), song["file_mp3"])

def put_artists_to_db(artists):
    data = [(artist.id, artist.to_json()) for artist in artists]
    conn = get_conn()
    conn.executemany("""
        INSERT INTO Artists VALUES (?, ?)
    """, data)
    conn.commit()

def put_track_to_db(track):
    put_artists_to_db(track.artists)
    track.artists = [a.id for a in track.artists]
    id, track_json = track.id, track.to_json()
    conn = get_conn()
    conn.execute("""
        INSERT INTO Tracks VALUES (?, ?)
    """, (id, track_json))
    conn.commit()

def main():
    # global input_str, file_to_dict, categ_dict, indxs, songs, result, song, track, i
    input_str = "Русский"# input()
    categ_dict = get_categories()
    indxs = get_indexes(input_str, categ_dict)
    songs = get_muzis_songs(indxs)
    result = []
    for song in songs:
        track = make_track_from_song(song)
        put_track_to_db(track)
        result.append(track.id)
    result = ' '.join([str(i) for i in result])
    print(result)


if __name__ == "__main__":
    main()
    # artists = [Artist(2, "A", ["a"], "Person", ["b"], "photo.jpg", ["best"]), Artist(3, "A", ["a"], "Person", ["b"], "photo.jpg", ["best"])]
    # artists_ids = [2]
    # # put_track_to_db(Track(1, artists_ids, "TrackName", ["trackname"], "track.mp3"))
    # put_artists_to_db(artists)