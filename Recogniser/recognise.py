"""
In this file
given some audio
fingerprint
compare this fingerprint to existing
"""
from Classifier.fingerprint import Fingerprint
import matplotlib.pyplot as plt

class Recognise():
    def __init__(self):
        self.filename = 'Samples/336739__astronautchild__goddog.wav'
        self.f = Fingerprint(self.filename)
        self.fprint = self.f.fingerprint()
        print "Recognise initialised"

    def compare(self, sample, fprint):
        t_comp = []
        for win_start in range(0, len(fprint)):
            print "\rComparing {0} of {1}".format(win_start, len(fprint)),
            win_comp = []
            for idx, window in enumerate(sample):
                try:
                    win_or = fprint[win_start + idx]
                except:
                    win_or = None
                win_comp.append(self.compare_window(window, win_or))
            t_comp.append(win_comp)
        plt.plot([sum(win) for win in t_comp])
        plt.show()

    def compare_window(self, window, fprint):
        if fprint is None:
            return sum(window)
        res = 0
        for x, y in map(None, window, fprint):
            if x is None:
                res += y
            else:
                res += abs(x-y)
        return res

if __name__ == "__main__":
    r = Recognise()
    f = Fingerprint(r.filename)
    sample = f.fingerprint()[40:80]
    r.compare(sample, r.fprint)
