import os
import wave
import array
import struct
from Tools.misc import chunks

class WaveHelper():
    def __init__(self, filename, read=True, debug=False):
        mode = 'r' if read else 'w'
        self.wav = wave.open(filename, mode)
        self.filename = filename
        self.rate = self.wav.getframerate()
        self.count_frames = self.wav.getnframes()
        self.channels = self.wav.getnchannels()
        self.fmt_size = "h" if self.wav.getsampwidth() == 2 else "i"
        self.fmt = "<" + self.fmt_size * self.channels

    def read_whole(self):
        a = array.array(self.fmt_size)
        a.fromfile(open(self.filename, 'rb'), os.path.getsize(self.filename)/a.itemsize)
        # calculate offset for 44B of header
        a = a[44/self.wav.getsampwidth():]
        print "WH: {0}".format(len(a))
        avg = lambda x, y: (x + float(y)) / 2
        if self.channels == 2:
            return map(avg, a[::2], a[1::2])
        return a
    
    def read_n_mili(self, n):
        ret = []
        samples_to_get = self.samples_per_n_mili(n)
        if samples_to_get == 0:
            samples_to_get = 1

        for _ in range(samples_to_get):
            try:
                decoded = struct.unpack(self.fmt, self.wav.readframes(1))
            except:
                # if samples left < samples_to_get
                # ie readframes(1) returns ''
                print "read_n_mili: reached end prematurely"
                break
            if len(decoded) == 2:
                ret.append((decoded[0] + decoded[1]) / 2)
            else:
                ret.append(decoded[0])
        return ret

    def samples_per_n_mili(self, n):
        time_per_sample = (1.0 / self.rate) * 1000
        return int(n / time_per_sample)

    def rewind(self):
        self.wav.rewind()

    def pos(self):
        return self.wav.tell()

    def seek(self, sample_no):
        self.wav.setpos(sample_no)
