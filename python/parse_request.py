import logging
import random
import sys

from pymystem3 import Mystem

from download_media import download_and_cut_song
import download_media

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
import csv
import requests
import time
from common import Artist, Track, get_conn, normalize_name

SIMILAR_ARTISTS_DEFAULT_SIZE = 2

API_ROOT = "http://muzis.ru/api/"
MUSICBRAINS_API_ROOT = "http://musicbrainz.org/ws/2/"
LAST_FM = "http://ws.audioscrobbler.com/2.0/"

FROM_VALUES_API = API_ROOT + "stream_from_values.api"
SIMILAR_PERFORMANCES_API = API_ROOT + "similar_performers.api"
SONGS_BY_PERFORMER = API_ROOT + "get_songs_by_performer.api"

M = Mystem()

artists_cache = {

}
tracks_cache = {

}


def file_to_dict(file):
    type_to_id = {normalize_name(row[1]): row[0] for row in csv.reader(open(file))}
    id_to_type = {v: k for k, v in type_to_id.items()}
    normalize = {''.join(M.lemmatize(key)).strip():type_to_id[key] for key in type_to_id}
    type_to_id.update(normalize)
    return type_to_id, id_to_type


def get_categories():
    categ_dict = {}
    id_to_type_full = {}
    tree_dict = {}
    for file in ['data/style.csv', 'data/theme.csv', 'data/time.csv', 'data/language.csv', 'data/tempo.csv']:
        type_to_id, id_to_type = file_to_dict(file)
        for cat, id in categ_dict.items():
            cat_split = cat.split()
            cur_dict = tree_dict
            for part in cat_split:
                if part not in cur_dict:
                    cur_dict[part] = {}
                cur_dict = cur_dict[part]
            cur_dict["$VAL$"] = id
        categ_dict.update(type_to_id)
        id_to_type_full.update(id_to_type)
    return categ_dict, id_to_type_full, tree_dict


def get_indexes(input_str, tree_dict):
    categories = [''.join(M.lemmatize(i)).strip() for i in input_str.split(',')]
    indxs = []
    for category in categories:
        category_split = normalize_name(category).split()
        previous_step = None
        cur_step = tree_dict
        for category_part in category_split:
            if category_part in cur_step:
                previous_step = cur_step
                cur_step = cur_step[category_part]
            else:
                if cur_step.get("$VAL$"):
                    indxs.append(cur_step.get("$VAL$"))
                    if category_part in tree_dict:
                        previous_step = None
                        cur_step = tree_dict
                if category_part in cur_step:
                    previous_step = cur_step
                    cur_step = cur_step[category_part]

        if cur_step.get("$VAL$"):
            indxs.append(cur_step.get("$VAL$"))
            previous_step = None
            cur_step = tree_dict
        # ind = categ_dict.get(normalize_name(category))
        # if ind:
        #     indxs.append(ind)
    return indxs


def get_muzis_songs(indxs):
    values = ','.join(['{}:100'.format(i) for i in indxs])
    data = {'values': values, 'size': 10, 'operator': 'AND'}
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
    type = artist.get("type", "Person")
    aliases = [alias["name"] for alias in artist.get("aliases", [])]
    return type, aliases


def generate_normalized_aliases(name, aliases, type):
    aliases = [normalize_name(name)] + [normalize_name(alias) for alias in aliases]
    if type == "Person":
        aliases.extend(
            [alias.split()[-1] for alias in aliases]
        )
    return list(set(aliases))


def get_last_fm_api_response(name):
    r = requests.get(LAST_FM,
                     params=dict(method="artist.gettoptracks", artist=name, api_key="eb7e02525703c69c761d0a17ca11923c",
                                 format="json"))
    try:
        best_tracks = [t["name"] for t in r.json()["toptracks"]["track"][:3]]
    except KeyError:
        logging.exception("Best tracks")
        return []
    return best_tracks


def make_artist(id, name, photo, related_names):
    logging.debug("last.fm api: {}:{}".format(id, name))
    best_tracks = get_last_fm_api_response(name)
    logging.debug("Done")
    logging.debug("musicbrainz api: {}:{}".format(id, name))
    try:
        type, aliases = get_musicbrainz_api_response(name)
    except:
        logging.exception("musicbrains")
        type, aliases = "Person", ""
    if photo:
        download_media.download_photo(photo)
    logging.debug("done")
    return Artist(id,
                  name,
                  generate_normalized_aliases(name, aliases, type),
                  type, related_names, photo,
                  best_tracks)


def get_similar_artists(artist_id):
    logging.debug("Similar query: {}".format(artist_id))
    r = requests.post(SONGS_BY_PERFORMER,
                      data={"performer_id": artist_id,
                            'size': SIMILAR_ARTISTS_DEFAULT_SIZE}
                      )
    logging.debug("Done")
    try:
        songs = r.json()["songs"]
        song_with_artist_info = None
        for song in songs:
            if song["performer_id"] == artist_id:
                song_with_artist_info = song
                break
        if not song_with_artist_info:
            logging.error("PERFORMER NOT FOUND FOR {}".format(artist_id))
            return None
    except:
        return None
    return make_artist(song_with_artist_info['performer_id'], song_with_artist_info['performer'],
                       song_with_artist_info['poster'], [])  # TODO similar


