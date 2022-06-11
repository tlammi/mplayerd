
DEFINITIONS = {
    "Uri": {
        "type": "string",
        "format": "uri"
    },
    "TimePoint": {

    },
    "SchedEntry": {
        "type": "array",
        "prefixItems": [
            {"$ref": "#/$defs/TimePoint"},
            {}  # any object
        ],
        "items": False
    }
}


PLAYLIST = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$defs": DEFINITIONS,
    "type": "array",
    "items": {
        "$ref": "#/$defs/Uri",
    }
}

SCHEDULE = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$defs": DEFINITIONS,
    "type": "array",
    "items": {
        "$ref": "#/$defs/SchedEntry"
    }
}

CONF = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "$defs": DEFINITIONS,
    "properties": {
        "version": {
            "type": "integer",
            "const": 0,
        },
        "config": {
            "type": "object"
        },
        "playlists": PLAYLIST,
        "schedule": SCHEDULE,
    },
    "required": ["version", "config", "playlists"]
}
