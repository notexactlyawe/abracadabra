import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 11025
RECORD_SECONDS = 10

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.float32))

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.hstack(frames)
