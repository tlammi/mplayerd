import sys

import mplayerlib


def main():
    mplayerlib.conf.Conf.load(sys.argv[1])


if __name__ == "__main__":
    main()
