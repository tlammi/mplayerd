import logging
import sys
import argparse
import tkinter
import os

import mplayerlib
import mplayer


LOGGER = logging.getLogger("")


def parse_cli():
    p = argparse.ArgumentParser("mplayerd", description="Daemon for playing media")
    players = mplayerlib.media.supported_players()
    default_workspace = "/tmp/mplayerd-workspace"
    p.add_argument("-f,", "--frontend",
                   help=f"Frontend(s) to use: {players}. Default: ['dump']", action="append")
    p.add_argument("-w", "--workspace",
                   help=f"Set workspace path. Default {default_workspace}", default=default_workspace)
    p.add_argument("-r", "--reload", help="Config reload interval in seconds. Default: 120", type=int, default=120)
    p.add_argument("source",
                   help="Path to configuration where to start.")
    p.add_argument("--debug", action="store_true")
    ns = p.parse_args(sys.argv[1:])
    if not ns.frontend:
        ns.frontend = ["dump"]
    return ns


def main():
    args = parse_cli()
    level = logging.DEBUG if args.debug else logging.INFO
    mplayerlib.log.init(os.path.dirname(args.source), level)
    LOGGER.info("Initializing mplayerd library")
    root = tkinter.Tk()
    settings = mplayer.Settings(root, args.source, args.workspace, args.frontend, args.reload)
    LOGGER.info("Library created. Initializing application logic")
    player = mplayer.MPlayer(settings)
    LOGGER.info("Application logic initialized. Entering main event loop.")
    try:
        root.mainloop()
    except KeyboardInterrupt:
        LOGGER.info("Got keyboard interrupt. Terminating...")
        root.destroy()
    LOGGER.info("Exited event loop. Terminating application logic.")
    player.terminate()
    LOGGER.info("Gracefully terminated application. Exiting.")


if __name__ == "__main__":
    main()
