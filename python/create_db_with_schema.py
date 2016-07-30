import sqlite3
__author__ = 'jambo'

db_filename = "data/tracks.db"
conn = sqlite3.connect(db_filename)

cur = conn.cursor()
cur.execute("""
CREATE TABLE Tracks
 (
 id integer PRIMARY KEY,
 TrackInfo text
 )
""")