import pytest


def test_tuple_comprehension():
    """ Check tuple comprehension with generator """

    tup = tuple(i for i in range(3))
    expected = (0, 1, 2)

    assert tup == expected


@pytest.mark.skip()
def test_skip():
    pass


@pytest.mark.xfail()
def test_tuple_comprehension_failing():
    """ Failing test """

    tup = tuple(i for i in range(3))
    expected = (1, 2, 3)

    assert tup == expected


@pytest.mark.marker_test()
def test_marker1():
    pass


@pytest.mark.marker_test()
def test_marker2():
    pass


@pytest.mark.slow()
def test_slow():
    # slow test
    pass
