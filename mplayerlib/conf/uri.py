import re
import os
from dataclasses import dataclass
from typing import Union


def parse(string: str) -> (Union[None, str], str):
    idx = string.find("://")
    if idx < 0:
        return None, string
    return string[:idx], string[idx+3:]


@dataclass
class Uri:
    scheme: str
    resource: str

    @staticmethod
    def parse(string: str, directory: str = None):
        """
        Parse URI from the given string

        :param string: URI to parse
        :param directory: Parent directory. Used if the URI is relative
        :return: URI
        """
        try:
            scheme, resource = re.fullmatch(r"^(\S+)://(.*)", string).group(1, 2)
        except AttributeError:
            raise ValueError("Invalid string")
        if directory is not None:
            resource = os.path.normpath(os.path.join(directory, resource))
        return Uri(scheme, resource)

    def __str__(self):
        return f"{self.scheme}://{self.resource}"

    def __repr__(self):
        return f"url:{str(self)}"
