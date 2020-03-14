from . import iteratorbase


class LoopIterator(iteratorbase.IteratorBase):

    def __init__(self, playlist: list):
        self._plist = playlist
        self._index = 0

    @classmethod
    def from_list(cls, playlist: list):
        return cls(playlist)

    def __next__(self):
        if len(self._plist) == 0:
            raise StopIteration()

        res = self._plist[self._index]
        self._index = (self._index + 1) % len(self._plist)
        return res


