import datetime
import threading
import pytest
import scheduler


def test_default():
    now = datetime.datetime.now()
    
    sem = threading.Semaphore(0)
    def cb(date, value):
        assert date == now
        assert value == "hello"
        sem.release()

    SCHEDULE = {
        now: "hello"
    }
    s = scheduler.Scheduler("default-value", SCHEDULE, cb)
    if not sem.acquire(timeout=1):
        raise AssertionError("No event received")

def test_current():
    now = datetime.datetime.now()

    def cb(*args):
        pass

    mock_time = now
    def datetime_mock():
        return mock_time

    SCHEDULE = {
        datetime.datetime.now() + datetime.timedelta(hours=1): "val0",
        datetime.datetime.now() + datetime.timedelta(hours=3): "val1"
    }
    s = scheduler.Scheduler("default-value", SCHEDULE, cb, datetime_mock)
    assert s.current_value() == "default-value"
    mock_time = now + datetime.timedelta(hours=1, minutes=1)
    assert s.current_value() == "val0"
    mock_time = now + datetime.timedelta(days=5)
    assert s.current_value() == "val1"

def test_past_and_future_events():
    now = datetime.datetime.now()

    sem = threading.Semaphore(0)
    def cb(date, value):
        assert value != "val0"
        assert value != "val2"
        if value == "val1":
            sem.release()
    
    SCHEDULE = {
        now - datetime.timedelta(hours=1): "val0",
        now: "val1",
        now + datetime.timedelta(hours=1): "val2"
    }

    s = scheduler.Scheduler("default-value", SCHEDULE, cb)
    if not sem.acquire(timeout=1):
        raise AssertionError("Event not fired")
