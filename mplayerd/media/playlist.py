import threading
import abc
import random

from . import media

class IteratorBase(abc.ABC):

    def __init__(self, wrapped_list: list, mutex: threading.Lock):
        self._list = wrapped_list
        self._mut = mutex

    def __iter__(self):
        return self
    
    def __next__(self):
        with self._mut:
            return self._list[self._index(len(self._list))]

    @abc.abstractmethod
    def _index(self, elem_count: int):
        pass

class Iterator(IteratorBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._i = 0

    def _index(self, elem_count: int):
        if self._i < elem_count:
            ret, self._i = self._i, self._i + 1
            return ret
        self._i = 0
        raise StopIteration()

class InfIterator(IteratorBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._i = 0
    
    def _index(self, elem_count: int):
        if elem_count == 0:
            raise StopIteration()
        ret, self._i = self._i, (self._i + 1) % elem_count
        return ret

class RndIterator(IteratorBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._indexes = []
        self._i = 0
    
    def _index(self, elem_count: int):
        if not self._indexes:
            self._indexes = [i for i in range(elem_count)]
            random.shuffle(self._indexes)
    
        if self._i < elem_count:
            ret, self._i = self._indexes[self._i], self._i + 1
            return ret

        self._i = 0
        raise StopIteration()

class InfRndIterator(IteratorBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._indexes = []
        self._i = 0

    def _index(self, elem_count: int):
        if not self._indexes:
            self._indexes = [i for i in range(elem_count)]
            random.shuffle(self._indexes)

        if elem_count == 0:
            raise StopIteration()
        ret, self._i = self._indexes[self._i], (self._i + 1) % elem_count
        return ret


class Playlist:

    def __init__(self, initial_list: list = None):
        self._list = initial_list or []
        self._mut = threading.Lock()
    
    def append(self, val: media.Media):
        with self._mut:
            self._list.append(val)
    
    def clear(self):
        with self._mut:
            self._list.clear()

    def extend(self, other):
        if isinstance(other, list):
            with self._mut:
                self._list.extend(other)
        elif isinstance(other, Playlist):
            with self._mut:
                with other._mut:
                    self._list.extend(other._list)
        else:
            raise TypeError()

    def iter(self):
        return Iterator(self._list, self._mut)
    
    def inf_iter(self):
        return InfIterator(self._list, self._mut)

    def rnd_iter(self):
        return RndIterator(self._list, self._mut)
    
    def inf_rnd_iter(self):
        return InfRndIterator(self._list, self._mut)

    def __getitem__(self, item):
        with self._mut:
            return self._list[item]
    
    def __setitem__(self, index, value: media.Media):
        with self._mut:
            self._list[index] = value
    
    def __add__(self, other):
        if isinstance(other, list):
            with self._mut:
                tmp = self._list + other
        elif isinstance(other, Playlist):
            with self._mut:
                with other._mut:
                    tmp = self._list + other._list
        else:
            raise TypeError()
        ret = Playlist()
        ret._list = tmp
        return ret

    def __len__(self):
        with self._mut:
            return len(self._list)
    