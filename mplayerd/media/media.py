
import tempfile
import os
import logging

LOGGER = logging.getLogger(__name__)


class Media:

    def __init__(self, file: str, options: dict = None):
        options = options or {}
        self._orig_file = file
        suffix = self._orig_file.split(".")[-1]
        self._fhandle, self._file = tempfile.mkstemp(suffix=suffix)
        with open(self._file, "w+b") as wf:
            with open(self._orig_file, "r+b") as rf:
                wf.write(rf.read())

        self._options = []
        for option, value in options.items():
            self._options.append(f"{option}={value}")

    def __del__(self):
        os.close(self._fhandle)
        os.remove(self._file)

    @property
    def file(self):
        return self._file

    @property
    def options(self):
        return self._options

