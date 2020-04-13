
import iterators
import time
import sys
import threading
import glob
import enum
import os
import logging
import signal
import config

from datetime import datetime, timedelta
from media import MediaPlayer, Media
from scheduler import Scheduler


LOGGER = logging.getLogger()

def sched_event_handler(date: datetime, value: str, cookie: tuple):
    LOGGER.debug("Scheduling event fired")
    mplayer, playlist_files = cookie
    plist_file = playlist_files[value]
    plist = [Media(m, plist_file.options) for m in plist_file.media()]
    mplayer.playlist().clear()
    mplayer.playlist().extend(plist)
    LOGGER.debug("Scheduling event handled")

def event_loop(mplayer: MediaPlayer):
    sched_conf, playlists = config.load_configs(r"G:\googledrive\Skriinille")
    s = Scheduler(
        sched_conf.default,
        sched_conf.schedule(),
        sched_event_handler,
        (mplayer, playlists)
    )
    plist = playlists[s.current_value()]
    medias = [Media(m, plist.options) for m in plist.media()]
    mplayer.playlist().extend(medias)
    mplayer.play()

def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    mplayer = MediaPlayer()
    t = threading.Thread(target=event_loop, daemon=True, args=(mplayer,))
    t.start()
    mplayer.run_forever()
    t.join()

main()
