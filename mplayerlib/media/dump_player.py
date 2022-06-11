
import threading
import time
import tkinter

from .player import Player
from .src import Src


class DumpPlayer(Player):
    """
    Player frontend which only dumps the media name/path to terminal
    """
    def __init__(self, _: tkinter.Tk):
        self._src = None
        self._thread = threading.Thread(target=self._work)
        self._mut = threading.Lock()
        self._cv = threading.Condition()
        self._operate = True

    def __del__(self):
        self.stop()

    def play(self):
        self._thread.start()

    def stop(self):
        with self._mut:
            self._operate = False
        with self._cv:
            self._cv.notify()
        try:
            self._thread.join()
        except RuntimeError:
            pass

    def set_media_source(self, source: Src):
        with self._mut:
            self._src = source
        with self._cv:
            self._cv.notify()

    def _work(self):
        while True:
            while self._src is None and self._operate:
                self._cv.wait()
            with self._mut:
                if not self._operate:
                    break
            with self._mut:
                print(self._src.next())
            time.sleep(10)