def make_track_name_aliases(param):
    return [normalize_name(param)]


def try_get_artists_from_db(artists):
    if not artists:
        return [], []

    result = []
    remains = []
    for artist in artists:
        if artist in artists_cache:
            result.append(artists_cache[artist])
        else:
            remains.append(artist)
    if remains:
        result_set = get_conn().cursor().execute("""
        SELECT ArtistInfo FROM Artists Where Id in (%s)
        """ % ",".join(["?" for _ in remains]), remains)
        rows = result_set.fetchall()
        for artist_json, in rows:
            artist_obj = Artist.from_json(artist_json)
            artists_cache[artist_obj.id] = artist_obj
            result.append(artist_obj)
        remains = [art for art in remains if not artists_cache.get(art)]
    return result, remains


def try_get_song_from_db(song_id):
    if song_id in tracks_cache:
        return tracks_cache[song_id]
    result_set = get_conn().cursor().execute("""
    SELECT TrackInfo FROM Tracks Where Id = ?
    """, [song_id])
    row = result_set.fetchone()
    if row:
        json_obj, = row
        track = Track.from_json(json_obj)
        artists, remains = try_get_artists_from_db(track.artists)
        if remains:
            remain_artists = [get_similar_artists(artist_id) for artist_id in remains]
            for artist in remain_artists:
                if not artist:
                    return None
            put_artists_to_db(remain_artists)
            artists.extend(remain_artists)
            remains.clear()
        assert (not remains)
        track.artists = artists
        tracks_cache[track.id] = track
        return track


def make_track_from_song(song):
    song_id = song['id']
    logging.debug("Current song: {}".format(song_id))
    track = try_get_song_from_db(song_id)
    if track:
        logging.debug("Found in db: {}:{}".format(track.artists[0].name, track.track_name))
        return track
    else:
        artists = song['performers']
        real_artists, remains = try_get_artists_from_db(artists)
        if remains:
            remains_ = [get_similar_artists(artist_id) for artist_id in remains]
            for artist_ in remains_:
                if not artist_:
                    return None
            real_artists.extend(remains_)
        new_track = Track(song_id, real_artists, song["track_name"], make_track_name_aliases(song["track_name"]),
                          song["file_mp3"])
        download_and_cut_song(song["file_mp3"])
        logging.debug("Track Done")
        put_track_to_db(new_track)
        return new_track


def put_artists_to_db(artists):
    artists = [artist for artist in artists if artist.id not in artists_cache]
    data = [(artist.id, artist.to_json()) for artist in artists]
    conn = get_conn()
    conn.executemany("""
        INSERT OR IGNORE INTO Artists VALUES (?, ?)
    """, data)
    conn.commit()
    for artist in artists:
        artists_cache[artist.id] = artist


def put_track_to_db(track):
    put_artists_to_db(track.artists)
    track.artists = [a.id for a in track.artists]
    id, track_json = track.id, track.to_json()
    conn = get_conn()
    conn.execute("""
        INSERT OR IGNORE INTO Tracks VALUES (?, ?)
    """, (id, track_json))
    conn.commit()
    tracks_cache[track.id] = track


def main():
    # global input_str, file_to_dict, categ_dict, indxs, songs, result, song, track, i
    input_str = input()
    if input_str == "demo":
        songs = [{'id': 1521, 'performers': [6307], "file_mp3": "0ny6b0atnkmh.mp3",
                  "track_name": "Кукушка"},
                 {'id': 19386,
                  "file_mp3" : "f4cvaybo03pw.mp3",
                  "track_name" : "Пять причин",
                  'performers': [5690]},
                 {'id': 35413,
                  "file_mp3" : "qai6pto6wphm.mp3",
                  "track_name" : "Rap god",
                  'performers' :[12407]
                 }]
        print("OK\tСоздаю демо игру")
    else:
        # 1521 кукушка кино
        # 19386 никалаев/выпьем за любовь/пять причин
        # 35413 эминем рэп гад
        categ_dict, id_to_type_dict, tree_dict = get_categories()
        indxs = list(set(get_indexes(input_str, tree_dict)))
        if indxs:
            print("OK\tСоздаю игру по следующему набору тем: {}".format(", ".join([id_to_type_dict[i] for i in indxs])))
            sys.stdout.flush()
        else:
            print("UNK\t{}".format("Я не смог понять тему игры. Попробуйте следующие варианты темы: «start русский рок», «start американский хип-хоп 80-х»"))
            sys.stdout.flush()
            return
        songs = get_muzis_songs(indxs)
    result = []
    logging.debug("Loaded songs: {}".format([song['id'] for song in songs]))
    for song in songs:
        track = make_track_from_song(song)
        if track is None:
            logging.error("couldn't make a song {}".format(song['id']))
        else:
            result.append(track)
    random.shuffle(result)
    result = '\n'.join(["{}\t{}".format(track.id, track.track_filename) for track in result[:5]])
    print(result)


if __name__ == "__main__":
    main()
    # artists = [Artist(2, "A", ["a"], "Person", ["b"], "photo.jpg", ["best"]), Artist(3, "A", ["a"], "Person", ["b"], "photo.jpg", ["best"])]
    # artists_ids = [2]
    # # put_track_to_db(Track(1, artists_ids, "TrackName", ["trackname"], "track.mp3"))
    # put_artists_to_db(artists)
