import copy
import json
import jsonschema
import glob
import os

from typing import Union
from .uri import Uri
from . import schema
from .. import media


class Playlist(media.Src):

    def __init__(self, playlist: Union[Uri, dict, list], directory: str, default_config: dict = None):
        """
        Init

        :param playlist:
        :param directory: Path to containing directory. Used for relative globs
        :param default_config: Configuration options to use in case no internal config is specified
        """
        self.media = []
        self.directory = directory
        default_config = default_config or {}
        if isinstance(playlist, Uri):
            if playlist.scheme == "glob":
                self._init_glob(playlist.resource)
            elif playlist.scheme == "inc":
                with open(playlist.resource) as f:
                    self._init_obj(json.load(f))
            else:
                raise ValueError(f"Unsupported scheme: {playlist.scheme}")
        elif isinstance(playlist, list):
            self.media = [os.path.realpath(os.path.join(self.directory, i)) for i in playlist]
        else:
            self._init_obj(playlist)
        self._iter = iter(self.media)
        if "loop" in default_config:
            self._loop = default_config["loop"]

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memodict))
        return result

    def dump(self) -> list:
        """
        """
        return [os.path.relpath(m, self.directory) for m in self.media]

    def next(self) -> str:
        try:
            return next(self._iter)
        except StopIteration:
            if self._loop:
                self._iter = iter(self.media)
                return next(self._iter)

    def _init_glob(self, glob_str: str):
        self.media = glob.glob(glob_str, recursive=True, root_dir=self.directory)

    def _init_obj(self, playlist: dict):
        # TODO: Implement
        jsonschema.validate(playlist, schema=schema.PLAYLIST)
