
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

    def __init__(self, d: dict, directory: str = None):
        """
        Create a new configuration object

        :param d: Deserialized data
        :param directory: Directory which contained the file. Used for relative references
            Relative imports do not work without this
        """
        jsonschema.validate(d, schema=schema.CONF)
        self.playlists = []
        self.schedule = Schedule([])

        c = d["config"]
        if "playlist-default" in c:
            playlist_config = c["playlist-default"]
        else:
            playlist_config = {}

        for k, v in d["playlists"].items():
            if isinstance(v, str):
                v = Uri.parse(v, directory)
            self.playlists.append(Playlist(v, directory, playlist_config))

        if "schedule" in d:
            v = d["schedule"]
            if isinstance(v, str):
                v = Uri.parse(v, directory)
            self.schedule = Schedule(v)

    @staticmethod
    def load(path: str):
        """
        Load configuration from a file

        :param path: Path to configuration file
        :return: Config object constructed from the file
        """
        d = os.path.realpath(os.path.dirname(path))
        with open(path, "r") as f:
            return Conf(json.load(f), d)
