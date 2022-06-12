
import json
import os.path

import jsonschema
from . import schema
from .uri import Uri
from .playlist import Playlist
from .schedule import Schedule


class Conf:
    """
    Root configuration object

    """

    def __init__(self, d: dict, directory: str, name: str):
        """
        Create a new configuration object

        :param d: Deserialized data
        :param directory: Directory which contained the file. Used for relative references
            Relative imports do not work without this
        """
        jsonschema.validate(d, schema=schema.CONF)
        self.playlists = {}
        self.schedule = Schedule([])
        # Directory containing config
        self.parent = directory
        # Config file name
        self.name = name

        self._c = d["config"]
        if "playlist-default" in self._c:
            playlist_config = self._c["playlist-default"]
        else:
            playlist_config = {}

        for k, v in d["playlists"].items():
            if isinstance(v, str):
                v = Uri.parse(v, directory)
            self.playlists[k] = Playlist(v, directory, playlist_config)

        if "schedule" in d:
            v = d["schedule"]
            if isinstance(v, str):
                v = Uri.parse(v, directory)
            self.schedule = Schedule(v)

    def dump(self) -> dict:
        out = {
            "version": 0,
            "config": self._c,
            "playlists": {k: p.dump() for k, p in self.playlists.items()},
            "schedule": self.schedule.dump()
        }
        return out

    @staticmethod
    def load(path: str):
        """
        Load configuration from a file

        :param path: Path to configuration file
        :return: Config object constructed from the file
        """
        d = os.path.realpath(os.path.dirname(path))
        n = os.path.basename(path)
        with open(path, "r") as f:
            return Conf(json.load(f), d, n)

    def __eq__(self, other: 'Conf'):
        if self._c != other._c:
            return False
        if self.playlists != other.playlists:
            return False
        if self.schedule != other.schedule:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
