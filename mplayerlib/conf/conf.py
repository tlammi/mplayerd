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
        self.setdefault("playlists", dict())
        self.setdefault("schedule", Schedule([]))
        self.setdefault("root", ".")
        if d is None:
            return
        self.directory = os.path.join(directory, self["root"])
        self.directory = os.path.realpath(self.directory)

        for k, v in self["playlists"].items():
            if isinstance(v, str):
                scheme, resource = uri.parse(v)
                if scheme == "inc":
                    # NOTE: incs ignore "root" key
                    p = os.path.join(directory, resource)
                    LOGGER.info("Loading playlist from %s", p)
                    self["playlists"][k] = Playlist.load(p)
                else:
                    self["playlists"][k] = Playlist(v, self.directory)
            else:
                self["playlists"][k] = Playlist(v, self.directory)
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

    def __eq__(self, other):
        if not isinstance(other, Conf):
            return False
        return self.playlists == other.playlists and self.schedule == other.schedule


def parse_conf(path: str) -> Conf:
    dname = os.path.dirname(path)
    with open(path, "r") as f:
        return Conf(json.load(f), dname)
