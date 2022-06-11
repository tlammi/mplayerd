import copy
import json
import jsonschema
import glob

from typing import Union
from .uri import Uri
from . import schema
from .. import media


class Playlist(media.Src):

    def __init__(self, playlist: Union[Uri, dict], directory: str = None):
        """
        Init

        :param playlist:
        :param directory: Path to containing directory. Used for relative globs
        """
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
        self._iter = iter(self.media)

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

    def next(self) -> str:
        return next(self._iter)

    def _init_glob(self, glob_str: str, directory: str = None):
        kwargs = {
            "recursive": True
        }
        if directory is not None:
            kwargs["root_dir"] = directory
        self.media = glob.glob(glob_str, **kwargs)

    def _init_obj(self, playlist: dict):
        jsonschema.validate(playlist, schema=schema.PLAYLIST)
