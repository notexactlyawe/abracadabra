import wave
import struct
from Tools.misc import chunks

class WaveHelper():
    def __init__(self, filename, read=True, debug=False):
        mode = 'r' if read else 'w'
        self.wav = wave.open(filename, mode)
        self.rate = self.wav.getframerate()
        self.count_frames = self.wav.getnframes()
        self.channels = self.wav.getnchannels()
        fmt_size = "h" if self.wav.getsampwidth() == 2 else "i"
        self.fmt = "<" + fmt_size * self.channels

    def unpacked_chunks(self, frames, size_chunk):
        for chunk in chunks(frames, size_chunk):
            yield struct.unpack(self.fmt, chunk)

    def read_whole(self):
        frames = self.wav.readframes(self.count_frames)
        size_ch = self.wav.getsampwidth() * self.channels
        if self.channels == 2:
            return [(ch[0] + ch[1]) / 2 for ch in self.unpacked_chunks(frames, size_ch)] 
        else:
            return unpacked_chunks(frames, size_chunk)
    
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
