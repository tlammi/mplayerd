from media import MediaPlayer, Media
from scheduler import Scheduler
import iterators
import time
import sys
import threading
import glob
from datetime import datetime, timedelta
import config
import filters


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
"""
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