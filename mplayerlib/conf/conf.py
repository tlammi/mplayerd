
import json
import jsonschema
from typing import Union
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
        self.schedule = None

        for k, v in d["playlists"].items():
            if isinstance(v, str):
                v = Uri.parse(v, directory)
            self.playlists.append(Playlist(v))

        if "schedule" in d:
            v = d["schedule"]
            if isinstance(v, str):
                v = Uri.parse(v, directory)
            self.schedule = Schedule(v)
