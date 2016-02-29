from __future__ import division
from Tools.wavehelper import WaveHelper
import Tools.misc as misc
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
        self.mili = 16
        self.freq_arr = np.linspace(0, 22050, self.wav_r.samples_per_n_mili(self.mili)/2)

    def windows(self, l, n):
        chunk_size = self.wav_r.samples_per_n_mili(n)
        for chunk in misc.chunks(l, chunk_size):
            yield chunk

    def fingerprint(self):
        no = 1
        total_len = 0
        fprint = []
        for window in self.windows(self.samples, self.mili):
            f = misc.fourier(window)
            temp = []
            for num, seg in enumerate(misc.chunks(f, len(f)//16)):
                f_idx = np.where(seg==max(seg))[0][0] + num * len(f)//16
                freq = self.freq_arr[f_idx]
                temp.append(freq)
            fprint.append(freq)
        return fprint
    
if __name__ == "__main__":
    f = Fingerprint(filename="Samples/336739__astronautchild__goddog.wav")
    f.fingerprint()
