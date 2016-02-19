import wave
import struct

def read_whole(filename):
    wav_r = wave.open(filename, 'r')
    ret = []
    while wav_r.tell() < wav_r.getnframes():
        decoded = struct.unpack("<h", wav_r.readframes(1))
        ret.append(decoded)
    return ret

class WaveHelper():
    def __init__(self, filename, read):
        mode = 'r' if read else 'w'
        self.wav = wave.open(filename, mode)

    def read_n_mili(self, n):
        ret = []

        time_per_sample = (1.0 / self.wav.getframerate()) * 1000
        samples_to_get  = int(n / time_per_sample)

        if samples_to_get == 0:
            samples_to_get = 1

        for _ in range(samples_to_get):
            try:
                decoded = struct.unpack("<h", self.wav.readframes(1))
            except:
                # if samples left < samples_to_get
                # ie readframes(1) returns ''
                break
            if len(decoded) == 2:
                ret.append((decoded[0] + decoded[1]) / 2)
            else:
                ret.append(decoded[0])
        return ret

    def rewind(self):
        self.wav.rewind()

    def pos(self):
        return self.wav.tell()

    def seek(self, sample_no):
        self.wav.setpos(sample_no)
