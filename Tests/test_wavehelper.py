from Tools.wavehelper import WaveHelper

def test_read_whole_len():
    import wave

    filename = 'Samples/test.wav'

    wav_r = wave.open(filename, 'r')
    expected_len = wav_r.getnframes()
    actual_len = len(WaveHelper.read_whole(filename))
    print "{0} == {1}".format(expected_len, actual_len)
    assert expected_len == actual_len

# Maybe figure out how to compare graphs?
