from totaltimeout import Timeout
from totaltimeout import _now

def test_import():
    import time
    try:
        assert time.monotonic is _now
    except AttributeError:
        assert time.time is _now

def test_zero_timeout():
    Timeout(0).time_left() == 0
