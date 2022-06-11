
import json
import jsonschema

from typing import Union
from .uri import Uri
from . import schema


class Playlist:

    def __init__(self, playlist: Union[Uri, dict]):
        if isinstance(playlist, Uri):
            if playlist.scheme != "inc":
                raise ValueError(f"Unsupported scheme: {playlist.scheme}")
            with open(playlist.resource) as f:
                playlist = json.load(f)
        jsonschema.validate(playlist, schema=schema.PLAYLIST)
