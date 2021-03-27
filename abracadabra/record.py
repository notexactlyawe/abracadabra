import os
import wave
import threading
import pyaudio
import numpy as np

CHUNK = 1024
"""Number of frames to buffer before writing."""
FORMAT = pyaudio.paInt16
"""The data type used to record audio. See ``pyaudio`` for constants."""
CHANNELS = 1
"""The number of channels to record."""
RATE = 44100
"""The sample rate."""
RECORD_SECONDS = 10
"""Number of seconds to record."""
SAVE_DIRECTORY = "test/"
"""Directory used to save audio when using :func:`gen_many_tests`."""


def record_audio(filename=None):
    """ Record 10 seconds of audio and optionally save it to a file

    :param filename: The path to save the audio (optional).
    :returns: The audio stream with parameters defined in this module.
    """
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
    """Used in :func:`gen_many_tests` to record audio.

    See :func:`gen_many_tests` for more details on this thread.
    """
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
        """Helper function to set the starting file_num to save with.

        Searches through :data:`SAVE_DIRECTORY` to find files saved under :attr:`self.base_filename`
        and increments the highest number it finds by 1.
        """
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
        """Writes an audio file."""
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
        """Main thread entry point. Call ``start()`` instead of this to run in a new thread."""
        while not self.stop_request.isSet():
            data = self.stream.read(CHUNK)
            self.frames.append(data)
            if len(self.frames) > self.chunks_per_write:
                self.write_piece()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def join(self, timeout=None):
        """Wait for the RecordThread to finish."""
        self.stop_request.set()
        super(RecordThread, self).join(timeout)


def gen_many_tests(base_filename, spacing=5, piece_len=10):
    """Generate sample files continuously by recording the microphone input.

    Takes a base_filename and saves overlapping audio segments of length ``piece_len`` to the path
    :data:`SAVE_DIRECTORY`/``base_filename<num>.wav`` where ``<num>`` is a monotonically
    increasing number.

    This function needs to be run manually since it will run until the user presses ``<Enter>``.

    It's intended that you run this function once per song that you want to generate test cases for.

    :param base_filename: The base filename to save recordings under. Should be without extension.
                          e.g. "mysong" instead of "mysong.wav"
    :param spacing: The number of seconds before each test starts recording.
    :param piece_len: The number of seconds for each recording.
    """
    rec_thr = RecordThread(base_filename, spacing=spacing, piece_len=piece_len)
    rec_thr.start()
    input("Press enter to stop recording")
    rec_thr.join()
