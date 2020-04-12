
import iterators
import time
import sys
import threading
import glob
import enum
import os
import logging
import config

from datetime import datetime, timedelta
from media import MediaPlayer, Media
from scheduler import Scheduler

LOGGER = logging.getLogger(__name__)

def address_sanity_issues(sanity: config.SanityIssue, schedules: list, playlists: list):
    if sanity == 0:
        LOGGER.info("No sanity issues found in configuration")
        return schedules, playlists

    LOGGER.info("Addressing configuration sanity issues")
    if sanity & config.SanityIssue.TooManySchedFiles:
        LOGGER.warning("Too many schedule files. Ignoring all except %s", schedules[0])
        schedules = schedules[:1]
    if sanity & config.SanityIssue.NoSchedFile:
        raise OSError("No schedule file found. Running without one is not yet supported")
    if sanity & config.SanityIssue.NonExistingPlaylistInSchedule:
        raise OSError("Non-existing playlist reference found in schedule. Terminating..")
    LOGGER.info("Sanity issues addressed")
    return schedules, playlists

def load_playlists(playlist_files: list):
    LOGGER.info("Loading playlists")
    plists = []
    for p in playlist_files:
        LOGGER.debug("Loading %s", p)
        plists.append(config.load_playlist(p))
    return plists


def load_configs(search_path: str):
    schedule_files, playlist_files = config.search_configs(search_path)
    sanity = config.sanity_check_configs(schedule_files, playlist_files)
    schedules, playlist_files = address_sanity_issues(sanity, schedule_files, playlist_files)
    plist_metas = load_playlists(playlist_files)

    playlist_to_meta_mapping = dict(zip([os.path.basename(f) for f in playlist_files], plist_metas))
    LOGGER.info("Loading schedule")
    default_playlist_file, schedule = config.load_schedule(schedule_files[0])
    LOGGER.info("Schedule loaded")
    return playlist_to_meta_mapping, default_playlist_file, schedule
    

def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    playlist_to_meta_mapping, default_playlist_file, schedule = load_configs(r"G:\googledrive\Skriinille")

    mplayer = MediaPlayer([])

    def cb(date_instance, value):
        meta = playlist_to_meta_mapping[value]
        media_objs = [Media(f, meta.options) for f in meta.media]
        mplayer.playlist_replace(media_objs)

    s = Scheduler(default_playlist_file, schedule, cb)

    meta = playlist_to_meta_mapping[s.current_value()]

    media_objs = [Media(f, meta.options) for f  in meta.media]
    mplayer.playlist_replace(media_objs)
    mplayer.run_forever()


main()

"""
def build_media_iterator(conf: config.Config):
    iter_mapping = {
        "Mux": iterators.MuxIterator,
        "FairRnd": iterators.FairRndIterator,
        "Loop": iterators.LoopIterator
    }
    algorithm = conf.playlist_config("mainokset")["algorithm"]
    itertype = iter_mapping[algorithm]
    media_set_name = conf.playlist_config("mainokset")["media-sets"][0]
    media_set = conf.media_set(media_set_name)

    files = glob.glob(media_set["glob"], recursive=True)
    return itertype.from_list(files)



def main():
    conf = config.Config("mplayerd\\config.json")
    schedule = conf.schedule()
    print(schedule)
    iterator = build_media_iterator(conf)
    print(iterator)
    sys.exit(0)

main()
bands = glob.glob(conf.media_sets()["bandit"]["glob"], recursive=True)
print(f"before filter: {bands}")
START = datetime(2019, 6, 20, 17, 0)
END = START + timedelta(hours=5)
bands = filters.date_filter(bands, START, END)
print(f"after filter: {bands}")

FILES = [Media(band, {"image-duration": "15.0"}) for band in bands]

MediaPlayer(FILES).run_forever()

def f(d, arg):
    print(f"d: {d}, arg: {arg}")


EVENT_START_DATE = datetime(2020, 6, 17)

schedule = {
    datetime.now() - timedelta(hours=3): "0",
    datetime.now() - timedelta(seconds=1): "asdf",
    datetime.now() + timedelta(seconds=10): "10sec",
    datetime.now() + timedelta(seconds=20): "20sec"
}

s = Scheduler(f, schedule)

s.start()
"""


"""
FILES = glob.glob(r"G:\googledrive\Skriinille\**", recursive=True)

FILES = [f for f in FILES if f.endswith(".jpg")]
FILES = [Media(f, {"image-duration": "2.0"}) for f in FILES]
print("\n".join([f.file for f in FILES]))

player = MediaPlayer(FILES)

player.run_forever()
"""