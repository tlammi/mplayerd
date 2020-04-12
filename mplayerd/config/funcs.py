import json
import datetime
import glob
import pathlib
import os
import enum

from collections import namedtuple


PlaylistMeta = namedtuple("PlaylistMeta", "algorithm media options")


def load_playlist(playlist_file: str, datefunc=datetime.datetime.now, date_format="%Y-%m-%d %H:%M"):

    def do_add(basedir: str, globs: list):
        out = []
        for g in globs:
            g = os.path.join(basedir, g)
            out += glob.glob(g)
        return out

    def do_rm(list_to_filter: list, basedir: str, globs: list):
        out = []
        abs_globs = [os.path.join(basedir, g) for g in globs]
        for i in list_to_filter:
            if not any(pathlib.Path(i).match(g) for g in abs_globs):
                out.append(i)
        return out
    
    with open(playlist_file, "r") as f:
        data = json.load(f)
    basedir = os.path.dirname(playlist_file)
    algorithm = data["algorithm"]

    media = []

    media = do_add(basedir, data["media-base"])
    if "media-delta" in data:
        for time, value in data["media-delta"].items():
            time = datetime.datetime.strptime(time, date_format)
            if time < datefunc():
                for operation, globs in value.items():
                    if operation == "rm":
                        media = do_rm(media, basedir, globs)
                    elif operation == "add":
                        media += do_add(basedir, globs)
                    else:
                        raise ValueError(f"Invalid operation type {operation} in {playlist_file}")

    try:
        options = data["options"]
    except KeyError:
        options = {}

    return PlaylistMeta(algorithm, media, options)


def load_schedule(schedule_file: str, date_format="%Y-%m-%d %H:%M"):
    with open(schedule_file, "r") as f:
        data = json.load(f)
    
    out = {}
    default = None
    for time, value in data.items():
        if time == "default":
            default = value
        else:
            time = datetime.datetime.strptime(time, date_format)
            out[time] = value
    return default, out


def search_configs(search_dir: str):
    children = [os.path.join(search_dir, c) for c in os.listdir(search_dir)]
    files = [c for c in children if os.path.isfile(c)]
    sched_files = [f for f in files if f.endswith(".schedule")]
    plist_files = [f for f in files if f.endswith(".playlist")]
    return sched_files, plist_files


class SanityIssue(enum.IntFlag):
    TooManySchedFiles = 1 << 0
    NoSchedFile = 1 << 1
    NonExistingPlaylistInSchedule = 1 << 2


def sanity_check_configs(sched_paths: list, playlist_paths: list):
    flags = SanityIssue(0)
    if len(sched_paths) > 1:
        flags |= SanityIssue.TooManySchedFiles
    elif len(sched_paths) < 0:
        flags |= SanityIssue.NoSchedFile

    for path in sched_paths:
        with open(path, "r") as f:
            data = json.load(f)
        for value in data.values():
            if value not in [os.path.basename(plist_path) for plist_path in playlist_paths]:
                flags |= SanityIssue.NonExistingPlaylistInSchedule
                break

    return flags