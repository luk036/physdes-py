from physdes.generic import min_dist, overlap
from physdes.recti import interval, point, rectangle
from physdes.vector2 import vector2


def test_Point_3D():
    a = point(point(40000, 80000), 20000)
    b = point(point(50000, 60000), 10000)
    v = (b - a) * 0.5  # integer division

    assert a < b
    assert a <= b
    assert not (a == b)
    assert a != b
    assert b > a
    assert b >= a
    assert (a + v) + v == b  # may not true due to integer division
    assert (a - v) + v == a

    # assert a.flip_xy().flip_xy() == a
    # assert a.flip_y().flip_y() == a


def test_Interval_3D():
    a = point(interval(4, 8), 1)
    b = point(interval(5, 6), 1)
    v = vector2(3, 0)

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
    assert a.intersection_with(b) == b
    assert not b.contains(a)
    assert a.overlaps(b)
    assert b.overlaps(a)

    assert min_dist(a, b) == 0


def test_Rectangle_3D():
    xrng1 = interval(40000, 80000)
    yrng1 = interval(50000, 70000)
    r1 = point(rectangle(xrng1, yrng1), 1000)
    xrng2 = interval(50000, 70000)
    yrng2 = interval(60000, 60000)
    r2 = point(rectangle(xrng2, yrng2), 1000)
    v = vector2(vector2(50000, 60000), 0)
    p1 = point(point(70000, 60000), 1000)
    p2 = point(point(70000, 60000), 2000)

    assert r1 != r2
    assert (r1 - v) + v == r1

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
#     xrng1 = interval(4, 8)
#     yrng1 = interval(5, 7)
#     s1 = hsegment(xrng1, 6)
#     s2 = vsegment(5, yrng1)

#     assert s1.overlaps(s2))
