from __future__ import division
"""
TODO in this file

Read in input
for each window
  Fourier transform it
  For each segment in fourier transform
    find max amplitude frequency
compress all this
store it
"""
from Tools.wavehelper import WaveHelper
from numpy.fft import rfft
import numpy as np
import matplotlib.pyplot as plt

class Fingerprint():
    def __init__(self, filename=None, rec_stream=None):
        if filename is None and rec_stream is None:
            raise ValueError('No filename or stream provided')
        if filename is None and rec_stream is not None:
            raise NotImplementedError('Sorry guys')
        self.wav_r = WaveHelper(filename, True)

    def fingerprint(self):
        windows = []
        nframes = self.wav_r.wav.getnframes()
        while self.wav_r.pos() < nframes:
            windows.append(self.wav_r.read_n_mili(16))
            print "\rReading file {0}%".format(self.wav_r.pos() / nframes * 100),
        freq_window = [rfft(i) for i in windows]
        xf = np.linspace(0.0, 1.0, len(windows[0])/2)
        plt.plot(xf, 2/len(windows[0]) * freq_window[0][:len(windows[0])/2])
        plt.show()
        plt.plot(windows[0])
        plt.show()

if __name__ == "__main__":
    f = Fingerprint(filename="Samples/test.wav")
    f.fingerprint()
