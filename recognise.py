import os
import numpy as np
from tinytag import TinyTag
from record import record_audio
from Fingerprint.fingerprint import fingerprint_file, fingerprint_audio
from Storage.storage import store_song, get_matches, get_info_for_song_id, song_in_db

# Extensions that I've tested with librosa
KNOWN_EXTENSIONS = ["mp3", "wav", "flac", "m4a"]

def get_song_info(filename):
    tag = TinyTag.get(filename)
    return (tag.albumartist, tag.album, tag.title)

def register_song(filename, sample_rate=11025, distance=30, point_efficiency=0.8):
    if song_in_db(filename):
        return
    hashes = fingerprint_file(filename, sample_rate=sample_rate, distance=distance, point_efficiency=point_efficiency)
    song_info = get_song_info(filename)
    store_song(hashes, song_info)

def register_directory(path, sample_rate=11025, distance=30, point_efficiency=0.8):
    """ Recursively register songs in a directory """
    for root, _, files in os.walk(path):
        for f in files:
            if f.split('.')[-1] not in KNOWN_EXTENSIONS:
                continue
            file_path = os.path.join(path, root, f)
            register_song(file_path, sample_rate=sample_rate, distance=distance, point_efficiency=point_efficiency)

def score_match(offsets):
    tks = list(map(lambda x: x[0] - x[1], offsets))
    hist, _ = np.histogram(tks)
    return np.max(hist)

def best_match(matches):
    matched_song = None
    best_score = 0
    for song_id, offsets in matches.items():
        if len(offsets) < best_score:
            # can't be best score, avoid expensive histogram
            continue
        score = score_match(offsets)
        if score > best_score:
            best_score = score
            matched_song = song_id
    return matched_song

def recognise_song(filename, sample_rate=11025, distance=30, point_efficiency=0.8):
    hashes = fingerprint_file(filename, sample_rate=sample_rate, distance=distance, point_efficiency=point_efficiency)
    matches = get_matches(hashes)
    matched_song = best_match(matches)
    info = get_info_for_song_id(matched_song)
    if info is not None:
        return info
    return matched_song

def listen_to_song(filename=None):
    audio = record_audio(filename=filename)
    hashes = fingerprint_audio(audio)
    matches = get_matches(hashes)
    matched_song = best_match(matches)
    info = get_info_for_song_id(matched_song)
    if info is not None:
        return info
    return matched_song
