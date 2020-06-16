import uuid
import numpy as np
from pydub import AudioSegment
from scipy.signal import spectrogram
from scipy.ndimage import maximum_filter

def my_spectrogram(audio, sample_rate, fft_window_size_s=0.1):
    # default 100ms segments (allows for 600BPM music)
    nperseg = int(sample_rate * fft_window_size_s)
    return spectrogram(audio, sample_rate, nperseg=nperseg)

def file_to_spectrogram(filename, rate=11025):
    a = AudioSegment.from_file(filename).set_channels(1).set_frame_rate(rate)
    audio = np.frombuffer(a.raw_data, np.int16)
    return my_spectrogram(audio, rate)

def find_peaks(Sxx, distance, point_efficiency=1):
    data_max = maximum_filter(Sxx, size=distance, mode='constant', cval=0.0)
    peak_goodmask = (Sxx == data_max)  # good pixels are True
    y_peaks, x_peaks = peak_goodmask.nonzero()
    peak_values = Sxx[y_peaks, x_peaks]
    i = peak_values.argsort()[::-1]
    # get co-ordinates into arr
    j = [(y_peaks[idx], x_peaks[idx]) for idx in i]
    peaks = []
    total = Sxx.shape[0] * Sxx.shape[1]
    # in a square with a perfectly spaced grid, we could fit area / distance^2 points
    # use point efficiency to reduce this, since it won't be perfectly spaced
    # accuracy vs speed tradeoff
    peak_target = int((total / (distance**2)) * point_efficiency)
    return j[:peak_target]

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

def fingerprint_file(filename, sample_rate=11025, distance=40, point_efficiency=1):
    f, t, Sxx = file_to_spectrogram(filename, rate=sample_rate)
    peaks = find_peaks(Sxx, distance, point_efficiency=point_efficiency)
    peaks = idxs_to_tf_pairs(peaks, t, f)
    return hash_points(peaks, filename)

def fingerprint_audio(frames, sample_rate=11025, distance=40, point_efficiency=1):
    f, t, Sxx = my_spectrogram(frames, sample_rate)
    peaks = find_peaks(Sxx, distance, point_efficiency=point_efficiency)
    peaks = idxs_to_tf_pairs(peaks, t, f)
    return hash_points(peaks, "recorded")
