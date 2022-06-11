
from .player import Player
from .vlc_player import VlcPlayer
from .dump_player import DumpPlayer


_PLAYER_MAP = {
    "dump": DumpPlayer,
    "vlc": VlcPlayer
}


def supported_players():
    """
    List supported player names
    :return:
    """
    return list(_PLAYER_MAP.keys())


def player(name: str) -> Player:
    """
    Make player object based on name

    :param name: Name of the player
    :return:
    """
    return _PLAYER_MAP[name]()

