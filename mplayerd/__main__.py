
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
import eventloop

from datetime import datetime, timedelta
from media import MediaPlayer, Media
from scheduler import Scheduler


LOGGER = logging.getLogger()


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    mplayer = MediaPlayer()
    t = threading.Thread(
        target=eventloop.EventLoop,
        daemon=True,
        args=(mplayer, r"G:\googledrive\Skriinille")
    )
    t.start()
    mplayer.run_forever()
    t.join()

main()
