"""
TODO in this file

Place save_recording into a save class
Possibly make it into a thread that reads from RecordThread
look at the docs for stop_stream/close/terminate

"""
import threading
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

class RecordThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_request = threading.Event()
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)

    def run(self):
        while not self.stop_request.isSet():
            data = self.stream.read(CHUNK)
            self.frames.append(data)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def join(self, timeout=None):
        self.stop_request.set()
        super(RecordThread, self).join(timeout)
        return self.frames

def save_recording(recording, filename):
    audio = pyaudio.PyAudio()
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

if __name__ == "__main__":
    rec_thr = RecordThread()
    rec_thr.start()
    filename = raw_input("> ")
    frames = rec_thr.join()
    save_recording(frames, filename)
