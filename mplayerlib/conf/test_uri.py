
from .uri import Uri


def test_parse_normal():
    test_set = [
        ("http://foo.bar", "http", "foo.bar"),
        ("file://./bar/baz.txt", "file", "./bar/baz.txt")
    ]

    for uri_str, scheme, resource in test_set:
        u = Uri.parse(uri_str)
        assert(u.scheme == scheme)
        assert(u.resource == resource)


def test_str():
    test_set = [
        "http://foo.bar",
        "https://asdf",
        "file:///home/user"
    ]
    for s in test_set:
        assert(s == str(Uri.parse(s)))


def test_parse_relative():
    test_set = [
        ("file://./subdir", "parent", "parent/subdir"),
        ("file://./../subdir", "parent", "subdir"),
    ]

    for uri_str, parent, expected in test_set:
        assert(Uri.parse(uri_str, parent).resource == expected)

