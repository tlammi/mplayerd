import sys
import argparse
import tkinter

import mplayerlib
import mplayer


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


def main():
    args = parse_cli()
    root = tkinter.Tk()
    settings = mplayer.Settings(root, args.source, args.workspace, args.frontend, args.reload)

    player = mplayer.MPlayer(settings)
    print("Starting main GUI loop")
    root.mainloop()
    player.terminate()


if __name__ == "__main__":
    main()
