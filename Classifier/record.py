import threading
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

class RecordThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_request = threading.Event()
        self.frames = []
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=FORMAT, channels=CHANNELS,
                                 rate=RATE, input=True,
                                 frames_per_buffer=CHUNK)

    def run(self):
        while not self.stop_request.isSet():
            data = self.stream.read(CHUNK)
            self.frames.append(data)

    def join(self, timeout=None):
        self.stop_request.set()
        super(RecordThread, self).join(timeout)
        return self.frames

if __name__ == "__main__":
    rec_thr = RecordThread()
    rec_thr.start()
    raw_input("> ")
    frames = rec_thr.join()
    print frames
