from Classifier.fingerprint import Fingerprint
from nose.tools import assert_raises

def test_init_no_args():
    assert_raises(ValueError, Fingerprint)
