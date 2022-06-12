
import tkinter

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
        self._conf = mplayerlib.conf.Conf.load(settings.source_path)
        self._fronts = [mplayerlib.media.player(f, settings.tk) for f in settings.frontends]
        for f in self._fronts:
            f.play()
        self._sched = SchedWorker(self._conf, self._fronts)

        def on_reload(sched: SchedWorker, config: mplayerlib.conf.Conf):
            sched.update_conf(config)

        self._reloader = Timer(settings.reload_interval, on_reload, [self._sched, self._conf])

    def terminate(self):
        self._sched.terminate()
        self._reloader.cancel()
