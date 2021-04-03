""" This file contains the global settings for the project. """


SAMPLE_RATE = 44100
""" When a file is fingerprinted it is resampled to SAMPLE_RATE Hz.
Higher sample rates mean more accuracy in recognition, but also slower recognition
and larger database file sizes. Setting it higher than the sample rate for your
input files could potentially cause problems.
"""

PEAK_BOX_SIZE = 30
""" The number of points in a spectrogram around a peak for it to be considered a peak.
Setting it higher reduces the number of fingerprints generated but also reduces accuracy.
Setting it too low can severely reduce recognition speed and accuracy.
"""

POINT_EFFICIENCY = 0.8
""" A factor between 0 and 1 that determines the number of peaks found for each file.

Affects database size and accuracy.
"""

TARGET_START = 0.05
""" How many seconds after an anchor point to start the target zone for pairing.
See paper for more details.
"""

TARGET_T = 1.8
""" The width of the target zone in seconds. Wider leads to more fingerprints and greater accuracy
to a point, but then begins to lose accuracy.
"""

TARGET_F = 4000
""" The height of the target zone in Hz. Higher means higher accuracy.
Can range from 0 - (0.5 * SAMPLE_RATE).
"""

FFT_WINDOW_SIZE = 0.2
""" The number of seconds of audio to use in each spectrogram segment. Larger windows mean higher
frequency resolution but lower time resolution in the spectrogram.
"""

DB_PATH = "hash.db"
""" Path to the database file to use. """

NUM_WORKERS = 24
""" Number of workers to use when registering songs. """
