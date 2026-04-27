"""
Tests for manhattan_arc_3d.py - ManhattanArc3D class

This module provides comprehensive tests for the ManhattanArc3D class
which represents a 3D Manhattan arc (rotated coordinate system).
"""

import pytest
from typing import Union

from physdes.interval import Interval
from physdes.manhattan_arc_3d import ManhattanArc3D
from physdes.point import Point


class TestManhattanArc3DInit:
    """Test ManhattanArc3D initialization with various coordinate types."""

    def test_init_with_scalars(self):
        """Test initialization with scalar integer coordinates."""
        arc = ManhattanArc3D(12, -4, 2, 6)
        assert arc.w_i == 12
        assert arc.x_i == -4
        assert arc.y_i == 2
        assert arc.z_i == 6

    def test_init_with_intervals(self):
        """Test initialization with Interval objects."""
        w = Interval(10, 20)
        x = Interval(-5, 5)
        y = Interval(0, 10)
        z = Interval(5, 15)
        arc = ManhattanArc3D(w, x, y, z)
        assert arc.w_i == w
        assert arc.x_i == x
        assert arc.y_i == y
        assert arc.z_i == z

    def test_init_mixed_types(self):
        """Test initialization with mixed scalar and interval types."""
        w = 10
        x = Interval(-5, 5)
        y = 2
        z = Interval(5, 15)
        arc = ManhattanArc3D(w, x, y, z)
        assert arc.w_i == w
        assert arc.x_i == x
        assert arc.y_i == y
        assert arc.z_i == z


class TestManhattanArc3DConstruct:
    """Test class methods and static methods."""

    def test_construct_simple(self):
        """Test construct static method with simple coordinates."""
        arc = ManhattanArc3D.construct(8, 10, 6)
        # xx = 8 - 10 = -2
        # yy = 8 + 10 = 18
        # w = (18 + 6) // 2 = 12
        # x = (-2 - 6) // 2 = -4
        # y = (-2 + 6) // 2 = 2
        # z = (18 - 6) // 2 = 6
        assert arc.w_i == 12
        assert arc.x_i == -4
        assert arc.y_i == 2
        assert arc.z_i == 6

    def test_construct_with_zero(self):
        """Test construct with zero coordinates."""
        arc = ManhattanArc3D.construct(0, 0, 0)
        assert arc.w_i == 0
        assert arc.x_i == 0
        assert arc.y_i == 0
        assert arc.z_i == 0

    def test_construct_with_negative(self):
        """Test construct with negative coordinates."""
        arc = ManhattanArc3D.construct(-5, -3, -2)
        # xx = -5 - (-3) = -2
        # yy = -5 + (-3) = -8
        # w = (-8 + -2) // 2 = -5
        # x = (-2 - -2) // 2 = 0
        # y = (-2 + -2) // 2 = -2
        # z = (-8 - -2) // 2 = -3
        assert arc.w_i == -5
        assert arc.x_i == 0
        assert arc.y_i == -2
        assert arc.z_i == -3


class TestManhattanArc3DFromPoint:
    """Test from_point class method."""

    def test_from_point_3d(self):
        inner = Point(8, 6)
        pt = Point(inner, 10)
        arc = ManhattanArc3D.from_point(pt)
        assert arc.w_i == 12
        assert arc.x_i == -4
        assert arc.y_i == 2
        assert arc.z_i == 6


class TestManhattanArc3DStringRepresentation:
    """Test __repr__, __str__, and __eq__ methods."""

    def test_repr(self):
        """Test __repr__ method."""
        arc = ManhattanArc3D(12, -4, 2, 6)
        assert repr(arc) == "ManhattanArc3D(12, -4, 2, 6)"

    def test_str(self):
        """Test __str__ method."""
        arc = ManhattanArc3D(12, -4, 2, 6)
        assert str(arc) == "/12, -4, 2, 6/"

    def test_eq_equal(self):
        """Test __eq__ with equal objects."""
        a = ManhattanArc3D(12, -4, 2, 6)
        b = ManhattanArc3D(12, -4, 2, 6)
        assert a == b

    def test_eq_not_equal(self):
        """Test __eq__ with different objects."""
        a = ManhattanArc3D(12, -4, 2, 6)
        b = ManhattanArc3D(7, 9, 2, 2)
        assert a != b

    def test_eq_different_type(self):
        """Test __eq__ with different type returns NotImplemented."""
        a = ManhattanArc3D(12, -4, 2, 6)
        assert a.__eq__("string") is NotImplemented
        assert a.__eq__(42) is NotImplemented
        assert a.__eq__(None) is NotImplemented


