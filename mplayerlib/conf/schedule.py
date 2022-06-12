
import json
import jsonschema

from typing import Union
from . import schema
from .uri import Uri


class _ScheduleIter:
    def __init__(self, sched):
        self._iter = iter(sched)

    def __next__(self):
        return next(self._iter)


class Schedule:

    def __init__(self, sched: Union[Uri, list]):
        if isinstance(sched, Uri):
            if sched.scheme != "inc":
                raise ValueError(f"Unsupported scheme {sched.scheme}")
            with open(sched.resource, "r") as f:
                sched = json.load(f)
        jsonschema.validate(sched, schema=schema.SCHEDULE)
        self._sched = sched

    def __iter__(self):
        return _ScheduleIter(self._sched)

    def __next__(self):
        raise StopIteration()
