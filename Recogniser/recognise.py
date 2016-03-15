from Classifier.fingerprint import Fingerprint
import matplotlib.pyplot as plt
import logging

class Recognise():
    def __init__(self):
        self.filename = 'Samples/336739__astronautchild__goddog.wav'
        self.f = Fingerprint(self.filename)
        self.fprint = self.f.fingerprint()
        self.window_size = 22050/16.0
        logging.debug("Recognise initialised")

    def compare(self, sample, fprint):
        t_comp = []
        for win_start in range(0, len(fprint)):
            logging.info("Comparing {0} of {1}".format(win_start+1, len(fprint)))
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
        """
        Takes in two lists of frequencies
        and compares them to produce a similarity
        figure.
        The figures it takes in should be frequencies
        with the max amplitudes in segments of a 
        fourier transformed window
        """
        if fprint is None:
            return 0.5 * len(window)
        res = 0
        for x, y in map(None, window, fprint):
            if x is None:
                res += 0.5
            else:
                res += abs(x-y) / self.window_size
        return res

if __name__ == "__main__":
    r = Recognise()
    f = Fingerprint(r.filename)
    sample = f.fingerprint()[40:80]
    r.compare(sample, r.fprint)
