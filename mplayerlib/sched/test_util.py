from . import util

from datetime import datetime, timedelta


def test_parse_datetime():
    d = datetime.now()
    assert(d == util.parse_event_time(d))


def test_parse_timedelta():
    d = datetime.now() - datetime.fromtimestamp(0)
    assert(d == util.parse_event_time(d))


def test_parse_datetime_str():
    date_str = r"2022-01-01 12:00"
    expected = datetime(2022, 1, 1, 12, 0)
    assert(expected == util.parse_event_time(date_str))


def test_parse_timedelta_str():
    test_set = (
        ("1h 10m", timedelta(hours=1, minutes=10)),
        ("100s", timedelta(seconds=100))
    )
    for time_str, expected in test_set:
        assert(util.parse_event_time(time_str) == expected)
