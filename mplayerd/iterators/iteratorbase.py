import abc


class IteratorBase(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_list(cls, playlist: list):
        pass

    def __iter__(self):
        return self

    @abc.abstractmethod
    def __next__(self):
        pass
