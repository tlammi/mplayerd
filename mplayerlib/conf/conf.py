
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
        jsonschema.validate(self, schema=schema.CONF)

        for k, v in self["playlists"].items():
            if isinstance(v, str):
                scheme, resource = uri.parse(v)
                if scheme == "inc":
                    p = os.path.join(directory, resource)
                    self["playlists"][k] = Playlist.load(p)
            else:
                self["playlists"][k] = Playlist(v, directory)

    @staticmethod
    def load(path: str) -> 'Conf':
        path = os.path.realpath(path)
        d = os.path.dirname(path)
        with open(path, "r") as f:
            return Conf(json.load(f), d)


def parse_conf(path: str) -> Conf:
    dname = os.path.dirname(path)
    with open(path, "r") as f:
        return Conf(json.load(f), dname)
