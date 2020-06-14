import sqlite3
from collections import defaultdict

# stored in the root of the project by default
DB_NAME = "hash.db"

def setup_db():
    """ To be run once through an interactive shell """
    conn, c = get_cursor()
    c.execute("CREATE TABLE hash (hash int, offset real, song_id text)")
    c.execute("CREATE TABLE song_info (artist text, album text, title text, song_id text)")

def get_cursor():
    conn = sqlite3.connect(DB_NAME)
    return conn, conn.cursor()

def store_song(hashes, song_info):
    conn, c = get_cursor()
    c.executemany("INSERT INTO hash VALUES (?, ?, ?)", hashes)
    insert_info = [i if i is not None else "Unknown" for i in song_info]
    c.execute("INSERT INTO song_info VALUES (?, ?, ?, ?)", (*song_info, hashes[0][2]))
    conn.commit()

def get_matches(hashes, threshold=5):
    conn, c = get_cursor()
    h_dict = {}
    for h, t, _ in hashes:
        h_dict[h] = t
    in_values = f"({','.join([str(h[0]) for h in hashes])})"
    c.execute(f"SELECT hash, offset, song_id FROM hash WHERE hash IN {in_values}")
    results = c.fetchall()
    result_dict = defaultdict(list)
    for r in results:
        result_dict[r[2]].append((r[1], h_dict[r[0]]))
    return result_dict

def get_info_for_song_id(song_id):
    conn, c = get_cursor()
    c.execute("SELECT artist, album, title FROM song_info WHERE song_id = ?", (song_id,))
    return c.fetchone()
