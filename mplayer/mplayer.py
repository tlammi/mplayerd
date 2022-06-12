
import tkinter
import os

from dataclasses import dataclass

import mplayerlib
from .sched_worker import SchedWorker
from .timer import Timer


@dataclass
class Settings:

    tk: tkinter.Tk
    source_path: str
    work_path: str = "/tmp/mplayerd-workspace"
    # e.g. vlc, dump
    frontends: list = None

    # Reload interval in seconds
    reload_interval: int = 120


class MPlayer:
    """
    Entrypoint for the application

    """

    def __init__(self, settings: Settings):
        self._conf_path = settings.source_path
        self._ws = mplayerlib.Workspace(settings.work_path)
        self._conf = self._ws.load(self._conf_path)
        self._fronts = [mplayerlib.media.player(f, settings.tk) for f in settings.frontends]
        for f in self._fronts:
            f.play()
        self._sched = SchedWorker(self._conf, self._fronts)
        self._reloader = Timer(settings.reload_interval, self._handle_config_reload)

    def terminate(self):
        self._sched.terminate()
        self._reloader.cancel()

    def _handle_config_reload(self):
        print("Reloading configuration")
        new_conf = mplayerlib.conf.Conf.load(self._conf_path)
        if new_conf != self._conf:
            print("Configs changed. Refreshing...")
            self._conf = self._ws.load(self._conf_path)
            self._sched.update_conf(self._conf)
            print("Refreshed")
        else:
            print("Configs did not change. Doing nothing")
