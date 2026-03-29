"""
Unit tests for ManhattanArc3D class.
"""

from physdes.interval import Interval
from physdes.manhattan_arc_3d import ManhattanArc3D
from physdes.point import Point


def test_init() -> None:
    """Test ManhattanArc3D initialization with integer coordinates."""
    arc = ManhattanArc3D(-4, 2, 6, 12)
    assert arc.x_i == -4
    assert arc.y_i == 2
    assert arc.z_i == 6
    assert arc.w_i == 12


def test_init_with_intervals() -> None:
    """Test ManhattanArc3D initialization with interval coordinates."""
    x = Interval(-5, -3)
    y = Interval(1, 3)
    z = Interval(5, 7)
    w = Interval(11, 13)
    arc = ManhattanArc3D(x, y, z, w)
    assert arc.x_i == x
    assert arc.y_i == y
    assert arc.z_i == z
    assert arc.w_i == w


def test_construct() -> None:
    """Test ManhattanArc3D.construct factory method."""
    arc = ManhattanArc3D.construct(4, 5, 3)
    assert arc.x_i == -4
    assert arc.y_i == 2
    assert arc.z_i == 6
    assert arc.w_i == 12


def test_from_point() -> None:
    """Test ManhattanArc3D.from_point class method."""
    pt = Point(Point(4, 3), 5)
    arc = ManhattanArc3D.from_point(pt)
    assert arc.x_i == -4
    assert arc.y_i == 2
    assert arc.z_i == 6
    assert arc.w_i == 12


def test_repr() -> None:
    """Test __repr__ method."""
    arc = ManhattanArc3D(-4, 2, 6, 12)
    assert repr(arc) == "ManhattanArc3D(-4, 2, 6, 12)"


def test_str() -> None:
    """Test __str__ method."""
    arc = ManhattanArc3D(-4, 2, 6, 12)
    assert str(arc) == "/-4, 2, 6, 12/"


def test_str_with_intervals() -> None:
    """Test __str__ method with interval coordinates."""
    x = Interval(-5, -3)
    y = Interval(1, 3)
    z = Interval(5, 7)
    w = Interval(11, 13)
    arc = ManhattanArc3D(x, y, z, w)
    assert str(arc) == "/[-5, -3], [1, 3], [5, 7], [11, 13]/"


def test_eq() -> None:
    """Test __eq__ method."""
    a = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
    b = ManhattanArc3D(7 - 9 - 2, 7 - 9 + 2, 7 + 9 - 2, 7 + 9 + 2)
    c = ManhattanArc3D.construct(4, 5, 3)
    assert (a == b) is False
    assert (a == c) is True
    assert (a == 42) is False


def test_eq_with_intervals() -> None:
    """Test __eq__ method with interval coordinates."""
    x1 = Interval(-5, -3)
    y1 = Interval(1, 3)
    z1 = Interval(5, 7)
    w1 = Interval(11, 13)
    a = ManhattanArc3D(x1, y1, z1, w1)

    x2 = Interval(-5, -3)
    y2 = Interval(1, 3)
    z2 = Interval(5, 7)
    w2 = Interval(11, 13)
    b = ManhattanArc3D(x2, y2, z2, w2)

    assert a == b


def test_min_dist_with() -> None:
    """Test min_dist_with method."""
    r1 = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
    r2 = ManhattanArc3D(7 - 9 - 2, 7 - 9 + 2, 7 + 9 - 2, 7 + 9 + 2)
    assert r1.min_dist_with(r2) == 8


def test_min_dist_with_same_point() -> None:
    """Test min_dist_with when both arcs are at the same point."""
    arc1 = ManhattanArc3D.construct(4, 5, 3)
    arc2 = ManhattanArc3D.construct(4, 5, 3)
    assert arc1.min_dist_with(arc2) == 0


def test_min_dist_with_overlapping() -> None:
    """Test min_dist_with with overlapping intervals."""
    arc1 = ManhattanArc3D(0, 10, 0, 10)
    arc2 = ManhattanArc3D(5, 15, 5, 15)
    assert arc1.min_dist_with(arc2) == 5


