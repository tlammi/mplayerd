import copy
import json
import os.path
import jsonschema

from typing import Union

from . import schema
from . import uri
from .playlist import Playlist
from .schedule import Schedule


class Conf(dict):
    """
    Root configuration object
    """

    def __init__(self, d: dict, directory: str):
        super().__init__(**d)
        self.directory = os.path.realpath(directory)
        #jsonschema.validate(self, schema=schema.CONF)

        for k, v in self["playlists"].items():
            if isinstance(v, str):
                scheme, resource = uri.parse(v)
                if scheme == "inc":
                    p = os.path.join(self.directory, resource)
                    self["playlists"][k] = Playlist.load(p)
            else:
                self["playlists"][k] = Playlist(v, directory)
        if "schedule" in self:
            self["schedule"] = Schedule(self["schedule"])
        else:
            self["schedule"] = Schedule([])

    @property
    def playlists(self):
        return self["playlists"]

    @property
    def schedule(self):
        return self["schedule"]

    @staticmethod
    def load(path: str) -> 'Conf':
        path = os.path.realpath(path)
        d = os.path.dirname(path)
        with open(path, "r") as f:
            return Conf(json.load(f), d)

    def dump(self):
        out = dict()
        out["version"] = self["version"]
        out["config"] = copy.deepcopy(self["config"])
        out["playlists"] = {k: v.dump() for k, v in self.playlists.items()}
        out["schedule"] = self.schedule.dump()
        return out


def parse_conf(path: str) -> Conf:
    dname = os.path.dirname(path)
    with open(path, "r") as f:
        return Conf(json.load(f), dname)
