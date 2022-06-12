import time

from typing import Iterable, Any, Tuple
from datetime import datetime, timedelta

from . import util


class Scheduler:

    def __init__(self, sched_conf: Iterable[Tuple[util.EventPoint, Any]],
                 init_clock=time.time, work_clock=time.monotonic):
        """
        Constructs a scheduler

        This object stores bunch of events at specific times in the future

        The given datetimes are converted to timedeltas using init_clock.
        After this the event expiration is checked against the work_clock.
        This allows for more deterministic performance.

        The event time resolution is not exact as multiple calls to diferent
        clocks are required.

        :param sched_conf: Iterable of (<event time point>, <any payload>)
            event time point may be
                - datetime
                - timedelta
                - datetime string "yyyy-mm-dd hh:mm"
                - timedelta string "1h 10m 100s" (spaces optional)
        :param init_clock: Clock for resolving datetime
        :param work_clock: Actual clock to use for event expiration.
            work_clock() - work_clock() should return change in seconds as integer
        """
        self._sched = []
        self._start = work_clock()
        now = init_clock()
        self._clock = work_clock
        for k, v in sched_conf:
            datetime_or_timedelta = util.parse_event_time(k)
            if isinstance(datetime_or_timedelta, datetime):
                tdelta = datetime_or_timedelta - datetime.fromtimestamp(now)
            elif isinstance(datetime_or_timedelta, timedelta):
                tdelta = datetime_or_timedelta
            else:
                raise TypeError(f"event time is of unsupported type {type(datetime_or_timedelta)}")
            self._sched.append((tdelta, v))

        def key(arg):
            return arg[0]

        self._sched.sort(key=key)

    def already_expired(self, override_clock=None):
        """
        Get already expired events

        :param override_clock: Override work_clock given in ctor
        :return: Yields already expired event payloads
        """
        t = (override_clock or self._clock)() - self._start
        t = timedelta(seconds=t)
        for value in [v for k, v in self._sched if k < t]:
            yield value

    def next(self, override_clock=None):
        """
        Get next expiring event

        :return: (timedelta, payload) or (None, None) if no events left
        """
        t = (override_clock or self._clock)() - self._start
        t = timedelta(seconds=t)

        try:
            return [v for v in self._sched if v[0] > t][0]
        except IndexError:
            return None, None
