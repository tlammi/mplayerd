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


class Playlist(list, media.Src):

    def __init__(self, l: Union[list, str, dict], directory: str):
        super().__init__()
        if isinstance(l, list):
            for e in l:
                self._add_entry(e, directory)
        else:
            self._add_entry(l, directory)
        self._iter = iter(self)

    def _add_entry(self, e: Union[str, dict], d: str):
        if isinstance(e, str):
            scheme, resource = uri.parse(e)
            print(f"{scheme=}, {resource=}")
            if scheme == "glob":
                print(f"root dir: {d=}")
                tmp = glob.glob(resource, recursive=True, root_dir=d)
                print(f"glob: {tmp=}")
                tmp = [Media(os.path.join(d, t)) for t in tmp]
                self.extend(tmp)
            elif scheme is None:
                self.append(Media(os.path.join(d, resource)))
            else:
                raise ValueError(f"unsupported scheme: {scheme}")
        elif isinstance(e, dict):
            scheme, resource = uri.parse(e["media"])
            if scheme == "glob" or scheme is None:
                m = os.path.join(d, resource)
            else:
                raise TypeError()
            a = e.get("after", 0)
            b = e.get("before", datetime.max)
            self.append(Media(m, after=a, before=b))
        else:
            raise TypeError()

    def __bool__(self):
        return len(self) != 0

    @staticmethod
    def load(path: str):
        path = os.path.realpath(path)
        d = os.path.dirname(path)
        with open(path, "r") as f:
            return Playlist(json.load(f), d)

    def next(self):
        stopped = False
        while True:
            try:
                m = next(self._iter)
                if m.active():
                    return m.media
            except StopIteration:
                if stopped:
                    # Avoid infinite loop
                    return None
                stopped = True
                self._iter = iter(self)

    def dump(self):
        out = []
        for m in self:
            a = int(m.after.timestamp())
            d = {"media": m.media, "after": a}
            try:
                # max() might overflow -> do not serialize
                b = int(m.before.timestamp())
                d["before"] = b
            except ValueError:
                pass
            out.append(d)
        return out

    def active(self) -> list:
        """
        Access set of media that is currently active
        :return:
        """
        return [m.media for m in self if m.active()]
