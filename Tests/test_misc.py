import matplotlib.pyplot as plt
import numpy as np
import Tools.misc as misc

def test_fourier_sin():
    no_samples = 600
    x = np.linspace(0, 1, 600)
    y = np.sin(50 * 2*np.pi*x)
    f = misc.fourier(y)
    # plt.plot(f)
    # plt.show()
    idx = np.where(f==max(f))[0][0]
    print idx
    assert(idx == 50)
