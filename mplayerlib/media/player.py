
import abc

from .src import Src


class Player(abc.ABC):

    @abc.abstractmethod
    def set_media_source(self, source: Src):
        """
        Set source for media

        Player uses this object to consume media.
        This method can be called during operation where
        the player should store the new media source and start
        consuming media from there when needed.

        :param source: Media source to use next
        """

    @abc.abstractmethod
    def play(self):
        """
        Start player operation asynchronously
        """

    @abc.abstractmethod
    def stop(self):
        """
        Stop operation
        """


