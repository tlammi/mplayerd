import json
import os
import shutil
from typing import Union

from .conf import Conf


class Workspace:
    """
    Copy of source files to allow safe handling of deleted files

    This object is used to keep duplicate data of source files somewhere
    else in the file system. Due to this it is safe to delete various.
    files from the source directory without affecting the process.

    Workspace consists of two slots, A and B which are written in turns
    allowing a fallback in case something goes wrong when copying a source directory.
    This might be the case e.g. if an invalid configuration is placed in the
    source directory.

    Only configuration and media files (etc.) are copied.
    """

    def __init__(self, work_path: str):
        """
        :param work_path: Path to workspace. Directory path is populated recursively if it does not exist
        :param conf: Config loaded from the source directory
        """
        os.makedirs(work_path, exist_ok=True)
        self._work_path = work_path
        self._a = os.path.join(self._work_path, "a")
        self._b = os.path.join(self._work_path, "b")
        self._active = self._b

    def load(self, conf: Union[Conf, str]):
        """
        Copy workspace from conf to workspace

        :param conf:
        :return:
        """
        if isinstance(conf, str):
            conf = Conf.load(conf)
        slot = self._next()
        shutil.rmtree(slot, ignore_errors=True)
        os.makedirs(slot, exist_ok=True)
        with open(os.path.join(slot, "mplayer.conf"), "w") as f:
            json.dump(conf.dump(), f, indent=4)
        for p in conf.playlists.values():
            for src_abs in p:
                src_rel = os.path.relpath(src_abs.media, conf.directory)
                dst_abs = os.path.join(slot, src_rel)
                os.makedirs(os.path.dirname(dst_abs), exist_ok=True)
                shutil.copy2(src_abs.media, dst_abs, follow_symlinks=True)
        self._active = slot
        path = os.path.join(slot, "mplayer.conf")
        return Conf.load(path)

    def _next(self):
        if self._active == self._a:
            return self._b
        else:
            return self._a
