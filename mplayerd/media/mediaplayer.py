import vlc
import tkinter
import threading
import time

from . import playlist

class MediaPlayer:

    def __init__(self):
        self._start = time.time()
        self._mut = threading.Lock()
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
        self._plist = playlist.Playlist()
        self._iter = self._plist.inf_iter()

    def play(self):
        self._root.after(0, self._play_media)

    def run_forever(self):
        self._root.mainloop()

    def stop(self):
        pass
    
    def playlist(self):
        return self._plist

    def _play_media(self):
        print("Play media called")
        try:
            media = next(self._iter)
            vlc_media = self._inst.media_new(media.file, *media.options)
            self._mplayer.set_media(vlc_media)
            self._mplayer.set_hwnd(self._videopanel.winfo_id())
            if self._mplayer.play():
                raise ValueError("non-zero return value")
            print(f"{vlc_media.get_duration()}")
        except StopIteration:
            pass

    def _media_ended_callback(self, _):
        print(f"Event received. Time since start: {time.time()-self._start}s")
        self._root.after(0, self._play_media)


"""
class MediaPlayer:

    def __init__(self, initial_playlist: list):
        self._start = time.time()
        self._media_lock = threading.Lock()
        self._iter = iter(FairRndIterator.from_list(initial_playlist))
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

    def playlist_replace(self, new_playlist: list):
        with self._media_lock:
            self._iter = FairRndIterator.from_list(new_playlist)

    def run_forever(self):
        self._root.after(0, self._main_task)
        self._root.mainloop()

    def _main_task(self):
        with self._media_lock:
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
        media = next(self._iter)
        vlc_media = self._inst.media_new(media.file, *media.options)
        return vlc_media

    def _media_ended_callback(self, _):
        print(f"Event received. Time since start: {time.time()-self._start}s")
"""