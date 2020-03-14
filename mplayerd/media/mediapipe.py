import abc
import random
from collections import deque
from dataclasses import dataclass
import math

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

    def __init__(self, playlist: list):
        self._plist = playlist
        self._index = 0

    @classmethod
    def from_playlist(cls, playlist: list):
        return cls(playlist)

    def __next__(self):
        if len(self._plist) == 0:
            raise StopIteration()

        res = self._plist[self._index]
        self._index = (self._index + 1) % len(self._plist)
        return res


class FairRndMediaPipe(MediaPipe):

    @dataclass
    class MediaItem:
        media: str
        showings: int

    def __init__(self, playlist: list):
        random.shuffle(playlist)
        half = len(playlist) // 2
        tmp = [FairRndMediaPipe.MediaItem(i, 1) for i in playlist]
        self._top_bin = tmp[half:]
        self._bottom_bin = deque(tmp[:half])
        self._indexes = [i for i, _ in enumerate(self._top_bin)]

    @classmethod
    def from_playlist(cls, playlist: list):
        return cls(playlist)

    def __next__(self):
        max_shows = max([i.showings for i in self._top_bin])
        weights = [max_shows - i.showings + 1 for i in self._top_bin]
        index = random.choices(self._indexes, weights)[0]
        self._top_bin[index].showings += 1
        rnd_elem = self._top_bin[index]

        self._top_bin[index] = self._bottom_bin.popleft()
        self._bottom_bin.append(rnd_elem)

        return rnd_elem.media
