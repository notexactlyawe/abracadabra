import Tools.wavehelper as wvhelp
import wave

filename = 'Samples/test.wav'

def test_read_whole_len():
    wav_r = wave.open(filename, 'r')
    expected_len = wav_r.getnframes()
    wav_r.close()
    actual_len = len(wvhelp.read_whole(filename))
    print "{0} == {1}".format(expected_len, actual_len)
    assert expected_len == actual_len

def test_read_n_mili_len():
    wav_r = wave.open(filename, 'r')
    t_p_s = (1.0 / wav_r.getframerate()) * 1000
    s_t_g = int(16 / t_p_s)
    wav_r.close()

    w = wvhelp.WaveHelper(filename, True)
    ms_samples = w.read_n_mili(16)
    print ms_samples
    print "exp: {0}, act {1}".format(s_t_g, len(ms_samples))
    assert s_t_g == len(ms_samples)

def test_read_n_mili_end_file():
    w = wvhelp.WaveHelper(filename, True)
    w.seek(w.wav.getnframes() - 1)
    samples = w.read_n_mili(16)
    assert len(samples) == 1

def test_read_n_mili_type():
    w = wvhelp.WaveHelper(filename, True)
    samples = w.read_n_mili(16)
    assert type(samples) is list
    assert type(samples[0]) is int
# Maybe figure out how to compare graphs?
