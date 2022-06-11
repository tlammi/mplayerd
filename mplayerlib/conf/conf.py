
import jsonschema
from . import schema


class Conf:
    def __init__(self, d: dict):
        """
        Create a new configuration object
        """
        jsonschema.validate(d, schema=schema.CONF)
        self._d = d
