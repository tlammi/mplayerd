import threading
import logging
from typing import List
from datetime import datetime

import mplayerlib

LOGGER = logging.getLogger(__name__)


class SchedWorker:
    """
    Thread managing schedule and acting based on those
    """

    def __init__(self, conf: mplayerlib.conf.Conf, frontends: List[mplayerlib.media.Player]):
        self._conf = conf
        self._sched = mplayerlib.sched.Scheduler(conf.schedule)
        self._fronts = frontends
        self._cv = threading.Condition()
        self._operate = True

        previous = self._sched.last_expired()
        if previous:
            for f in self._fronts:
                f.set_media_source(self._conf.playlists[previous])

        self._t = threading.Thread(target=self._work)
        self._t.start()

    def update_conf(self, conf: mplayerlib.conf.Conf):
        """
        Set the worker schedule to a new configuration
        """
        LOGGER.debug("Updating schedule configuration")
        with self._cv:
            self._conf = conf
            self._sched = mplayerlib.sched.Scheduler(conf.schedule)
            previous = self._sched.last_expired()
            for f in self._fronts:
                f.set_media_source(self._conf.playlists[previous])
            self._cv.notify()

    def terminate(self):
        """
        Signal to terminate the worker
        """
        with self._cv:
            self._operate = False
            self._cv.notify()
        try:
            self._t.join()
        except RuntimeError:
            pass

    def _work(self):
        with self._cv:
            while True:
                sched = self._sched
                conf = self._conf
                dur, playlist = sched.next()
                if dur is not None:
                    tpoint = datetime.now() + dur
                    LOGGER.info(f"Next playlist '{playlist}' after '{dur}' which is at '{tpoint}'")
                    notified = self._cv.wait(dur.total_seconds())
                else:
                    LOGGER.info("No more events left in schedule")
                    self._cv.wait()
                    notified = True
                if notified:
                    if not self._operate:
                        break
                    continue
                else:
                    for f in self._fronts:
                        f.set_media_source(conf.playlists[playlist])
