import pytest
import os
from mplayerd.fs import JsonDict


def test_jsondict():
    thisdir = os.path.dirname(os.path.realpath(__file__))
    testjson = os.path.join(thisdir, "tmp.json")
    try:
        with JsonDict(testjson, True) as f:
            f["hello"] = 100
            f["world"] = 0.2

        with JsonDict(testjson, False) as f:
            assert "hello" in f
            assert "world" in f
            assert f["hello"] == 100
            assert f["world"] == 0.2
            f["asdf"] = "lorem ipsum"

        with JsonDict(testjson, True) as f:
            assert "asdf" not in f
    finally:
        try:
            os.remove(testjson)
        except Exception:
            pass
