
import json
import jsonschema
import glob

from typing import Union
from .uri import Uri
from . import schema


class Playlist:

    def __init__(self, playlist: Union[Uri, dict], directory: str = None):
        if isinstance(playlist, Uri):
            if playlist.scheme == "glob":
                self._init_glob(playlist.resource, directory)
            elif playlist.scheme == "inc":
                with open(playlist.resource) as f:
                    self._init_obj(json.load(f))
            else:
                raise ValueError(f"Unsupported scheme: {playlist.scheme}")
        else:
            self._init_obj(playlist)

    def _init_glob(self, glob_str: str, directory: str = None):
        kwargs = {
            "recursive": True
        }
        if directory is not None:
            kwargs["root_dir"] = directory
        self.media = glob.glob(glob_str, **kwargs)

    def _init_obj(self, playlist: dict):
        jsonschema.validate(playlist, schema=schema.PLAYLIST)
