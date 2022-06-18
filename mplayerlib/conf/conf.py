import copy
import json
import logging
import os.path
import logging

from typing import List

from . import uri
from .playlist import Playlist
from .schedule import Schedule

LOGGER = logging.getLogger(__name__)


class Conf(dict):
    """
    Root configuration object
    """

    def __init__(self, d: dict = None, directory: str = None):
        super().__init__(**(d or dict()))
        if d is None:
            self["playlists"] = dict()
            self["schedule"] = Schedule([])
            return
        self.directory = os.path.realpath(directory)

        for k, v in self["playlists"].items():
            if isinstance(v, str):
                scheme, resource = uri.parse(v)
                if scheme == "inc":
                    p = os.path.join(self.directory, resource)
                    self["playlists"][k] = Playlist.load(p)
                else:
                    self["playlists"][k] = Playlist(v, directory)
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
            c = Conf(json.load(f), d)
        errs = c._errors()
        if errs:
            raise ValueError(f"Validation errors in config: {errs}")
        return c

    def _errors(self) -> List[str]:
        """
        Run configuration checks and return found errors
        :return: Empty list if no errors, either list of errors found
        """
        errs = []
        for _, playlist_name in self.schedule:
            if playlist_name not in self.playlists:
                errs.append(f"Schedule contains non-existent playlist '{playlist_name}'")
        return errs

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