def test_enlarge_with() -> None:
    """Test enlarge_with method."""
    a = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
    r = a.enlarge_with(1)
    assert r.x_i == Interval(-5, -3)
    assert r.y_i == Interval(1, 3)
    assert r.z_i == Interval(5, 7)
    assert r.w_i == Interval(11, 13)


def test_enlarge_with_zero() -> None:
    """Test enlarge_with with alpha=0 (returns degenerate intervals)."""
    arc = ManhattanArc3D(1, 2, 3, 4)
    result = arc.enlarge_with(0)
    assert result.x_i == Interval(1, 1)
    assert result.y_i == Interval(2, 2)
    assert result.z_i == Interval(3, 3)
    assert result.w_i == Interval(4, 4)


def test_enlarge_with_negative() -> None:
    """Test enlarge_with with negative alpha."""
    a = ManhattanArc3D(
        Interval(-5, -1), Interval(1, 5), Interval(5, 9), Interval(11, 15)
    )
    r = a.enlarge_with(-1)
    assert r.x_i == Interval(-4, -2)
    assert r.y_i == Interval(2, 4)
    assert r.z_i == Interval(6, 8)
    assert r.w_i == Interval(12, 14)


def test_intersect_with() -> None:
    """Test intersect_with method with identical coordinates."""
    r1 = ManhattanArc3D(0, 0, 0, 0)
    r2 = ManhattanArc3D(0, 0, 0, 0)
    result = r1.intersect_with(r2)
    assert result.x_i == 0
    assert result.y_i == 0
    assert result.z_i == 0
    assert result.w_i == 0


def test_intersect_with_intervals() -> None:
    """Test intersect_with with interval coordinates."""
    r1 = ManhattanArc3D(
        Interval(0, 10), Interval(0, 10), Interval(0, 10), Interval(0, 10)
    )
    r2 = ManhattanArc3D(
        Interval(5, 15), Interval(5, 15), Interval(5, 15), Interval(5, 15)
    )
    result = r1.intersect_with(r2)
    assert result.x_i == Interval(5, 10)
    assert result.y_i == Interval(5, 10)
    assert result.z_i == Interval(5, 10)
    assert result.w_i == Interval(5, 10)


def test_merge_with() -> None:
    """Test merge_with method."""
    r1 = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
    r2 = ManhattanArc3D(7 - 9 - 2, 7 - 9 + 2, 7 + 9 - 2, 7 + 9 + 2)
    result = r1.merge_with(r2, 4)
    assert result.x_i == Interval(-8, 0)
    assert result.y_i == Interval(-2, 4)
    assert result.z_i == Interval(10, 10)
    assert result.w_i == Interval(14, 16)


def test_merge_with_zero_alpha() -> None:
    """Test merge_with with alpha=0."""
    r1 = ManhattanArc3D(0, 10, 0, 10)
    r2 = ManhattanArc3D(20, 30, 20, 30)
    result = r1.merge_with(r2, 0)
    assert result is not None


def test_get_point() -> None:
    """Test get_point method."""
    a = ManhattanArc3D(-4, 2, 6, 12)
    pt = a.get_point()
    assert pt == Point(Point(4, 3), 5)


def test_get_point_with_intervals() -> None:
    """Test get_point method with interval coordinates."""
    a = ManhattanArc3D(
        Interval(0, 4), Interval(4, 8), Interval(8, 12), Interval(12, 16)
    )
    pt = a.get_point()
    assert pt.xcoord.xcoord == Interval(6, 10)
    assert pt.ycoord == Interval(3, 5)
    assert pt.xcoord.ycoord == Interval(1, 3)


def test_round_trip_construct_get_point() -> None:
    """Test that construct followed by get_point returns original point."""
    original = Point(Point(4, 3), 5)
    arc = ManhattanArc3D.from_point(original)
    result = arc.get_point()
    assert result == original


def test_round_trip_manual() -> None:
    """Test manual round-trip conversion."""
    xcoord = 4
    ycoord = 5
    zcoord = 3
    x = xcoord - ycoord - zcoord
    y = xcoord - ycoord + zcoord
    z = xcoord + ycoord - zcoord
    w = xcoord + ycoord + zcoord
    arc = ManhattanArc3D(x, y, z, w)
    result = arc.get_point()
    assert result.xcoord.xcoord == xcoord
    assert result.ycoord == ycoord
    assert result.xcoord.ycoord == zcoord
