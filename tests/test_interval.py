from physdes.generic import min_dist
from physdes.recti import Interval

# include <recti/halton_int.hpp>


def test_interval():
    a = Interval(4, 8)
    b = Interval(5, 6)
    v = 3

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

    assert (a - v) + v == a

    assert a.contains(4)
    assert a.contains(8)
    assert a.intersection_with(8) == 8
    assert a.contains(b)
    assert a.intersection_with(b) == b
    assert not b.contains(a)
    assert a.overlaps(b)
    assert b.overlaps(a)
    assert min_dist(a, b) == 0


def test_interval_of_interval():
    a = Interval(Interval(3, 4), Interval(8, 9))
    b = Interval(Interval(5, 6), Interval(6, 7))
    v = 3

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

    assert (a - v) + v == a

    assert a.contains(Interval(4, 5))
    assert a.contains(Interval(7, 8))
    assert a.overlaps(Interval(7, 8))

    # print(max(Interval(3, 4), 7))
    # print(min(Interval(8, 9), 8))
    # print(a.intersection_with(Interval(7, 8)))

    # The following depends on how max() and min() are implemented!!!!
    assert a.intersection_with(Interval(7, 8)) == Interval(7, Interval(8, 9))

    assert a.contains(b)
    assert a.intersection_with(b) == b
    assert not b.contains(a)
    assert a.overlaps(b)
    assert b.overlaps(a)
    assert min_dist(a, b) == 0
