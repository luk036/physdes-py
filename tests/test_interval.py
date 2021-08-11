from physdes.recti import interval
from physdes.generic import min_dist
#include <recti/halton_int.hpp>


def test_interval():
    a = interval(4, 8)
    b = interval(5, 6)
    v = 3;

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
    a = interval(interval(3, 4), interval(8, 9))
    b = interval(interval(5, 6), interval(6, 7))
    v = 3;

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

    assert a.contains(interval(4, 5))
    assert a.contains(interval(7, 8))
    assert a.overlaps(interval(7, 8))

    # print(max(interval(3, 4), 7))
    # print(min(interval(8, 9), 8))
    # print(a.intersection_with(interval(7, 8)))

    # The following depends on how max() and min() are implemented!!!!
    assert a.intersection_with(interval(7, 8)) == interval(7, interval(8, 9))

    assert a.contains(b)
    assert a.intersection_with(b) == b
    assert not b.contains(a)
    assert a.overlaps(b)
    assert b.overlaps(a)
    assert min_dist(a, b) == 0

