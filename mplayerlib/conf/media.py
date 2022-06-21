
from datetime import datetime
from typing import Union, List
from ..timeutil import Date, to_datetime


class Media(dict):
    def __init__(self, media: str,
                 after: Date = datetime.fromtimestamp(0),
                 before: Date = datetime.max):
        """
        Media entry in playlist

        :param media: (Absolute) path to media file
        :param after: Media is active after this time
        :param before: Media is active before this time
        """
        super().__init__(media=media, after=to_datetime(after), before=to_datetime(before))

    @property
    def media(self):
        return self["media"]

    @property
    def after(self):
        return self["after"]

    @property
    def before(self):
        return self["before"]

    def active(self, clock=datetime.now):
        """
        True if the current time is between after and before
        :param clock:
        :return:
        """
        t = clock()
        return self.after < t <= self.before
