
from .uri import parse


def test_parse_normal():
    test_set = [
        ("http://foo.bar", "http", "foo.bar"),
        ("file://./bar/baz.txt", "file", "./bar/baz.txt")
    ]

    for uri_str, scheme, resource in test_set:
        s, r = parse(uri_str)
        assert(s == scheme)
        assert(r == resource)
