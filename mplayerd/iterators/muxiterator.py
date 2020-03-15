from . import iteratorbase, loopiterator, fairrnditerator


class MuxIterator(iteratorbase.IteratorBase):

    _ITER_MAPPING = {
        "FairRnd": fairrnditerator.FairRndIterator,
        "Loop": loopiterator.LoopIterator
    }

    def __init__(self, iterator_names: list, playlists: list):

        self._iterators = []
        for iter_name, plist in zip(iterator_names, playlists):
            self._iterators.append(iter(self._ITER_MAPPING[iter_name](plist)))
        self._index = 0

    @classmethod
    def from_list(cls, playlist: list):
        pass

    def __next__(self):
        val = next(self._iterators[self._index])
        self._index = (self._index + 1) % len(self._iterators)
        return val
