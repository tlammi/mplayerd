import sys

import vlc
import tkinter
import threading
import time
import enum
from .player import Player
from .src import Src


class OsType(enum.Enum):
    Linux = 0
    Windows = 1


def _os_type() -> OsType:
    if sys.platform.startswith("linux"):
        return OsType.Linux
    if sys.platform.startswith("win"):
        return OsType.Windows
    raise EnvironmentError("Only implemented for linux and windows")


def _create_vlc() -> vlc.Instance:
    """
    Create VLC library instance in platform abstract way
    :return: vlc.Instance
    """

    if _os_type() == OsType.Linux:
        args = ("--no-xlib",)
    else:
        args = ()
    return vlc.Instance(*args)


def _assign_to_window(mplayer, frame: tkinter.Frame):
    """
    Assign VLC media player to an existing window

    :param mplayer: Media player to insert
    :param frame: Frame where to insert the player
    """
    if _os_type() == OsType.Linux:
        mplayer.set_xwindow(frame.winfo_id())
    else:
        mplayer.set_hwnd(frame.winfo_id())


class VlcPlayer(Player):

    def __init__(self, root: tkinter.Tk):
        self._start = time.time()
        self._mut = threading.Lock()
        self._root = root
        self._root.title("Media Player Daemon")

        self._inst = _create_vlc()
        self._mplayer = self._inst.media_player_new()
        self._mplayer.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self._media_ended_callback
        )
        self._videopanel = tkinter.Frame(self._root)
        self._canvas = tkinter.Canvas(self._videopanel)
        self._canvas.pack(fill=tkinter.BOTH, expand=1)
        self._videopanel.pack(fill=tkinter.BOTH, expand=1)
        _assign_to_window(self._mplayer, self._videopanel)
        self._src = None

    def play(self):
        self._root.after(0, self._play_media)

    def set_media_source(self, source: Src):
        with self._mut:
            old = self._src
            self._src = source
        if source is not None and old is None:
            self.play()

    def stop(self):
        pass

    def _play_media(self):
        try:
            with self._mut:
                if self._src is None:
                    # Cannot do anything if no medias available
                    return
                try:
                    media = self._src.next()
                except StopIteration:
                    # No media available
                    return
            vlc_media = self._inst.media_new(media)
            self._mplayer.set_media(vlc_media)
            if self._mplayer.play():
                raise ValueError("non-zero return value")
        except StopIteration:
            pass

    def _media_ended_callback(self, _):
        print(f"Event received. Time since start: {time.time() - self._start}s")
        try:
            self._root.after(0, self._play_media)
        except RuntimeError:
            # E.g. when main thread has terminated
            pass

