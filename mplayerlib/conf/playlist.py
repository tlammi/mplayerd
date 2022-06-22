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
        self._directory = directory
        if isinstance(l, list):
            for e in l:
                self._add_entry(e, self._directory)
        else:
            self._add_entry(l, self._directory)
        self._iter = iter(self)

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
            e_media = e["media"]
            if isinstance(e_media, str):
                e_media = [e_media]
            if not isinstance(e_media, list):
                raise TypeError()
            for em in e_media:
                scheme, resource = uri.parse(em)
                a = e.get("after", 0)
                b = e.get("before", datetime.max)
                if scheme == "glob":
                    tmp = glob.glob(resource, recursive=True, root_dir=d)
                    tmp = [Media(os.path.join(d, t), after=a, before=b) for t in tmp]
                    self.extend(tmp)
                elif scheme is None:
                    self.append(Media(os.path.join(d, resource), after=a, before=b))
                else:
                    raise ValueError(f"Unsupported scheme: '{scheme}'")
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
            media = os.path.relpath(m.media, self._directory)
            d = {"media": media, "after": a}
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
