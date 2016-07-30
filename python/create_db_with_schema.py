import sqlite3
from common import get_conn

__author__ = 'jambo'

conn = get_conn()
conn.execute("""
CREATE TABLE Tracks
 (
 id integer PRIMARY KEY,
 TrackInfo text
 )
""")
conn.execute("""
CREATE TABLE Artists
(
  id integer PRIMARY KEY,
  ArtistInfo text
)
""")