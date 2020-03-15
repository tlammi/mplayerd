import time
import datetime
import bisect

from typing import Union


class Scheduler:

    def __init__(self, callback: callable, schedule: dict):
        """
        Initializes a scheduler

        :param callback: Callback invoked on event fire.
        :param schedule: Group of datetime objects telling the Scheduler when to fire
            NOTE: if the list contains events that have already passed, the latest
            passed event will fire immediately
        """
        self._arg_mapping = schedule
        self._sched = sorted(schedule)
        self._cb = callback

    def start(self):

        curtime = datetime.datetime.now()
        if len(self._sched) > 0 and curtime >= self._sched[0]:
            last_event = self._get_greatest_lt(curtime, self._sched)
            self._cb(last_event, self._arg_mapping[last_event])

        while True:
            try:
                next_wake = self._get_smallest_ge(datetime.datetime.now(), self._sched)
            except IndexError:
                break
            print(f"Current time: {datetime.datetime.now()}")
            print(f"Next wake up at: {next_wake}")
            sleep_duration = next_wake - datetime.datetime.now()
            print(f"Sleeping for: {sleep_duration}")
            time.sleep(sleep_duration.total_seconds())
            print(f"Invoking scheduling callback")
            self._cb(next_wake, self._arg_mapping[next_wake])

    @staticmethod
    def _get_greatest_lt(comp, listin: list):
        index = bisect.bisect(listin, comp)-1
        print(f"got index: {index}")
        return listin[index]

    @staticmethod
    def _get_smallest_ge(comp, listin: list):
        index = bisect.bisect(listin, comp)
        return listin[index]