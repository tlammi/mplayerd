import datetime
import threading
import logging

LOGGER = logging.getLogger(__name__)

class Scheduler:

    def __init__(self, default_value, schedule: dict, event_handler: callable, cookie=None, *, date_func=datetime.datetime.now):
        self._default = default_value
        self._sched = []
        self._date_func = date_func
        self._ehandler = event_handler
        self._cookie = cookie
        self._timers = []
        self.update_schedule(schedule)
    
    def __del__(self):
        self.cancel()

    def update_schedule(self, schedule: dict):
        LOGGER.info("Updating schedule")
        self.cancel()
        self._sched = []
        start = self._date_func()
        next_event = datetime.datetime.max
        for date, val in schedule.items():
            self._sched.append((date, val))
            LOGGER.debug("Scheduling event at %s", date)
            sleep_dur = (date - start).total_seconds()
            next_event = min(next_event, date)
            self._timers.append(threading.Timer(
                sleep_dur, self._ehandler, args=(date, val, self._cookie)
            ))
            self._timers[-1].daemon = True
            self._timers[-1].start()
        LOGGER.info("Schedule updated")
        if next_event < datetime.datetime.max:
            LOGGER.info("Next event at %s", next_event)
        else:
            LOGGER.info(f"No events scheduled")

    def current_value(self):
        if len(self._sched) == 0 or self._date_func() < self._sched[0][0]:
            return self._default
        for index, (date, value) in enumerate(self._sched):
            if date > self._date_func():
                return self._sched[index-1][1]
        return self._sched[-1][1]

    def cancel(self):
        for t in self._timers:
            t.cancel()
        self._timers = []
