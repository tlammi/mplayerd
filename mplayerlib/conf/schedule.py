
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
