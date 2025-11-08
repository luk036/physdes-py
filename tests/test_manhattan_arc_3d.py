import pytest
from physdes.manhattan_arc_3d import ManhattanArc3D
from physdes.point import Point
from physdes.manhattan_arc import ManhattanArc
from icecream import ic


def test_from_point():
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    assert ma.ma1 == ManhattanArc.from_point(Point(1, 3))
    assert ma.ma2 == ManhattanArc.from_point(Point(3, 2))
    assert ma.ma3 == ManhattanArc.from_point(Point(1, 2))


def test_eq():
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(1, 2), 3)
    ma2 = ManhattanArc3D.from_point(p2)
    p3 = Point(Point(4, 5), 6)
    ma3 = ManhattanArc3D.from_point(p3)
    assert ma1 == ma2
    assert ma1 != ma3


def test_min_dist_with():
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(4, 5), 6)
    ma2 = ManhattanArc3D.from_point(p2)
    assert ma1.min_dist_with(ma2) == 9


def test_enlarge_with():
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    enlarged_ma = ma.enlarge_with(2)
    assert enlarged_ma.ma1 == ma.ma1.enlarge_with(2)
    assert enlarged_ma.ma2 == ma.ma2.enlarge_with(2)
    assert enlarged_ma.ma3 == ma.ma3.enlarge_with(2)


def test_intersect_with():
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    intersection = ma1.intersect_with(ma1)
    assert intersection == ma1


def test_intersect_with_different_points():
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(4, 5), 6)
    ma2 = ManhattanArc3D.from_point(p2)
    with pytest.raises(AssertionError):
        ma1.intersect_with(ma2)


def test_get_center():
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    center = ma.get_center()
    assert center.xcoord.xcoord == 1
    assert center.xcoord.ycoord == 2
    assert center.ycoord == 3


def test_get_lower_corner():
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    lower_corner = ma.get_lower_corner()
    assert lower_corner.xcoord.xcoord == 1
    assert lower_corner.xcoord.ycoord == 2
    assert lower_corner.ycoord == 3


def test_get_upper_corner():
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    upper_corner = ma.get_upper_corner()
    assert upper_corner.xcoord.xcoord == 1
    assert upper_corner.xcoord.ycoord == 2
    assert upper_corner.ycoord == 3