class TestManhattanArc3DOperations:
    """Test main operations: min_dist_with, enlarge_with, intersect_with, merge_with."""

    def test_min_dist_with_scalars(self):
        """Test min_dist_with with scalar coordinates."""
        r1 = ManhattanArc3D(4 + 5 + 3, 4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3)
        r2 = ManhattanArc3D(7 + 9 + 2, 7 - 9 - 2, 7 - 9 + 2, 7 + 9 - 2)
        # These are from the doctests - they should work
        result = r1.min_dist_with(r2)
        assert isinstance(result, int)
        assert result >= 0

    def test_min_dist_with_intervals(self):
        """Test min_dist_with with interval coordinates."""
        r1 = ManhattanArc3D(Interval(10, 20), Interval(-5, 5), Interval(0, 10), Interval(5, 15))
        r2 = ManhattanArc3D(Interval(15, 25), Interval(0, 10), Interval(5, 15), Interval(10, 20))
        result = r1.min_dist_with(r2)
        assert isinstance(result, int)
        assert result >= 0

    def test_min_dist_with_self(self):
        """Test min_dist_with with self (identical objects)."""
        r1 = ManhattanArc3D(12, -4, 2, 6)
        result = r1.min_dist_with(r1)
        assert result == 0

    def test_enlarge_with(self):
        """Test enlarge_with method."""
        a = ManhattanArc3D(4 + 5 + 3, 4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3)
        # a = ManhattanArc3D(12, -4, 2, 6) with scalars
        r = a.enlarge_with(1)
        assert isinstance(r, ManhattanArc3D)

    def test_enlarge_with_zero(self):
        arc = ManhattanArc3D(12, -4, 2, 6)
        r = arc.enlarge_with(0)
        assert r.w_i == Interval(12, 12)
        assert r.x_i == Interval(-4, -4)

    def test_enlarge_with_intervals(self):
        w = Interval(10, 20)
        x = Interval(-5, 5)
        y = Interval(0, 10)
        z = Interval(5, 15)
        arc = ManhattanArc3D(w, x, y, z)
        r = arc.enlarge_with(5)
        assert isinstance(r, ManhattanArc3D)

    def test_intersect_with(self):
        """Test intersect_with method."""
        r1 = ManhattanArc3D(Interval(10, 20), Interval(-5, 5), Interval(0, 10), Interval(5, 15))
        r2 = ManhattanArc3D(Interval(15, 25), Interval(0, 10), Interval(5, 15), Interval(10, 20))
        result = r1.intersect_with(r2)
        assert isinstance(result, ManhattanArc3D)

    def test_intersect_with_no_overlap(self):
        """Test intersect_with with non-overlapping intervals."""
        r1 = ManhattanArc3D(Interval(0, 10), Interval(0, 10), Interval(0, 10), Interval(0, 10))
        r2 = ManhattanArc3D(Interval(20, 30), Interval(20, 30), Interval(20, 30), Interval(20, 30))
        result = r1.intersect_with(r2)
        # Non-overlapping should result in invalid/empty intervals
        assert isinstance(result, ManhattanArc3D)

    def test_merge_with(self):
        """Test merge_with method."""
        r1 = ManhattanArc3D(4 + 5 + 3, 4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3)
        r2 = ManhattanArc3D(7 + 9 + 2, 7 - 9 - 2, 7 - 9 + 2, 7 + 9 - 2)
        result = r1.merge_with(r2, 4)
        assert isinstance(result, ManhattanArc3D)

    def test_merge_with_large_alpha(self):
        """Test merge_with with large alpha value."""
        r1 = ManhattanArc3D(40 + 50 + 30, 40 - 50 - 30, 40 - 50 + 30, 40 + 50 - 30)
        r2 = ManhattanArc3D(70 + 90 + 20, 70 - 90 - 20, 70 - 90 + 20, 70 + 90 - 20)
        result = r1.merge_with(r2, 40)
        assert isinstance(result, ManhattanArc3D)


