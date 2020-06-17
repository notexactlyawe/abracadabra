import os
import wave
import threading
import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
SAVE_DIRECTORY = "test/ab/"

def record_audio(filename=None):
    """ Record 10 seconds of audio and optionally save it to a file """
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    write_frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.int16))
        if filename is not None:
            write_frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    if filename is not None:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    return np.hstack(frames)

class RecordThread(threading.Thread):
    def __init__(self, base_filename, piece_len=10, spacing=5):
        threading.Thread.__init__(self)
        self.stop_request = threading.Event()
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.chunks_per_write = int((RATE / CHUNK) * piece_len)
        self.chunks_to_delete = int((RATE / CHUNK) * spacing)
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)
        self.base_filename = base_filename
        self.file_num = self.get_file_num()

    def get_file_num(self):
        file_num = 1
        for f in os.listdir(SAVE_DIRECTORY):
            if self.base_filename not in f:
                continue
            # <filename><num>.wav
            num = int(f.split(".")[0][len(self.base_filename):])
            if num >= file_num:
                file_num = num + 1
        return file_num

    def write_piece(self):
        filename = os.path.join(SAVE_DIRECTORY, f"{self.base_filename}{self.file_num}.wav")
        frames_to_write = self.frames[:self.chunks_per_write]

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames_to_write))
        wf.close()

        # delete up until overlap point
        self.frames = self.frames[self.chunks_to_delete:]
        self.file_num += 1

    def run(self):
        while not self.stop_request.isSet():
            data = self.stream.read(CHUNK)
            self.frames.append(data)
            if len(self.frames) > self.chunks_per_write:
                self.write_piece()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def join(self, timeout=None):
        self.stop_request.set()
        super(RecordThread, self).join(timeout)

def gen_many_tests(base_filename, spacing=5, piece_len=10):
    rec_thr = RecordThread(base_filename, spacing=spacing, piece_len=piece_len)
    rec_thr.start()
    input("Press enter to stop recording")
    rec_thr.join()
