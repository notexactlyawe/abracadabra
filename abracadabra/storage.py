import uuid
import sqlite3
from collections import defaultdict
from contextlib import contextmanager
from . import settings


@contextmanager
def get_cursor():
    """Get a connection/cursor to the database.

    :returns: Tuple of connection and cursor.
    """
    try:
        conn = sqlite3.connect(settings.DB_PATH, timeout=30)
        yield conn, conn.cursor()
    finally:
        conn.close()


def setup_db():
    """Create the database and tables.

    To be run once through an interactive shell.
    """
    with get_cursor() as (conn, c):
        c.execute("CREATE TABLE IF NOT EXISTS hash (hash int, offset real, song_id text)")
        c.execute("CREATE TABLE IF NOT EXISTS song_info (artist text, album text, title text, song_id text)")
        # dramatically speed up recognition
        c.execute("CREATE INDEX IF NOT EXISTS idx_hash ON hash (hash)")
        # faster write mode that enables greater concurrency
        # https://sqlite.org/wal.html
        c.execute("PRAGMA journal_mode=WAL")
        # reduce load at a checkpoint and reduce chance of a timeout
        c.execute("PRAGMA wal_autocheckpoint=300")


def checkpoint_db():
    with get_cursor() as (conn, c):
        c.execute("PRAGMA wal_checkpoint(FULL)")


def song_in_db(filename):
    """Check whether a path has already been registered.

    :param filename: The path to check.
    :returns: Whether the path exists in the database yet.
    :rtype: bool
    """
    with get_cursor() as (conn, c):
        song_id = str(uuid.uuid5(uuid.NAMESPACE_OID, filename).int)
        c.execute("SELECT * FROM song_info WHERE song_id=?", (song_id,))
        return c.fetchone() is not None


def store_song(hashes, song_info):
    """Register a song in the database.

    :param hashes: A list of tuples of the form (hash, time offset, song_id) as returned by
        :func:`~abracadabra.fingerprint.fingerprint_file`.
    :param song_info: A tuple of form (artist, album, title) describing the song.
    """
    if len(hashes) < 1:
        # TODO: After experiments have run, change this to raise error
        # Probably should re-run the peaks finding with higher efficiency
        # or maybe widen the target zone
        return
    with get_cursor() as (conn, c):
        c.executemany("INSERT INTO hash VALUES (?, ?, ?)", hashes)
        insert_info = [i if i is not None else "Unknown" for i in song_info]
        c.execute("INSERT INTO song_info VALUES (?, ?, ?, ?)", (*insert_info, hashes[0][2]))
        conn.commit()


def get_matches(hashes, threshold=5):
    """Get matching songs for a set of hashes.

    :param hashes: A list of hashes as returned by
        :func:`~abracadabra.fingerprint.fingerprint_file`.
    :param threshold: Return songs that have more than ``threshold`` matches.
    :returns: A dictionary mapping ``song_id`` to a list of time offset tuples. The tuples are of
        the form (result offset, original hash offset).
    :rtype: dict(str: list(tuple(float, float)))
    """
    h_dict = {}
    for h, t, _ in hashes:
        h_dict[h] = t
    in_values = f"({','.join([str(h[0]) for h in hashes])})"
    with get_cursor() as (conn, c):
        c.execute(f"SELECT hash, offset, song_id FROM hash WHERE hash IN {in_values}")
        results = c.fetchall()
    result_dict = defaultdict(list)
    for r in results:
        result_dict[r[2]].append((r[1], h_dict[r[0]]))
    return result_dict


def get_info_for_song_id(song_id):
    """Lookup song information for a given ID."""
    with get_cursor() as (conn, c):
        c.execute("SELECT artist, album, title FROM song_info WHERE song_id = ?", (song_id,))
        return c.fetchone()
