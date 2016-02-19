import wave
import struct

class WaveHelper():
    @staticmethod
    def read_whole(filename):
        wav_r = wave.open(filename, 'r')
        ret = []
        while wav_r.tell() < wav_r.getnframes():
            decoded = struct.unpack("<h", wav_r.readframes(1))
            ret.append(decoded)
        return ret
