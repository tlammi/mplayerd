import os
from . import configfile


def load_configs(path: str):
    children = [os.path.join(path, f) for f in os.listdir(path)]
    files = [c for c in children if os.path.isfile(c)]
    sched_files = [
        configfile.ScheduleFile(f) for f in files if f.endswith(".schedule")
    ]
    assert len(sched_files) == 1
    playlist_paths = [
        configfile.PlaylistFile(f) for f in files if f.endswith(".playlist")
    ]
    playlist_files = {}
    for p in playlist_paths:
        playlist_files[p.basename] = p
    return sched_files[0], playlist_files