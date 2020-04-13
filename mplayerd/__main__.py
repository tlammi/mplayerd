
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

def playlist_config_to_media_list(plist_config: config.PlaylistFile):
    media = []
    tmp = list(plist_config.media())
    tmp.sort()
    for m in tmp:
        try:
            media.append(Media(m, plist_config.options))
        except FileNotFoundError:
            # File removed between globbing and creation
            pass
    return media

def sched_event_handler(date: datetime, value: str, cookie: tuple):
    LOGGER.debug("Scheduling event fired")
    mplayer, playlist_files = cookie
    plist_file = playlist_files[value]
    media = playlist_config_to_media_list(plist_file)
    mplayer.playlist().clear()
    mplayer.playlist().extend(media)
    LOGGER.debug("Scheduling event handled")

def event_loop(mplayer: MediaPlayer):
    sched_conf, playlists = config.load_configs(r"G:\googledrive\Skriinille")
    s = Scheduler(
        sched_conf.default,
        sched_conf.schedule(),
        sched_event_handler,
        (mplayer, playlists)
    )

    media = playlist_config_to_media_list(playlists[s.current_value()])
    mplayer.playlist().extend(media)
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
