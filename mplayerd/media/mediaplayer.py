import vlc
import tkinter
import threading
import time
from .playlist import Playlist


class MediaPlayer:

    def __init__(self, initial_playlist: Playlist):
        self._start = time.time()
        self._sem = threading.Semaphore(1)
        self._current_plist = initial_playlist
        self._root = tkinter.Tk()
        self._root.title("Media Player Daemon")

        self._inst = vlc.Instance()
        self._mplayer = self._inst.media_player_new()
        self._mplayer.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self._media_ended_callback
        )
        self._videopanel = tkinter.Frame(self._root)
        self._canvas = tkinter.Canvas(self._videopanel)
        self._canvas.pack(fill=tkinter.BOTH, expand=1)
        self._videopanel.pack(fill=tkinter.BOTH, expand=1)

        self._index = 0

    def settings(self):
        pass

    def playlist(self):
        return self._current_plist

    def change_playlist(self, new_playlist: Playlist):
        self._current_plist = new_playlist

    def run_forever(self):
        self._root.after(0, self._main_task)
        self._root.mainloop()

    def _main_task(self):
        vlc_media = self._next_vlc_media()
        self._play_vlc_media(vlc_media)
        vlc_media.parse()
        self._root.after(vlc_media.get_duration(), self._main_task)

    def _play_vlc_media(self, vlc_media):
        self._mplayer.set_media(vlc_media)
        self._mplayer.set_hwnd(self._videopanel.winfo_id())
        if self._mplayer.play():
            raise ValueError("non-zero return value")

    def _next_vlc_media(self):
        media = self._current_plist[self._index]
        vlc_media = self._inst.media_new(media.file, *media.options)
        self._index = (self._index + 1) % len(self._current_plist)
        return vlc_media

    def _media_ended_callback(self, _):
        print(f"Event received. Time since start: {time.time()-self._start}s")
