
import threading


class Timer:

    def __init__(self, interval: float, on_event, args=None, kwargs=None):
        self._interval = interval
        self._on_event = on_event
        self._args = args or []
        self._kwargs = kwargs or {}
        self._timer = None
        self._make_timer()

    def cancel(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None

    def _step(self):
        self._on_event(*self._args, **self._kwargs)
        self._make_timer()

    def _make_timer(self):
        self._timer = threading.Timer(self._interval, self._step)
        self._timer.start()
