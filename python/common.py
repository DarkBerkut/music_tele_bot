__author__ = 'jambo'
import json


def normalize_name(string):
    return " ".join("".join([ch if ch.isalpha() or ch.isdigit() else " " for ch in string.lower()]).split())


def generate_aliases():
    pass


class Track():
    def __init__(self, id, artists, track_name, track_name_aliases, track_filename):
        self.id = id
        self.artists = artists
        self.track_name = track_name
        self.track_name_aliases = track_name_aliases
        self.track_filename = track_filename

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    @classmethod
    def from_json(cls, track_json):
        track = json.loads(track_json)
        return Track(track['id'], track['artists'], track['track_name'], track['track_name_aliases'],
                     track['track_filename'])


class Artist():
    def __init__(self, id, name, aliases, type, related, photo, best_tracks):
        self.id = id
        self.name = name
        self.aliases = aliases
        self.type = type
        self.related = related
        self.photo = photo
        self.best_tracks = best_tracks

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    @classmethod
    def from_json(cls, artist_json):
        artist = json.loads(artist_json)
        return Artist(artist['id'], artist['name'], artist['aliases'], artist['type'], artist['related'],
                      artist['photo'], artist['best_tracks'])
