
SCHEMA_URL = "https://json-schema.org/draft/2020-12/schema"

DEFINITIONS = {
    "Uri": {
        "type": "string",
        "format": "uri"
    },
    "TimePoint": {
        "oneOf": [
            {"type": "integer"},
            {"type": "string"}
        ]
    },
    "PlaylistConfig": {
        "type": "object",
        "properties": {
            "loop": {"type": "boolean"}
        }
    },
    "SchedEntry": {
        "type": "array",
        "prefixItems": [
            {"$ref": "#/$defs/TimePoint"},
            {"type": "string"}
        ],
        "items": False
    }
}


PLAYLIST = {
    "$schema": SCHEMA_URL,
    "$defs": DEFINITIONS,
    "type": "object",
    "patternProperties": {
        "^.*$": {"$ref": "#/$defs/Uri"}
    }
}

SCHEDULE = {
    "$schema": SCHEMA_URL,
    "$defs": DEFINITIONS,
    "type": "array",
    "items": {
        "$ref": "#/$defs/SchedEntry"
    }
}

CONF = {
    "$schema": SCHEMA_URL,
    "type": "object",
    "$defs": DEFINITIONS,
    "properties": {
        "version": {
            "type": "integer",
            "const": 0,
        },
        "config": {
            "type": "object",
            "properties": {
                "playlist-default": {"$ref": "#/$defs/PlaylistConfig"}
            }
        },
        "playlists": PLAYLIST,
        "schedule": SCHEDULE,
    },
    "required": ["version", "config", "playlists"]
}
