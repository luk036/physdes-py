from physdes.interval import Interval
from physdes.point import Point
from physdes.vector2 import Vector2


def test_point():
    a = Point(4, 8)
    b = Point(5, 6)
    assert a < b
    assert a <= b
    assert not (b == a)
    assert b != a


def test_point2():
    a = Point(3, 4)
    r = Point(Interval(3, 4), Interval(5, 6))  # Rectangle
    assert not r.contains(a)
    assert r.contains(Point(4, 5))
    assert not r.overlaps(a)
    assert r.overlaps(Point(4, 5))
    assert r.overlaps(Point(4, 6))
    assert r.intersect_with(Point(4, 5)) == Point(Interval(4, 4), Interval(5, 5))


def test_transform():
    a = Point(3, 5)
    b = Vector2(5, 7)
    assert a + b == Point(8, 12)
    assert a - b == Point(-2, -2)
    assert a.flip() == Point(5, 3)

    a += b
    assert a == Point(8, 12)
    a -= b
    assert a == Point(3, 5)


def test_displacement():
    a = Point(3, 5)
    b = Point(5, 7)
    c = Point(7, 8)
    assert a.displace(b) == Vector2(-2, -2)
    assert a.displace(c) == Vector2(-4, -3)
    assert b.displace(c) == Vector2(-2, -1)


def test_enlarge():
    a = Point(3, 5)
    assert a.enlarge_with(2) == Point(Interval(1, 5), Interval(3, 7))


def test_hull():
    a = Point(3, 5)
    b = Point(5, 7)
    assert a.hull_with(b) == Point(Interval(3, 5), Interval(5, 7))


def test_min_dist():
    a = Point(3, 5)
    b = Point(5, 7)
    assert a.min_dist_with(b) == 4


def test_repr():
    a = Point(3, 5)
    assert repr(a) == "Point(3, 5)"


def test_lt():
    a = Point(3, 5)
    b = Point(5, 7)
    c = Point(3, 7)
    assert (a < b) is True
    assert (a < c) is True
    assert (b < a) is False
    assert (c < a) is False
