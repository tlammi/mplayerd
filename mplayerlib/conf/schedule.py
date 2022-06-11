
import json
import jsonschema

from typing import Union
from . import schema
from .uri import Uri


class Schedule:

    def __init__(self, sched: Union[Uri, dict]):
        if isinstance(sched, Uri):
            if sched.scheme != "inc":
                raise ValueError(f"Unsupported scheme {sched.scheme}")
            with open(sched.resource, "r") as f:
                sched = json.load(f)
        jsonschema.validate(sched, schema=schema.SCHEDULE)
