
import threading


class Timer:
    """
    Interval timer for firing events periodically after each interval
    """

    def __init__(self, interval: float, on_event, args=None, kwargs=None):
        """
        Init timer

        :param interval: Event interval in seconds
        :param on_event: Callable invoked after each interval
        :param args: Args to pass to on_event
        :param kwargs: Kwargs to pass to on_event
        """
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
