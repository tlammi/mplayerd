
import json
import jsonschema

from typing import Union
from . import schema
from .uri import Uri
from .. import timeutil


class Schedule(list):

    def __init__(self, l: list):
        super().__init__(l)
        for i, (t, v) in enumerate(self):
            self[i] = (timeutil.to_datetime(t), v)

        def key(pair):
            return pair[0]
        self.sort(key=key)

    def dump(self):
        out = []
        for t, v in self:
            out.append((t.timestamp(), v))
        return out

##class _ScheduleIter:
##    def __init__(self, sched):
##        self._iter = iter(sched)
##
##    def __next__(self):
##        return next(self._iter)
##
##
##class Schedule:
##
##    def __init__(self, sched: Union[Uri, list]):
##        if isinstance(sched, Uri):
##            if sched.scheme != "inc":
##                raise ValueError(f"Unsupported scheme {sched.scheme}")
##            with open(sched.resource, "r") as f:
##                sched = json.load(f)
##        jsonschema.validate(sched, schema=schema.SCHEDULE)
##        self._sched = sched
##
##    def __iter__(self):
##        return _ScheduleIter(self._sched)
##
##    def __next__(self):
##        raise StopIteration()
##
##    def dump(self):
##        return self._sched
##
##    def __eq__(self, other: 'Schedule'):
##        return self._sched == other._sched
##
##    def __ne__(self, other):
##        return not self.__eq__(other)
