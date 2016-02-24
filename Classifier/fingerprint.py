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
import Tools.misc as misc
from numpy.fft import rfft
import numpy as np
import matplotlib.pyplot as plt

class Fingerprint():
    def __init__(self, filename=None, rec_stream=None):
        if filename is None and rec_stream is None:
            raise ValueError('No filename or stream provided')
        if filename is None and rec_stream is not None:
            raise NotImplementedError('Sorry guys')
        self.wav_r = WaveHelper(filename, read=True, debug=True)
        self.samples = self.wav_r.read_whole()

    def windows(self, l, n):
        chunk_size = self.wav_r.samples_per_n_mili(n)
        for chunk in misc.chunks(l, chunk_size):
            yield chunk
        
    def fourier(self, window):
        return rfft(window)

    def fingerprint(self):
        no = 1
        total_len = 0
        for window in self.windows(self.samples, 16):
            f = self.fourier(window)
    
if __name__ == "__main__":
    f = Fingerprint(filename="Samples/336739__astronautchild__goddog.wav")
    f.fingerprint()
