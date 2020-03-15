import datetime
import re

DATE_REGEX = re.compile(r"\\(\d{4})(\d{2})(\d{2})\D{4}(\d{2})(\d{2})[^\\]*$")


def date_filter(files: list, notbefore: datetime.datetime, notafter: datetime.datetime):

    matches = [DATE_REGEX.findall(file)[0] for file in files]
    out = []
    for match, file in zip(matches, files):
        year, month, day, hour, minute = match
        year, month, day, hour, minute = int(year), int(month), int(day), int(hour), int(minute)
        while minute > 59:
            hour += 1
            minute -= 60
        while hour > 23:
            day += 1
            hour -= 24
        date = datetime.datetime(year, month, day, hour, minute)
        if notbefore <= date <= notafter:
            out.append(file)
    return out
