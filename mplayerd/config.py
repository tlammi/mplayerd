import datetime
import os
from fs import JsonDict


class Config:

    def __init__(self, file: str):
        self._data = JsonDict(file, False)

    def media_sets(self):
        root = self._data["media-config"]["media-root"]
        set_config = self._data["media-config"]["media-sets"]

        for k, v in set_config.items():
            v["glob"] = os.path.join(root, v["glob"])
        return set_config

    def schedule(self):
        def config_to_sched_item(year, month, day, time, event_meta):
            hours, minutes = time.split(":")
            d = datetime.datetime(int(year), int(month), int(day), int(hours), int(minutes))
            return d, event_meta

        def sched_from_times(year, month, day, times):
            out = {}
            for timeins, event in times.items():
                key, value = config_to_sched_item(year, month, day, timeins, event)
                out[key] = value
            return out

        def sched_from_days(year, month, days):
            out = {}
            for day, times in days.items():
                out.update(sched_from_times(year, month, day, times))
            return out

        def sched_from_months(year, months):
            out = {}
            for month, days in months.items():
                out.update(sched_from_days(year, month, days))
            return out

        def parse_schedule(sched_config: dict):
            out = {}
            for year, months in sched_config.items():
                out.update(sched_from_months(year, months))
            return out

        sched_config = self._data["schedule"]
        return parse_schedule(sched_config)
