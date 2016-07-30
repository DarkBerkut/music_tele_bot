import csv
import json
import requests
from common import Artist

SIMILAR_ARTISTS_DEFAULT_SIZE = 5

API_ROOT = "http://muzis.ru/api/"
MUSICBRAINS_API_ROOT = "http://musicbrainz.org/ws/2/"
LAST_FM = "http://ws.audioscrobbler.com/2.0/"

FROM_VALUES_API = API_ROOT + "stream_from_values.api"
SIMILAR_PERFORMANCES_API = API_ROOT + "similar_performers.api"


def get_categories():
    for file in ['data/style.csv', 'data/theme.csv', 'data/time.csv', 'data/language.csv', 'data/tempo.csv']:
        categ_dict = file_to_dict(file)


def get_indexes():
    categories = [i.strip() for i in input_str.split(',')]
    indxs = []
    for category in categories:
        ind = categ_dict.get(category.lower())
        if ind:
            indxs.append(ind)


def get_muzis_songs():
    values = ','.join(['{}:10'.format(i) for i in indxs])
    data = {'values': values, 'size': 20, 'operator': 'AND'}
    r = requests.post(FROM_VALUES_API, data=data)
    songs = r.json()['songs']


def create_aliases(name):
    pass


def get_musicbrainz_api_response(name):
    r = requests.get(MUSICBRAINS_API_ROOT + "artist", params={"query": name, "fmt": json})
    artist = r.json()["artists"][0]
    type = artist["type"]
    aliases = [alias["name"] for alias in artist.get("aliases", [])]
    return type, aliases


def generate_normalized_aliases(name, aliases, type):
    pass


def get_last_fm_api_response(name):
    r = requests.get(LAST_FM, params=dict(method="artist.gettoptracks", artist=name, api_key="eb7e02525703c69c761d0a17ca11923c", format=json))
    best_tracks = [t["name"] for t in r.json()["toptracks"]["track"][:3]]

def make_artist(id, name, photo, related_names):
    best_tracks = get_last_fm_api_response(name)
    type, aliases = get_musicbrainz_api_response(name)
    return Artist(id,
                  name,
                  generate_normalized_aliases(name, aliases, type),
                  type, related_names, photo, get_last_fm_api_response)


def get_similar_artists(artist_id):
    r = requests.post(SIMILAR_PERFORMANCES_API,
                      data={"performer_id": artist_id,
                            'size': SIMILAR_ARTISTS_DEFAULT_SIZE}
    )
    performers = r.json()['performers']
    make_artist(performers['id'], performers['title'], performers['poster'])

    # "poster" : "iwbfg69nl60u.jpg",
    # "id" : 389,
    # "title" : "Елена Ваенга",
    return


def make_track_from_song(song):
    song_id = song['id']
    artists = song['performers']
    for artist_id in artists:
        similar_artists = get_similar_artists(artist_id)





if __name__ == "__main__":
    input_str = input()

    def file_to_dict(file):
        return {row[1].lower(): row[0] for row in csv.reader(open(file))}

    categ_dict = get_categories()
    indxs = get_indexes()
    songs = get_muzis_songs()

    result = []
    for song in songs:
        track = make_track_from_song(song)
        result.append(song['id'])

    result = ' '.join([str(i) for i in result])
    print(result)
