
import json
import jsonschema
from typing import Union
from . import schema
from .uri import Uri


class Conf:
    def __init__(self, d: dict, directory: str = None):
        """
        Create a new configuration object

        :param d: Deserialized data
        :param directory: Directory which contained the file. Used for relative references
            Relative imports do not work without this
        """
        jsonschema.validate(d, schema=schema.CONF)
        self._d = d

        Conf._resolve_incs(self._d["playlists"], directory)
        try:
            Conf._resolve_incs(self._d["schedule"], directory)
        except KeyError:
            pass

    @classmethod
    def _resolve_incs(cls, obj: Union[dict, list], directory: str):
        if isinstance(obj, dict):
            cls._resolve_incs_dict(obj, directory)
        else:
            cls._resolve_incs_list(obj, directory)

    @classmethod
    def _resolve_incs_dict(cls, d: dict, directory: str):
        for k, v in d.items():
            try:
                u = Uri.parse(v, directory)
                if u.scheme == "inc":
                    with open(u.resource, "r") as f:
                        d[k] = json.load(f)
            except ValueError:
                pass

    @classmethod
    def _resolve_incs_list(cls, a: list, directory: str):
        for i, v in enumerate(a):
            try:
                u = Uri.parse(v, directory)
                if u.scheme == "inc":
                    with open(u.resource, "r") as f:
                        a[i] = json.load(f)
            except ValueError:
                pass
