__author__ = 'jambo'

def normalize_name(string):
    return " ".join("".join([ch if ch.isalpha() or ch.isdigit() else " " for ch in string.lower()]).split())

from Levenshtein import distance as lev_distance

def generate_aliases():
    pass


class Track():
    def __init__(self, id, artists, track_name, track_name_aliases):
        self.id = id
        self.artists = artists
        self.track_name = track_name
        self.track_name_aliases = track_name_aliases


class Artist():
    def __init__(self, name, aliases, type, related, photo, album, track_filename):
        self.name = name
        self.aliases = aliases
        self.type = type
        self.related = related
        self.photo = photo
        self.album = album
        self.track_filename = track_filename

