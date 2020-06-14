import uuid
import numpy as np
import librosa.core as lr
from scipy.signal import spectrogram

def my_spectrogram(audio, sample_rate, fft_window_size_s=0.1):
    # default 100ms segments (allows for 600BPM music)
    nperseg = int(sample_rate * fft_window_size_s)
    return spectrogram(audio, sample_rate, nperseg=nperseg)

def file_to_spectrogram(filename, rate=11025):
    audio, _ = lr.load(filename, sr=rate, mono=True)
    return my_spectrogram(audio, rate)

def find_peaks(arr, distance, point_efficiency=0.4):
    # get sorted flattened indices descending
    i = arr.argsort(axis=None)[::-1]
    # get co-ordinates into arr
    j = np.vstack(np.unravel_index(i, arr.shape)).T
    peaks = []
    total = j.size
    # in a square with a perfectly spaced grid, we could fit area / distance^2 points
    # use point efficiency to reduce this, since it won't be perfectly spaced
    # accuracy vs speed tradeoff
    peak_target = (total / (distance**2)) * point_efficiency
    for point in j:
        if len(peaks) > peak_target:
            break
        for peak in peaks:
            if abs(point[0] - peak[0]) + abs(point[1] - peak[1]) < distance:
                break
        else:
            peaks.append(point)
    return peaks

def idxs_to_tf_pairs(idxs, t, f):
    return np.array([(f[i[0]], t[i[1]]) for i in idxs])

def hash_point_pair(p1, p2):
    return hash((p1[0], p2[0], p2[1]-p2[1]))

def target_zone(anchor, points, width, height, t):
    x_min = anchor[1] + t
    x_max = x_min + width
    y_min = anchor[0] - (height*0.5)
    y_max = y_min + height
    for point in points:
        if point[0] < y_min or point[0] > y_max:
            continue
        if point[1] < x_min or point[1] > x_max:
            continue
        yield point

def hash_points(points, filename, target_start=0.1, target_t=1, target_f=2000):
    hashes = []
    song_id = uuid.uuid5(uuid.NAMESPACE_OID, filename).int
    for anchor in points:
        for target in target_zone(
            anchor, points, target_t, target_f, target_start
        ):
            hashes.append((
                # hash
                hash_point_pair(anchor, target),
                # time offset
                anchor[1],
                # filename
                str(song_id)
            ))
    return hashes

def fingerprint_file(filename, sample_rate=11025, distance=30, point_efficiency=0.4):
    f, t, Sxx = file_to_spectrogram(filename, rate=sample_rate)
    peaks = find_peaks(Sxx, distance, point_efficiency=point_efficiency)
    peaks = idxs_to_tf_pairs(peaks, t, f)
    return hash_points(peaks, filename)

def fingerprint_audio(frames, sample_rate=11025, distance=30, point_efficiency=0.4):
    f, t, Sxx = my_spectrogram(frames, sample_rate)
    peaks = find_peaks(Sxx, distance, point_efficiency=point_efficiency)
    peaks = idxs_to_tf_pairs(peaks, t, f)
    return hash_points(peaks, "recorded")
