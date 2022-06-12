import sys
import argparse
import copy
import time
import typing
import tkinter

import mplayerlib


def parse_cli():
    p = argparse.ArgumentParser("mplayerd", description="Daemon for playing media")
    players = mplayerlib.media.supported_players()
    p.add_argument("-f,", "--frontend",
                   help=f"Frontend(s) to use: {players}. Default: ['dump']", action="append")
    p.add_argument("source",
                   help="Path to configuration where to start.")
    ns = p.parse_args(sys.argv[1:])
    if not ns.frontend:
        ns.frontend = ["dump"]
    return ns


def main():
    args = parse_cli()
    conf = mplayerlib.conf.Conf.load(args.source)
    root = tkinter.Tk()
    frontends = [mplayerlib.media.player(f, root) for f in args.frontend]

    _sched = mplayerlib.sched.Scheduler(conf.schedule)

    for f in frontends:
        f.set_media_source(copy.deepcopy((conf.playlists[0])))
    for f in frontends:
        f.play()
    root.mainloop()
    for f in frontends:
        f.stop()


if __name__ == "__main__":
    main()
