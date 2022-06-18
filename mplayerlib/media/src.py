
import abc


class Src(abc.ABC):
    """
    Object acting as a media source

    A generic object which produces sources for consumption elsewhere
    """

    @abc.abstractmethod
    def next(self) -> str:
        """
        Get next data

        :return: Path to the next media to play
        :raise: StopIteration on end of media
        """

    @abc.abstractmethod
    def __bool__(self) -> bool:
        """
        :return: True if not empty or False
        """