
import abc
import threading
import time

from .src import Src


class Player(abc.ABC):

    @abc.abstractmethod
    def set_media_source(self, source: Src):
        """
        Set source for media

        Player uses this object to consume media.
        This method can be called during operation where
        the player should store the new media source and start
        consuming media from there when needed.

        :param source: Media source to use next
        """

    @abc.abstractmethod
    def play(self):
        """
        Start player operation asynchronously
        """


class DumpPlayer(Player):
    """
    Player frontend which only dumps the media name/path to terminal
    """
    def __init__(self):
        self._src = None
        self._thread = threading.Thread(target=self._work)
        self._mut = threading.Lock()
        self._cv = threading.Condition()
        self._operate = True

    def __del__(self):
        with self._mut:
            self._operate = False
        with self._cv:
            self._cv.notify()
        try:
            self._thread.join()
        except RuntimeError:
            pass

    def play(self):
        self._thread.start()

    def set_media_source(self, source: Src):
        with self._mut:
            self._src = source
        with self._cv:
            self._cv.notify()

    def _work(self):
        while self._operate:
            while self._src is None and self._operate:
                self._cv.wait()
            if not self._operate:
                break
            with self._mut:
                print(self._src.next())
            time.sleep(10)


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

