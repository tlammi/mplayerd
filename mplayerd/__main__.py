from media import MediaPlayer, Media
from scheduler import Scheduler
import time
import threading
import glob
from datetime import datetime, timedelta


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
FILES = glob.glob(r"G:\googledrive\Skriinille\**", recursive=True)

FILES = [f for f in FILES if f.endswith(".jpg")]
FILES = [Media(f, {"image-duration": "2.0"}) for f in FILES]
print("\n".join([f.file for f in FILES]))

player = MediaPlayer(FILES)

player.run_forever()
"""