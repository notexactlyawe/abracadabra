from numpy.fft import rfft
import numpy as np

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def fourier(window):
    f = np.abs(rfft(window)) ** 2
    n = len(window)
    return (2.0/n) * f[:n//2]
