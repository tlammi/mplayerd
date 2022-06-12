
import pytest

from .conf import Conf


def test_minimal():
    Conf({
        "version": 0,
        "config": {},
        "playlists": {}
    }, ".", "dummy")


def test_wrong_version():
    with pytest.raises(Exception):
        Conf({
            "version": 69,
            "config": {},
            "playlists": {}
        }, ".", "dummy")
