import pytest

from physdes.manhattan_arc import ManhattanArc
from physdes.manhattan_arc_3d import ManhattanArc3D
from physdes.point import Point


def test_from_point() -> None:
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    assert ma.ma1 == ManhattanArc.from_point(Point(1, 3))
    assert ma.ma2 == ManhattanArc.from_point(Point(3, 2))
    assert ma.ma3 == ManhattanArc.from_point(Point(1, 2))


def test_eq() -> None:
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(1, 2), 3)
    ma2 = ManhattanArc3D.from_point(p2)
    p3 = Point(Point(4, 5), 6)
    ma3 = ManhattanArc3D.from_point(p3)
    assert ma1 == ma2
    assert ma1 != ma3


def test_eq_with_non_manhattan_arc_3d() -> None:
    """Test equality with non-ManhattanArc3D objects"""
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    assert ma != "not a ManhattanArc3D"
    assert ma != 123
    assert ma is not None


def test_min_dist_with() -> None:
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(4, 5), 6)
    ma2 = ManhattanArc3D.from_point(p2)
    assert ma1.min_dist_with(ma2) == 9


def test_enlarge_with() -> None:
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    enlarged_ma = ma.enlarge_with(2)
    assert enlarged_ma.ma1 == ma.ma1.enlarge_with(2)
    assert enlarged_ma.ma2 == ma.ma2.enlarge_with(2)
    assert enlarged_ma.ma3 == ma.ma3.enlarge_with(2)


def test_intersect_with() -> None:
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    intersection = ma1.intersect_with(ma1)
    assert intersection == ma1


def test_intersect_with_different_points() -> None:
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(4, 5), 6)
    ma2 = ManhattanArc3D.from_point(p2)
    with pytest.raises(AssertionError):
        ma1.intersect_with(ma2)


def test_get_center() -> None:
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    center = ma.get_center()
    assert center.xcoord.xcoord == 1
    assert center.xcoord.ycoord == 2
    assert center.ycoord == 3


def test_get_lower_corner() -> None:
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    lower_corner = ma.get_lower_corner()
    assert lower_corner.xcoord.xcoord == 1
    assert lower_corner.xcoord.ycoord == 2
    assert lower_corner.ycoord == 3


def test_get_upper_corner() -> None:
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    upper_corner = ma.get_upper_corner()
    assert upper_corner.xcoord.xcoord == 1
    assert upper_corner.xcoord.ycoord == 2
    assert upper_corner.ycoord == 3


def test_repr() -> None:
    """Test string representation of ManhattanArc3D"""
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)
    repr_str = repr(ma)

    # Should contain all three ManhattanArc representations
    assert "/" in repr_str
    assert "," in repr_str


def test_merge_with() -> None:
    """Test merging two ManhattanArc3D objects"""
    p1 = Point(Point(0, 0), 0)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(10, 0), 0)
    ma2 = ManhattanArc3D.from_point(p2)

    # Merge with alpha = 0
    merged = ma1.merge_with(ma2, 0)
    assert merged is not None

    # Merge with alpha = distance/2
    distance = ma1.min_dist_with(ma2)
    merged_half = ma1.merge_with(ma2, distance // 2)
    assert merged_half is not None

    # Merge with alpha = distance
    merged_full = ma1.merge_with(ma2, distance)
    assert merged_full is not None


def test_merge_with_zero_distance() -> None:
    """Test merging with zero distance"""
    p = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p)
    ma2 = ManhattanArc3D.from_point(p)

    merged = ma1.merge_with(ma2, 0)
    assert merged is not None


def test_nearest_point_to() -> None:
    """Test finding nearest point in ManhattanArc3D"""
    p1 = Point(Point(0, 0), 0)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(10, 10), 10)

    nearest = ma1.nearest_point_to(p2)
    assert nearest is not None
    assert isinstance(nearest, Point)


def test_nearest_point_to_same_point() -> None:
    """Test finding nearest point when target is the same"""
    p = Point(Point(1, 2), 3)
    ma = ManhattanArc3D.from_point(p)

    nearest = ma.nearest_point_to(p)
    assert nearest == p
