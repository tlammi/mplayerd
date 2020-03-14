import pytest
from mplayerd.iterators import *


@pytest.mark.parametrize("itertype", [
    LoopIterator,
    FairRndIterator
])
def test_simple(itertype):
    it = itertype.from_list([i for i in range(1000)])
    for i in range(10000):
        try:
            next(it)
        except StopIteration:
            pass


@pytest.mark.parametrize("itertype", [
    LoopIterator, FairRndIterator
])
def test_two(itertype):
    it = itertype.from_list([1, 2])
    for i in range(100):
        try:
            next(it)
        except StopIteration:
            pass


@pytest.mark.parametrize("itertype", [
    LoopIterator, FairRndIterator
])
def test_one(itertype):
    it = itertype.from_list([1])
    for i in range(100):
        try:
            next(it)
        except StopIteration:
            pass

@pytest.mark.parametrize("itertype", [
    LoopIterator, FairRndIterator
])
def test_zero(itertype):
    it = itertype.from_list([])
    for i in range(1000):
        try:
            next(it)
        except StopIteration:
            pass
