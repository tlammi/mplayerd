
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
