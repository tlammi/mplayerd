import sys
import argparse
import os
import copy
import json
import threading
import time
import tkinter

from typing import List

import mplayerlib


class Shared:
    """
    Shared state share information between worker threads
    """

    def __init__(self, conf: mplayerlib.conf.Conf, frontends: List[mplayerlib.media.Player]):
        self._mut = threading.Lock()
        self._conf = conf
        self._fronts = frontends
        self._cv = threading.Condition()

    @property
    def condition(self):
        return self._cv

    @property
    def frontends(self):
        return self._fronts

    @property
    def conf(self):
        with self._mut:
            return self._conf

    @conf.setter
    def conf(self, c: mplayerlib.conf.Conf):
        with self._mut:
            self._conf = c


def parse_cli():
    p = argparse.ArgumentParser("mplayerd", description="Daemon for playing media")
    players = mplayerlib.media.supported_players()
    default_workspace = "/tmp/mplayerd-workspace"
    p.add_argument("-f,", "--frontend",
                   help=f"Frontend(s) to use: {players}. Default: ['dump']", action="append")
    p.add_argument("-w", "--workspace",
                   help=f"Set workspace path. Default {default_workspace}", default=default_workspace)
    p.add_argument("-r", "--reload", help="Config reload interval in seconds. Default: 120", default=120)
    p.add_argument("source",
                   help="Path to configuration where to start.")
    ns = p.parse_args(sys.argv[1:])
    if not ns.frontend:
        ns.frontend = ["dump"]
    return ns


def sched_worker(state: Shared):
    time.sleep(1)
    print("start working")
    print(state.conf.dump())
    sched = mplayerlib.sched.Scheduler(state.conf.schedule)
    print([i for i in sched.already_expired()])
    previous = sched.last_expired()
    for f in state.frontends:
        print("setting playlist")
        f.set_media_source(state.conf.playlists[previous])
    while True:
        dur, playlist = sched.next()
        with state.condition:
            notified = state.condition.wait(dur)
            if notified:
                break
            else:
                for f in state.frontends:
                    f.set_media_source(state.conf.playlists[playlist])


def reload_worker(interval: int, workspace: mplayerlib.Workspace, state: Shared):
    print(f"Starting reload worker with interval '{interval}'")
    while True:
        with state.condition:
            notified = state.condition.wait(interval)
            if notified:
                break
            else:
                print("Reloading configuration")
                path = os.path.join(state.conf.parent, state.conf.name)
                conf = workspace.load(path)
                print("Updating configuration")
                state.conf = conf


def main():
    args = parse_cli()
    conf = mplayerlib.conf.Conf.load(args.source)
    print(f"Parsed config: {json.dumps(conf.dump(), indent=4)}")
    ws = mplayerlib.Workspace(args.workspace)
    conf = ws.load(conf)
    print(f"Moved config: {json.dumps(conf.dump(), indent=4)}")
    root = tkinter.Tk()
    frontends = [mplayerlib.media.player(f, root) for f in args.frontend]
    state = Shared(conf, frontends)
    sched_worker_thread = threading.Thread(target=sched_worker, args=[state])
    sched_worker_thread.start()
    reload_worker_thread = threading.Thread(target=reload_worker, args=[args.reload, ws, state])
    reload_worker_thread.start()

    for f in frontends:
        f.play()
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    for f in frontends:
        f.stop()
    with state.condition:
        state.condition.notify_all()
    sched_worker_thread.join()
    reload_worker_thread.join()


if __name__ == "__main__":
    main()
