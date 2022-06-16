
from typing import Union
from datetime import datetime

Date = Union[datetime, str, int]

_FORMAT = "%Y-%m-%d %H:%M"


def to_datetime(d: Date) -> datetime:
    if isinstance(d, datetime):
        return d
    if isinstance(d, str):
        return datetime.strptime(d, _FORMAT)
    if isinstance(d, int):
        return datetime.fromtimestamp(d)
    raise TypeError()


def to_string(d: Date) -> str:
    if isinstance(d, int):
        d = to_datetime(d)
    if isinstance(d, datetime):
        return d.strftime(_FORMAT)
    if isinstance(d, str):
        return d
