import datetime
import json
import glob
import os

class ConfigFile:
    
    def __init__(self, path: str):
        self._path = path
    
    @property
    def path(self):
        return self._path

    @property
    def basename(self):
        return os.path.basename(self._path)
    
    def __repr__(self):
        return f"{self.__class__.__name__}[{self._path}]"

class ScheduleFile(ConfigFile):
    
    def __init__(self, path: str, date_format = "%Y-%m-%d %H:%M"):
        super().__init__(path)
        self._dformat = date_format

    @property
    def default(self):
        sched, _ = self._load_json()
        return sched
    
    def schedule(self, events_after: datetime.datetime = None):
        _, data = self._load_json()
        if events_after:
            out = dict(
                filter(
                    lambda key: key > events_after,
                    data.keys()
                )
            )
        else:
            out = data
        return out

    def _load_json(self):
        with open(self.path, "r") as f:
            raw_data = json.load(f)
        sched = {}
        default = None
        for rkey, rvalue in raw_data.items():
            if rkey == "default":
                default = rvalue
            else:
                okey = datetime.datetime.strptime(rkey, self._dformat)
                sched[okey] = rvalue
        return default, sched


class PlaylistFile(ConfigFile):
    
    def __init__(self, path: str, date_format = "%Y-%m-%d %H:%M"):
        super().__init__(path)
        self._dformat = date_format

    @property
    def algorithm(self):
        tmp = self._load_json()
        return tmp[0]

    @property
    def options(self):
        tmp = self._load_json()
        return tmp[3]
    
    def media(self, date: datetime.datetime = None):
        date = date or datetime.datetime.now()
        _, base_globs, delta_globs, _ = self._load_json()
        media = self._do_relative_glob(base_globs)

        for key, rule in delta_globs.items():
            key = datetime.datetime.strptime(key, self._dformat)
            if key <= date:
                try:
                    rm_files = self._do_relative_glob(rule["rm"])
                    media -= rm_files
                except KeyError:
                    pass
                try:
                    add_files = self._do_relative_glob(rule["add"])
                    media.update(add_files)
                except KeyError:
                    pass
        return media

    def _do_relative_glob(self, globlist: list):
        workdir = os.path.dirname(self.path)
        res = set()
        for g in globlist:
            g = os.path.join(workdir, g)
            res.update(glob.glob(g))
        return res

    def _load_json(self):
        with open(self.path, "r") as f:
            raw_data = json.load(f)
        try:
            algo = raw_data["algorithm"]
        except KeyError:
            algo = None
        
        media_base = raw_data["media-base"]
        try:
            media_delta =  raw_data["media-delta"]
        except KeyError:
            media_delta = {}
        try:
            options = raw_data["options"]
        except KeyError:
            options = []
        return algo, media_base, media_delta, options
        