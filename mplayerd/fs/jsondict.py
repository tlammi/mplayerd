import os
import random
import string
import json


class JsonDict:

    def __init__(self, path: str, write: bool):
        self._path = path
        self._write = write
        while True:

            self._tmppath = os.path.join(
                os.path.dirname(path),
                "tmp" + "".join(random.choices(string.ascii_uppercase, k=10))
            )
            if not os.path.exists(self._tmppath):
                break
        self._d = {}
        if os.path.exists(self._path):
            with open(self._path, "r") as rf:
                self._d = json.load(rf)

    def __iter__(self):
        return self._d.keys().__iter__()

    def __contains__(self, item):
        return item in self._d

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._write:
            with open(self._tmppath, "w") as wf:
                json.dump(self._d, wf, default=str)
            os.replace(self._tmppath, self._path)

    def __getitem__(self, item):
        return self._d[item]

    def __setitem__(self, key, value):
        self._d[key] = value

    def __delitem__(self, key):
        del self._d[key]
