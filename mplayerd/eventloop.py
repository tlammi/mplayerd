import datetime

import config

from media import Media, MediaPlayer
from scheduler import Scheduler

class EventLoop:
    
    def __init__(self, media_player: MediaPlayer, config_path: str):
        self._mplayer = media_player
        self._config_path = config_path
        self._sched_conf, self._plist_confs = config.load_configs(config_path)
        self._scheduler = Scheduler(
            self._sched_conf.default,
            self._sched_conf.schedule(),
            self._sched_event_handler
        )

        media = self._playlist_config_to_media_list(
           self._plist_confs[self._scheduler.current_value()]
        )
        self._mplayer.playlist().extend(media)
        self._mplayer.play()

    @staticmethod
    def _playlist_config_to_media_list(plist_config: config.PlaylistFile):
        media = []
        tmp = list(plist_config.media())
        tmp.sort()
        for m in tmp:
            try:
                media.append(Media(m, plist_config.options))
            except FileNotFoundError:
                # File removed between globbing and creation
                pass
        return media

    def _sched_event_handler(self, date: datetime, value: str, _):
        LOGGER.debug("Scheduling event fired")
        plist_file = self._plist_confs[value]
        media = playlist_config_to_media_list(plist_file)
        self._mplayer.playlist().replace(media)
        LOGGER.debug("Scheduling event handled")
