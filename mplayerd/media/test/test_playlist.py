import pytest
import media

def test_ctor():
    p = media.Playlist([1,2,3,4,5])
    assert len(p) == 5
    p = media.Playlist()
    assert len(p) == 0
    p = media.Playlist([])
    assert len(p) == 0

def test_append():
    p = media.Playlist()
    p.append(1)
    p.append(2)
    assert len(p) == 2

def test_add():
    p = media.Playlist()
    assert isinstance(p + [1,2,3], media.Playlist)
    assert len(p) == 0
    p += [1,2,3,4]
    assert len(p) == 4

def test_clear():
    p = media.Playlist([1,2,3,4,5])
    p.clear()
    assert len(p) == 0

def test_len():
    p = media.Playlist()
    assert len(p) == 0
    p.append(1)
    assert len(p) == 1

def test_getitem():
    p = media.Playlist([1,2,3,4,5])
    assert p[0] == 1
    assert p[1] == 2
    assert p[4] == 5

def test_setitem():
    p = media.Playlist([1,2,3])
    assert p[0] == 1
    assert p[1] == 2
    p[0] = 100
    assert p[0] == 100
    assert p[1] == 2

def test_iter():
    p = media.Playlist([1,2,3,4])
    index = 0
    for i in p.iter():
        index += 1
    assert index == 4

    i = iter(p.iter())
    assert next(i) == 1
    assert next(i) == 2
    assert next(i) == 3
    assert next(i) == 4

    with pytest.raises(StopIteration):
        assert next(i)
    
    i = iter(p.iter())
    assert next(i) == 1
    assert next(i) == 2
    p.append(100)
    p.append(200)
    assert next(i) == 3
    assert next(i) == 4
    assert next(i) == 100
    assert next(i) == 200
    