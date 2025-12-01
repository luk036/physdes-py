from physdes.interval import Interval
from physdes.point import Point
from physdes.vector2 import Vector2


def test_init_and_str() -> None:
    a = Point(3, 4)
    assert str(a) == "(3, 4)"
    a3d = Point(a, 5)
    assert str(a3d) == "((3, 4), 5)"


def test_nearest_to() -> None:
    a = Point(3, 4)
    b = Point(5, 6)
    assert a.nearest_to(b) == Point(3, 4)

    r = Point(Interval(3, 4), Interval(5, 6))  # Rectangle
    assert r.nearest_to(a) == Point(3, 5)
    assert r.nearest_to(b) == Point(4, 6)


def test_comparison_3d() -> None:
    a = Point(3, 4)
    b = Point(5, 6)
    a3d = Point(a, 5)
    b3d = Point(b, 1)
    assert not (a3d > b3d)
    assert not (b3d < a3d)  # This was the failing line
    assert a3d != b3d


def test_arithmetic_3d() -> None:
    a = Point(3, 4)
    v = Vector2(5, 6)
    a3d = Point(a, 5)
    v3d = Vector2(v, 1)
    res_add = a3d + v3d
    assert res_add.xcoord.xcoord == 8
    assert res_add.xcoord.ycoord == 10
    assert res_add.ycoord == 6

    res_sub = a3d - v3d
    assert res_sub.xcoord.xcoord == -2
    assert res_sub.xcoord.ycoord == -2
    assert res_sub.ycoord == 4


def test_flip_interval() -> None:
    r = Point(Interval(3, 4), Interval(5, 6))  # Rectangle
    flipped_r = r.flip()
    assert flipped_r.xcoord.lb == 5
    assert flipped_r.xcoord.ub == 6
    assert flipped_r.ycoord.lb == 3
    assert flipped_r.ycoord.ub == 4


def test_hull_with_interval() -> None:
    r1 = Point(Interval(3, 4), Interval(5, 6))
    r2 = Point(Interval(1, 2), Interval(7, 8))
    hull = r1.hull_with(r2)
    assert hull.xcoord.lb == 1
    assert hull.xcoord.ub == 4
    assert hull.ycoord.lb == 5
    assert hull.ycoord.ub == 8


def test_intersect_with_interval() -> None:
    r1 = Point(Interval(3, 5), Interval(3, 5))
    r2 = Point(Interval(4, 6), Interval(4, 6))
    intersection = r1.intersect_with(r2)
    assert intersection.xcoord.lb == 4
    assert intersection.xcoord.ub == 5
    assert intersection.ycoord.lb == 4
    assert intersection.ycoord.ub == 5


def test_min_dist_with_interval() -> None:
    r = Point(Interval(3, 4), Interval(5, 6))
    a = Point(1, 1)
    assert r.min_dist_with(a) == 6  # (3-1) + (5-1) = 2 + 4 = 6
