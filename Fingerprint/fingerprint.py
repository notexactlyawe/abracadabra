from Tools.wavehelper import WaveHelper
import Tools.misc as misc
import numpy as np
import matplotlib.pyplot as plt
import logging

class Fingerprint:
    def __init__(self):
        pass

    def windows(self, l, n):
        chunk_size = self.wav_r.samples_per_n_mili(n)
        for chunk in misc.chunks(l, chunk_size):
            yield chunk

    def fingerprint(self):
        pass

if __name__ == "__main__":
    f = Fingerprint(filename="Samples/336739__astronautchild__goddog.wav")
    f.fingerprint()
