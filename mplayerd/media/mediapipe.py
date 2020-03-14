import abc
from .playlist import Playlist


class MediaPipe(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_playlist(cls, playlist: list):
        pass

    def __iter__(self):
        return self

    @abc.abstractmethod
    def __next__(self):
        pass


class LoopMediaPipe(MediaPipe):

    def __init__(self, playlist: Playlist):
        self._plist = playlist
        self._index = 0

    @classmethod
    def from_playlist(cls, playlist: Playlist):
        return cls(playlist)

    def __next__(self):
        if len(self._plist) == 0:
            raise StopIteration()

        res = self._plist[self._index]
        self._index = (self._index + 1) % len(self._plist)
        return res
