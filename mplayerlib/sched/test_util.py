from . import util

from datetime import datetime, timedelta


def test_parse_datetime():
    d = datetime.now()
    assert(d == util.parse_event_time(d))


def test_parse_timedelta():
    d = datetime.now() - datetime.fromtimestamp(0)
    assert(d == util.parse_event_time(d))
