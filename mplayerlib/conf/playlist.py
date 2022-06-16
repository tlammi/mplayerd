import copy
import filecmp
import json
import jsonschema
import glob
import os

from datetime import datetime
from dataclasses import dataclass
from typing import Union, List
from . import uri
from . import schema
from .media import Media
from .. import media


class Playlist(list):

    def __init__(self, l: Union[list, str, dict], directory: str):
        super().__init__()
        if isinstance(l, list):
            for e in l:
                self._add_entry(e, directory)
        else:
            self._add_entry(l, directory)

    def _add_entry(self, e: Union[str, dict], d: str):
        if isinstance(e, str):
            scheme, resource = uri.parse(e)
            if scheme == "glob":
                tmp = glob.glob(resource, recursive=True, root_dir=d)
                tmp = [Media(os.path.join(d, t)) for t in tmp]
                self.extend(tmp)
            elif scheme is None:
                self.append(Media(os.path.join(d, resource)))
            else:
                raise ValueError(f"unsupported scheme: {scheme}")
        elif isinstance(e, dict):
            m = os.path.join(d, e["media"])
            a = e.get("after", 0)
            b = e.get("before", datetime.max)
            self.append(Media(m, after=a, before=b))
        else:
            raise TypeError()

    @staticmethod
    def load(path: str):
        path = os.path.realpath(path)
        d = os.path.dirname(path)
        with open(path, "r") as f:
            return Playlist(json.load(f), d)
