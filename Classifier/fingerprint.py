"""
TODO in this file

Read in input
for each window
  Fourier transform it
  For each segment in fourier transform
    find max amplitude frequency
compress all this
store it
"""
import wave

class Fingerprint():
    def __init__(self, filename=None, rec_stream=None):
        if filename is None and rec_stream is None:
            raise ValueError('No filename or stream provided')
        if filename is None and rec_stream is not None:
            raise NotImplementedError('Sorry guys')
        self.wav_file = wave.open(filename)

    def read_n_mili(self, n):
        """
        Returns an array of samples that represent n miliseconds
        """
        # assuming that this will be the only access to the
        # raw data we will check for multiple channels
        # and average them if they exist

        # calculate the number of samples to return
        time_per_sample = (1.0 / self.wav_file.getframerate()) * 1000
        samples_to_get  = int(16 / time_per_sample)

        if samples_to_get == 0:
            samples_to_get = 1

        raw = self.wav_file.readframes(samples_to_get)
        if self.wav_file.getnchannels() == 1:
            return raw
        else:
            raise NotImplementedError("Sorry guys")


