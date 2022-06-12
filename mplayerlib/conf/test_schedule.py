

from .schedule import Schedule


def test_eq():
    l = Schedule([[0, "foo"], [1, "bar"]])
    r = l
    assert(l == r)


def test_ne():
    s0 = Schedule([[0, "foo"], [1, "bar"]])
    s1 = Schedule([[0, "foo"], [1, "baz"]])
    s2 = Schedule([[0, "foo"], [3, "bar"]])
    assert(s0 != s1)
    assert(s0 != s2)
    assert(s1 != s2)