class TestManhattanArc3DToPoint:
    """Test to_point method."""

    def test_to_point(self):
        """Test to_point conversion."""
        a = ManhattanArc3D(12, -4, 2, 6)
        pt = a.to_point()
        assert isinstance(pt, Point)
        # From doctest: print(a.to_point()) = ((8, 6), 10)
        # xx = x_i + y_i = -4 + 2 = -2
        # zz = z_i + w_i = 6 + 12 = 18
        # xcoord = (xx + zz) // 2 = (-2 + 18) // 2 = 8
        # ycoord = (-xx + zz) // 2 = (2 + 18) // 2 = 10
        # zcoord = (w_i - x_i + y_i - z_i) // 2 = (12 - (-4) + 2 - 6) // 2 = 12 // 2 = 6
        assert pt.ycoord == 10

    def test_to_point_with_intervals(self):
        """Test to_point with interval coordinates."""
        a = ManhattanArc3D(Interval(10, 20), Interval(-5, 5), Interval(0, 10), Interval(5, 15))
        pt = a.to_point()
        assert isinstance(pt, Point)


class TestManhattanArc3DCorners:
    """Test get_center, get_lower_corner, get_upper_corner methods."""

    def test_get_center(self):
        """Test get_center method."""
        r1 = ManhattanArc3D(40 + 50 + 30, 40 - 50 - 30, 40 - 50 + 30, 40 + 50 - 30)
        r2 = ManhattanArc3D(70 + 90 + 20, 70 - 90 - 20, 70 - 90 + 20, 70 + 90 - 20)
        r3 = r1.merge_with(r2, 40)
        center = r3.get_center()
        assert isinstance(center, Point)

    def test_get_lower_corner(self):
        """Test get_lower_corner method."""
        r1 = ManhattanArc3D(40 + 50 + 30, 40 - 50 - 30, 40 - 50 + 30, 40 + 50 - 30)
        r2 = ManhattanArc3D(70 + 90 + 20, 70 - 90 - 20, 70 - 90 + 20, 70 + 90 - 20)
        r3 = r1.merge_with(r2, 40)
        lower = r3.get_lower_corner()
        assert isinstance(lower, Point)

    def test_get_upper_corner(self):
        """Test get_upper_corner method."""
        r1 = ManhattanArc3D(40 + 50 + 30, 40 - 50 - 30, 40 - 50 + 30, 40 + 50 - 30)
        r2 = ManhattanArc3D(70 + 90 + 20, 70 - 90 - 20, 70 - 90 + 20, 70 + 90 - 20)
        r3 = r1.merge_with(r2, 40)
        upper = r3.get_upper_corner()
        assert isinstance(upper, Point)


class TestManhattanArc3DNearest:
    """Test nearest point methods."""

    def test_nearest_point_to(self):
        """Test nearest_point_to method."""
        r1 = ManhattanArc3D(40 + 50 + 30, 40 - 50 - 30, 40 - 50 + 30, 40 + 50 - 30)
        r2 = ManhattanArc3D(70 + 90 + 20, 70 - 90 - 20, 70 - 90 + 20, 70 + 90 - 20)
        r3 = r1.merge_with(r2, 40)
        # Test with Point object
        other = Point(Point(1000, 1000), 1000)
        nearest = r3.nearest_point_to(other)
        assert isinstance(nearest, Point)

    def test_nearest_point_to_origin(self):
        """Test nearest_point_to with origin."""
        r1 = ManhattanArc3D(40 + 50 + 30, 40 - 50 - 30, 40 - 50 + 30, 40 + 50 - 30)
        r2 = ManhattanArc3D(70 + 90 + 20, 70 - 90 - 20, 70 - 90 + 20, 70 + 90 - 20)
        r3 = r1.merge_with(r2, 40)
        # Test with construct(0, 0, 0)
        other = ManhattanArc3D.construct(0, 0, 0)
        nearest = r3._nearest_point_to(other)
        assert isinstance(nearest, Point)


class TestManhattanArc3DEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_zero_coordinates(self):
        """Test with all zero coordinates."""
        arc = ManhattanArc3D(0, 0, 0, 0)
        assert arc.w_i == 0
        assert arc.x_i == 0
        assert arc.y_i == 0
        assert arc.z_i == 0

    def test_negative_coordinates(self):
        """Test with negative coordinates."""
        arc = ManhattanArc3D(-10, -20, -30, -40)
        assert arc.w_i == -10
        assert arc.x_i == -20
        assert arc.y_i == -30
        assert arc.z_i == -40

    def test_large_coordinates(self):
        """Test with large coordinates."""
        arc = ManhattanArc3D(10**6, 10**6, 10**6, 10**6)
        assert arc.w_i == 10**6

    def test_min_dist_with_zero_distance(self):
        """Test min_dist_with when objects are at same location."""
        arc1 = ManhattanArc3D(10, 20, 30, 40)
        arc2 = ManhattanArc3D(10, 20, 30, 40)
        assert arc1.min_dist_with(arc2) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
