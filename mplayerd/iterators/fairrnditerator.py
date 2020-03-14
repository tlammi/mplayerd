import random
from collections import deque
from dataclasses import dataclass
from . import iteratorbase


class FairRndIterator(iteratorbase.IteratorBase):

    @dataclass
    class WrappedItem:
        item: str
        showings: int

    def __init__(self, playlist: list):
        random.shuffle(playlist)
        half = len(playlist) // 2
        tmp = [FairRndIterator.WrappedItem(i, 1) for i in playlist]
        self._top_bin = tmp[half:]
        self._bottom_bin = deque(tmp[:half])
        self._indexes = [i for i, _ in enumerate(self._top_bin)]

    @classmethod
    def from_list(cls, playlist: list):
        return cls(playlist)

    def __next__(self):
        if len(self._top_bin) == 0:
            raise StopIteration()

        max_shows = max([i.showings for i in self._top_bin])
        weights = [max_shows - i.showings + 1 for i in self._top_bin]
        index = random.choices(self._indexes, weights)[0]
        self._top_bin[index].showings += 1
        rnd_elem = self._top_bin[index]
        if len(self._bottom_bin) > 0:
            self._top_bin[index] = self._bottom_bin.popleft()
            self._bottom_bin.append(rnd_elem)

        return rnd_elem.item
