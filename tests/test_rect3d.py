from hypothesis import given
from hypothesis.strategies import integers

from physdes.generic import overlap
from physdes.interval import Interval, min_dist
from physdes.recti import Point, Rectangle
from physdes.vector2 import Vector2


@given(integers(), integers(), integers(), integers(), integers(), integers())
def test_Point_hypo(a1, a2, b1, b2, v1, v2):
    a = Point(a1, a2)
    b = Point(b1, b2)
    v = Vector2(v1, v2)
    assert (a - v) + v == a
    assert (b - v) + v == b


def test_Point_3D():
    a = Point(Point(40000, 8), 20000)
    b = Point(Point(50000, 6), 10000)
    # v = b.displace(a) * 0.5  # integer division

    assert a < b
    assert a <= b
    assert not (a == b)
    assert a != b
    assert b > a
    assert b >= a
    # assert (a + v) + v == b  # may not true due to integer division
    # assert (a - v) + v == a

    # assert a.flip_xy().flip_xy() == a
    # assert a.flip_y().flip_y() == a


def test_Interval_3D():
    a = Point(Interval(4, 8), 1)
    b = Point(Interval(5, 6), 1)
    v = Vector2(3, 0)

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

    assert a.contains(b)
    assert a.intersect_with(b) == b
    assert not b.contains(a)
    assert a.overlaps(b)
    assert b.overlaps(a)

    assert min_dist(a, b) == 0


def test_Rectangle_3D():
    xrng1 = Interval(40000, 80000)
    yrng1 = Interval(50000, 70000)
    r1 = Point(Rectangle(xrng1, yrng1), 1000)
    xrng2 = Interval(50000, 70000)
    yrng2 = Interval(60000, 60000)
    r2 = Point(Rectangle(xrng2, yrng2), 1000)
    # v = Vector2(Vector2(50000, 60000), 0)
    p1 = Point(Point(70000, 60000), 1000)
    p2 = Point(Point(70000, 60000), 2000)

    assert r1 != r2
    # assert (r1 - v) + v == r1

    # assert r1 <= p
    assert r1.contains(p1)
    assert not r1.contains(p2)
    assert r1.contains(r2)
    assert r1.overlaps(r2)
    assert overlap(r1, r2)

    assert r1.min_dist_with(r2) == 0
    assert min_dist(r1, r2) == 0

    assert r1.min_dist_with(p2) == p2.min_dist_with(r1)
    # assert min_dist(r1, p2) == min_dist(p2, r1)


# def test_Segment():
#     xrng1 = Interval(4, 8)
#     yrng1 = Interval(5, 7)
#     s1 = HSegment(xrng1, 6)
#     s2 = VSegment(5, yrng1)

#     assert s1.overlaps(s2))
