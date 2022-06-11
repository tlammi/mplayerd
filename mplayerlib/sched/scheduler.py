from typing import Iterable, Any, Callable
import time
from .util import *


class Scheduler:

    def __init__(self, sched_conf: Iterable[EventPoint, Any], on_event: Callable, clock=time.monotonic):
        self._sched = []
        for k, v in sched_conf:
            pass