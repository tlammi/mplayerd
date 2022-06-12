import threading
from typing import List

import mplayerlib


class SchedWorker:
    """
    Thread managing schedule and acting based on those
    """

    def __init__(self, conf: mplayerlib.conf.Conf, frontends: List[mplayerlib.media.Player]):
        self._conf = conf
        self._sched = mplayerlib.sched.Scheduler(conf.schedule)
        self._fronts = frontends
        self._cv = threading.Condition()
        self._t = threading.Thread(target=self._work)
        self._t.start()

    def update_conf(self, conf: mplayerlib.conf.Conf):
        """
        Set the worker schedule to a new configuration
        """
        self._conf = conf
        self._sched = mplayerlib.sched.Scheduler(conf.schedule)

    def terminate(self):
        """
        Signal to terminate the worker
        """
        with self._cv:
            self._cv.notify()
        try:
            self._t.join()
        except RuntimeError:
            pass

    def _work(self):
        print(f"Already gone events {[i for i in self._sched.already_expired()]}")
        previous = self._sched.last_expired()
        print("setting playlist")
        for f in self._fronts:
            print(f"setting {f}")
            f.set_media_source(self._conf.playlists[previous])
        print("playlist set")
        while True:
            dur, playlist = self._sched.next()
            with self._cv:
                notified = self._cv.wait(dur)
                if notified:
                    break
                else:
                    for f in self._fronts:
                        f.set_media_source(self._conf.playlists[playlist])
