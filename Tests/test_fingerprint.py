from Classifier.fingerprint import Fingerprint
from nose.tools import assert_raises

def test_init():
    assert_raises(ValueError, Fingerprint)
    f = Fingerprint(filename='Samples\\file3.wav')
