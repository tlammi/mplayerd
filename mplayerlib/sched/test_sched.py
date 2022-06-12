import time
from datetime import datetime, timedelta

from .scheduler import Scheduler


def test_ctor():
    Scheduler([("2022-12-12 16:59", None)])
    Scheduler([("1h 10m 100s", None)])
    Scheduler([(datetime.fromtimestamp(0), None)])
    Scheduler([(timedelta(), None)])


EVENTS = [
    ("1970-02-02 12:00", 0),
    ("1h", 1),
    (datetime.now(), 2),
    (timedelta(100), 3),
]


def test_expired():
    s = Scheduler(EVENTS)
    expired = [i for i in s.already_expired()]
    assert(expired == [0, 2])

    def inf_clock():
        return 2**46
    expired = [i for i in s.already_expired(inf_clock)]
    assert(expired == [0, 2, 1, 3])


def test_last_expired():
    s = Scheduler(EVENTS)
    value = s.last_expired()
    assert(value == 2)

    def future_clock():
        return time.monotonic() + 60*60*2
    value = s.last_expired(future_clock)
    assert(value == 1)


def test_next():
    s = Scheduler(EVENTS)
    _, value = s.next()
    assert(value == 1)

    def past_clock():
        return time.monotonic() - 100
    _, value = s.next(past_clock)
    assert(value == 2)
