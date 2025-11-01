import pytest
from hypothesis import given
from hypothesis.strategies import integers

from physdes.generic import contain, displacement, intersection, min_dist, overlap
from physdes.interval import Interval, enlarge, hull


@given(
    integers(min_value=-1000, max_value=1000), integers(min_value=-1000, max_value=1000)
)
def test_interval_hypo(a1: int, a2: int):
    a = Interval(min(a1, a2), max(a1, a2))
    assert a.lb <= a.ub


def test_interval_arithmetic_hypo():
    @given(
        integers(min_value=-1000, max_value=1000),
        integers(min_value=0, max_value=1000),
        integers(min_value=-1000, max_value=1000),
    )
    def test_add_sub(a1, a2, v):
        a = Interval(min(a1, a2), max(a1, a2))
        assert (a + v) - v == a

    test_add_sub()


def test_interval():
    a = Interval(4, 8)
    b = Interval(5, 6)

    assert not (a < b)
    assert not (b < a)
    assert not (a > b)
    assert not (b > a)
    assert a <= b
    assert b <= a
    assert a >= b
    assert b >= a

    assert not (b == a)
    assert b != a

    assert a.contains(4)
    assert a.contains(8)
    assert a.intersect_with(8) == Interval(8, 8)
    assert a.contains(b)
    assert a.intersect_with(b) == b
    assert not b.contains(a)
    assert a.overlaps(b)
    assert b.overlaps(a)
    assert min_dist(a, b) == 0


@pytest.mark.parametrize(
    ("interval", "op", "value", "expected"),
    [
        (Interval(3, 5), "+", 1, Interval(4, 6)),
        (Interval(3, 5), "-", 1, Interval(2, 4)),
        (Interval(3, 5), "*", 2, Interval(6, 10)),
        (Interval(3, 5), "neg", None, Interval(-5, -3)),
        (Interval(3, 5), "+=", 1, Interval(4, 6)),
        (Interval(4, 6), "-=", 1, Interval(3, 5)),
        (Interval(3, 5), "*=", 2, Interval(6, 10)),
    ],
)
def test_arithmetic(interval, op, value, expected):
    if op == "+":
        assert interval + value == expected
    elif op == "-":
        assert interval - value == expected
    elif op == "*":
        assert interval * value == expected
    elif op == "neg":
        assert -interval == expected
    elif op == "+=":
        interval += value
        assert interval == expected
    elif op == "-=":
        interval -= value
        assert interval == expected
    elif op == "*=":
        interval *= value
        assert interval == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), True),
        (Interval(5, 7), Interval(7, 8), True),
        (Interval(3, 5), Interval(7, 8), False),
        (Interval(7, 8), Interval(3, 5), False),
        (Interval(3, 5), 4, True),
        (Interval(3, 5), 6, False),
        (4, Interval(3, 5), True),
        (6, Interval(3, 5), False),
        (4, 4, True),
    ],
)
def test_overlap(a, b, expected):
    assert overlap(a, b) is expected
    if isinstance(a, Interval):
        assert a.overlaps(b) is expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), False),
        (Interval(5, 7), Interval(7, 8), False),
        (Interval(3, 5), Interval(7, 8), False),
        (Interval(7, 8), Interval(3, 5), False),
        (Interval(3, 5), 4, True),
        (Interval(3, 5), 6, False),
        (4, Interval(3, 5), False),
        (4, 4, True),
    ],
)
def test_contains(a, b, expected):
    assert contain(a, b) is expected
    if isinstance(a, Interval):
        assert a.contains(b) is expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), Interval(5, 5)),
        (Interval(5, 7), Interval(7, 8), Interval(7, 7)),
        (Interval(3, 5), Interval(7, 8), None),
        (Interval(3, 5), 4, Interval(4, 4)),
        (Interval(3, 5), 6, None),
        (4, Interval(3, 5), Interval(4, 4)),
        (4, 4, 4),
    ],
)
def test_intersection(a, b, expected):
    if expected is not None:
        assert intersection(a, b) == expected
        if isinstance(a, Interval):
            assert a.intersect_with(b) == expected
    else:
        if isinstance(a, Interval):
            assert a.intersect_with(b).is_invalid()


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), Interval(3, 7)),
        (Interval(5, 7), Interval(7, 8), Interval(5, 8)),
        (Interval(3, 5), Interval(7, 8), Interval(3, 8)),
        (Interval(3, 5), 4, Interval(3, 5)),
        (Interval(3, 5), 6, Interval(3, 6)),
        (4, Interval(3, 5), Interval(3, 5)),
        (6, Interval(3, 5), Interval(3, 6)),
        (4, 6, Interval(4, 6)),
    ],
)
def test_hull(a, b, expected):
    assert hull(a, b) == expected
    if isinstance(a, Interval):
        assert a.hull_with(b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), 0),
        (Interval(3, 5), Interval(7, 8), 2),
        (Interval(5, 7), Interval(7, 8), 0),
        (Interval(3, 5), 4, 0),
        (4, Interval(3, 5), 0),
        (Interval(3, 5), 6, 1),
        (6, Interval(3, 5), 1),
    ],
)
def test_min_dist(a, b, expected):
    assert min_dist(a, b) == expected
    if isinstance(a, Interval):
        assert a.min_dist_with(b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), Interval(-2, -2)),
        (Interval(3, 5), Interval(7, 8), Interval(-4, -3)),
        (Interval(5, 7), Interval(7, 8), Interval(-2, -1)),
        (4, 4, 0),
        (4, 6, -2),
        (6, 4, 2),
    ],
)
def test_displacement(a, b, expected):
    assert displacement(a, b) == expected
    if isinstance(a, Interval):
        assert a.displace(b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), 2, Interval(1, 7)),
        (4, 6, Interval(-2, 10)),
        (6, 4, Interval(2, 10)),
    ],
)
def test_enlarge(a, b, expected):
    assert enlarge(a, b) == expected
    if isinstance(a, Interval):
        assert a.enlarge_with(b) == expected


# def test_interval_of_interval():
#     a = Interval(Interval(3, 4), Interval(8, 9))
#     b = Interval(Interval(5, 6), Interval(6, 7))
#     v = 3

#     assert not (a < b)
#     assert not (b < a)
#     assert not (a > b)
#     assert not (b > a)
#     assert a <= b
#     assert b <= a
#     assert a >= b
#     assert b >= a

#     assert not (b == a)
#     assert b != a

#     assert (a - v) + v == a

#     assert a.contains(Interval(4, 5))
#     assert a.contains(Interval(7, 8))
#     assert a.overlaps(Interval(7, 8))

#     # print(max(Interval(3, 4), 7))
#     # print(min(Interval(8, 9), 8))
#     # print(a.intersect_with(Interval(7, 8)))

#     # The following depends on how max() and min() are implemented!!!!
#     assert a.intersect_with(Interval(7, 8)) == Interval(7, Interval(8, 9))

#     assert a.contains(b)
#     assert a.intersect_with(b) == b
#     assert not b.contains(a)
#     assert a.overlaps(b)
#     assert b.overlaps(a)
#     assert min_dist(a, b) == 0
