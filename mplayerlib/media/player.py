
import abc


class Player(abc.ABC):
    pass


class DumpPlayer(Player):
    """
    Player frontend which only dumps the media name/path to terminal
    """


class VlcPlayer(Player):
    """
    Player frontend using libvlc
    """


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

