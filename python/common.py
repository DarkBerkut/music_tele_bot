__author__ = 'jambo'

def normalize_name(string):
    return " ".join("".join([ch if ch.isalpha() or ch.isdigit() else " " for ch in string.lower()]).split())

from Levenshtein import distance as lev_distance

