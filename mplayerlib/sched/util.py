
import re
from typing import Union
from datetime import datetime, timedelta

EventPoint = Union[datetime, timedelta, str]

_TIME_FORMAT = "%Y-%m-%d %H:%M"
_DATE_REGEX = re.compile(r"(\d+)(h|m|s)")

_UNIT_MULTIPIER = {
    "s": 1,
    "m": 60,
    "h": 60*60
}


def parse_event_time(e: EventPoint) -> Union[datetime, timedelta]:
    if isinstance(e, (datetime, timedelta)):
        return e
    if isinstance(e, str):
        try:
            return datetime.strptime(e, _TIME_FORMAT)
        except ValueError:
            pass
    match = _DATE_REGEX.findall(e)
    if not match:
        raise ValueError(f"Invalid string: {e}")
    delta = timedelta()
    for m in match:
        dur, unit = m
        delta += timedelta(seconds=dur*_UNIT_MULTIPIER[unit])
    return delta
