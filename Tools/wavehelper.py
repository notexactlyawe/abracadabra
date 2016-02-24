import wave
import struct

class WaveHelper():
    def __init__(self, filename, read):
        mode = 'r' if read else 'w'
        self.wav = wave.open(filename, mode)
        self.rate = self.wav.getframerate()
        self.count_frames = self.wav.getnframes()
        fmt_size = "h" if self.wav.getsampwidth() == 2 else "i"
        self.fmt = "<" + fmt_size * self.wav.getnchannels()

    def read_whole(self):
        ret = []
        self.rewind()
        while self.pos() < self.count_frames:
            decoded = struct.unpack(self.fmt, self.wav.readframes(1))
            ret.append(decoded)
        return ret
    
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
