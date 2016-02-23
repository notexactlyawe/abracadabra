def test_imports():
    import numpy as np
    from numpy.fft import rfft
    import matplotlib.pyplot as plot
    import threading
    import wave
    import pyaudio
    from nose.tools import assert_raises
    import struct

def test_correct_nose_dir():
    import Tools.wavehelper as wvhelp
    from Classifier.fingerprint import Fingerprint
