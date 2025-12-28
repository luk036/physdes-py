"""
Hypothesis tests for Point class operations.

This module contains property-based tests for the Point class using the
hypothesis library. These tests verify mathematical properties and invariants
that should hold for all valid inputs.
"""

from hypothesis import given, strategies as st
import pytest

from physdes.point import Point
from physdes.vector2 import Vector2
from physdes.interval import Interval


# Strategy for generating numeric values (integers and floats)
numeric_values = st.one_of(
    st.integers(min_value=-1000, max_value=1000),
    st.floats(min_value=-1000.0, max_value=1000.0, allow_nan=False, allow_infinity=False)
)

# Strategy for generating Interval objects
interval_strategy = st.builds(
    Interval,
    lb=numeric_values,
    ub=numeric_values
).filter(lambda interval: interval.lb <= interval.ub)

# Strategy for generating Point objects with numeric coordinates
point_numeric_strategy = st.builds(
    Point,
    xcoord=numeric_values,
    ycoord=numeric_values
)

# Strategy for generating Point objects with interval coordinates
point_interval_strategy = st.builds(
    Point,
    xcoord=interval_strategy,
    ycoord=interval_strategy
)

# Strategy for generating any type of Point
point_strategy = st.one_of(point_numeric_strategy, point_interval_strategy)

# Strategy for generating Vector2 objects
vector2_strategy = st.builds(
    Vector2,
    x=numeric_values,
    y=numeric_values
)


class TestPointNumericProperties:
    """Test properties of points with numeric coordinates."""
    
    @given(point_numeric_strategy, vector2_strategy)
    def test_point_vector_addition(self, p: Point, v: Vector2) -> None:
        """Test that adding a vector to a point updates coordinates correctly."""
        result = p + v
        assert result.xcoord == p.xcoord + v.x
        assert result.ycoord == p.ycoord + v.y
    
    @given(point_numeric_strategy, vector2_strategy)
    def test_point_vector_subtraction(self, p: Point, v: Vector2) -> None:
        """Test that subtracting a vector from a point updates coordinates correctly."""
        result = p - v
        assert result.xcoord == p.xcoord - v.x
        assert result.ycoord == p.ycoord - v.y
    
    @given(point_numeric_strategy, vector2_strategy)
    def test_point_vector_addition_subtraction_inverse(self, p: Point, v: Vector2) -> None:
        """Test that addition and subtraction are inverse operations."""
        result = (p + v) - v
        assert result.xcoord == p.xcoord
        assert result.ycoord == p.ycoord
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_displacement(self, p1: Point, p2: Point) -> None:
        """Test that displacement between points is calculated correctly."""
        disp = p1.displace(p2)
        assert disp.x == p2.xcoord - p1.xcoord
        assert disp.y == p2.ycoord - p1.ycoord
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_displacement_antisymmetric(self, p1: Point, p2: Point) -> None:
        """Test that displacement is antisymmetric: p1.displace(p2) == -p2.displace(p1)."""
        disp1 = p1.displace(p2)
        disp2 = p2.displace(p1)
        assert disp1.x == -disp2.x
        assert disp1.y == -disp2.y
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_min_distance_symmetry(self, p1: Point, p2: Point) -> None:
        """Test that minimum distance is symmetric."""
        dist1 = p1.min_dist_with(p2)
        dist2 = p2.min_dist_with(p1)
        assert dist1 == dist2
    
    @given(point_numeric_strategy)
    def test_point_min_distance_self(self, p: Point) -> None:
        """Test that distance from a point to itself is zero."""
        assert p.min_dist_with(p) == 0
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_hull_properties(self, p1: Point, p2: Point) -> None:
        """Test properties of hull operation."""
        hull = p1.hull_with(p2)
        
        # Hull should contain both original points
        assert hull.contains(p1)
        assert hull.contains(p2)
        
        # Hull coordinates should be min/max of original coordinates
        assert hull.xcoord.lb <= min(p1.xcoord, p2.xcoord)
        assert hull.xcoord.ub >= max(p1.xcoord, p2.xcoord)
        assert hull.ycoord.lb <= min(p1.ycoord, p2.ycoord)
        assert hull.ycoord.ub >= max(p1.ycoord, p2.ycoord)
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_hull_commutativity(self, p1: Point, p2: Point) -> None:
        """Test that hull operation is commutative."""
        hull1 = p1.hull_with(p2)
        hull2 = p2.hull_with(p1)
        assert hull1 == hull2
    
    @given(point_numeric_strategy, numeric_values)
    def test_point_enlarge_properties(self, p: Point, delta: float) -> None:
        """Test properties of enlarge operation."""
        enlarged = p.enlarge_with(delta)
        
        # Enlarged point should contain original point
        assert enlarged.contains(p)
        
        # Enlarged coordinates should be original ± delta
        assert enlarged.xcoord.lb <= p.xcoord - delta
        assert enlarged.xcoord.ub >= p.xcoord + delta
        assert enlarged.ycoord.lb <= p.ycoord - delta
        assert enlarged.ycoord.ub >= p.ycoord + delta
    
    @given(point_numeric_strategy, numeric_values)
    def test_point_flip_properties(self, p: Point) -> None:
        """Test properties of flip operation."""
        flipped = p.flip()
        assert flipped.xcoord == p.ycoord
        assert flipped.ycoord == p.xcoord
    
    @given(point_numeric_strategy)
    def test_point_double_flip(self, p: Point) -> None:
        """Test that double flip returns original point."""
        assert p.flip().flip() == p


class TestPointIntervalProperties:
    """Test properties of points with interval coordinates."""
    
    @given(point_interval_strategy, point_interval_strategy)
    def test_interval_point_overlap_properties(self, p1: Point, p2: Point) -> None:
        """Test properties of overlap for interval points."""
        # Overlap should be symmetric
        assert p1.overlaps(p2) == p2.overlaps(p1)
        
        # If p1 contains p2, then they should overlap
        if p1.contains(p2):
            assert p1.overlaps(p2)
    
    @given(point_interval_strategy)
    def test_interval_point_self_containment(self, p: Point) -> None:
        """Test that a point contains itself."""
        assert p.contains(p)
    
    @given(point_interval_strategy, point_interval_strategy)
    def test_interval_point_containment_transitivity(self, p1: Point, p2: Point, p3: Point) -> None:
        """Test transitivity of containment."""
        if p1.contains(p2) and p2.contains(p3):
            assert p1.contains(p3)
    
    @given(point_interval_strategy, point_interval_strategy)
    def test_interval_point_intersection_properties(self, p1: Point, p2: Point) -> None:
        """Test properties of intersection for interval points."""
        intersection = p1.intersect_with(p2)
        
        # If intersection is valid, it should be contained in both points
        if not intersection.is_invalid():
            assert p1.contains(intersection)
            assert p2.contains(intersection)
    
    @given(point_interval_strategy, point_interval_strategy)
    def test_interval_point_min_distance_non_negative(self, p1: Point, p2: Point) -> None:
        """Test that minimum distance is always non-negative."""
        dist = p1.min_dist_with(p2)
        assert dist >= 0
    
    @given(point_interval_strategy, point_interval_strategy)
    def test_interval_point_min_distance_zero_if_overlap(self, p1: Point, p2: Point) -> None:
        """Test that min distance is zero if points overlap."""
        if p1.overlaps(p2):
            assert p1.min_dist_with(p2) == 0


class TestPointComparison:
    """Test comparison operations between points."""
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_total_ordering(self, p1: Point, p2: Point) -> None:
        """Test that points have total ordering."""
        # Exactly one of these should be true for distinct points
        if p1 != p2:
            assert (p1 < p2) or (p2 < p1)
            assert not ((p1 < p2) and (p2 < p1))
    
    @given(point_numeric_strategy, point_numeric_strategy, point_numeric_strategy)
    def test_point_ordering_transitivity(self, p1: Point, p2: Point, p3: Point) -> None:
        """Test transitivity of point ordering."""
        if p1 < p2 and p2 < p3:
            assert p1 < p3
    
    @given(point_numeric_strategy)
    def test_point_comparison_reflexivity(self, p: Point) -> None:
        """Test reflexivity of point comparison."""
        assert not (p < p)
        assert p <= p
        assert p >= p
        assert not (p > p)
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_comparison_antisymmetry(self, p1: Point, p2: Point) -> None:
        """Test antisymmetry of point comparison."""
        if p1 <= p2 and p2 <= p1:
            assert p1 == p2


class TestPointEdgeCases:
    """Test edge cases and special conditions."""
    
    @given(point_strategy)
    def test_point_equality_reflexivity(self, p: Point) -> None:
        """Test that a point is equal to itself."""
        assert p == p
    
    @given(point_strategy, point_strategy)
    def test_point_equality_symmetry(self, p1: Point, p2: Point) -> None:
        """Test that equality is symmetric."""
        result = p1 == p2
        assert result == (p2 == p1)
    
    @given(point_strategy, point_strategy, point_strategy)
    def test_point_equality_transitivity(self, p1: Point, p2: Point, p3: Point) -> None:
        """Test that equality is transitive."""
        if p1 == p2 and p2 == p3:
            assert p1 == p3
    
    @given(point_strategy)
    def test_point_repr_roundtrip(self, p: Point) -> None:
        """Test that the repr contains expected information."""
        repr_str = repr(p)
        assert "Point" in repr_str
        assert str(p.xcoord) in repr_str
        assert str(p.ycoord) in repr_str
    
    @given(point_strategy)
    def test_point_str_format(self, p: Point) -> None:
        """Test that string representation follows expected format."""
        str_repr = str(p)
        assert str_repr.startswith("(")
        assert str_repr.endswith(")")
        assert "," in str_repr


class TestPointNestedPoints:
    """Test properties of nested Point objects (higher-dimensional points)."""
    
    @given(numeric_values, numeric_values, numeric_values)
    def test_nested_point_creation(self, x: float, y: float, z: float) -> None:
        """Test creating and manipulating nested points."""
        p2d = Point(x, y)
        p3d = Point(p2d, z)
        
        assert p3d.xcoord == p2d
        assert p3d.ycoord == z
    
    @given(numeric_values, numeric_values, numeric_values, numeric_values)
    def test_nested_point_vector_addition(self, x: float, y: float, z: float, scalar: float) -> None:
        """Test vector addition with nested points."""
        p2d = Point(x, y)
        p3d = Point(p2d, z)
        v = Vector2(scalar, scalar)
        
        result = p3d + v
        
        assert result.xcoord == p2d + v
        assert result.ycoord == z + scalar
    
    @given(numeric_values, numeric_values, numeric_values, numeric_values)
    def test_nested_point_flip(self, x: float, y: float, z: float, w: float) -> None:
        """Test flip operation with nested points."""
        p2d = Point(x, y)
        p3d = Point(p2d, z)
        p4d = Point(p3d, w)
        
        flipped = p4d.flip()
        
        assert flipped.xcoord == p3d
        assert flipped.ycoord == w


class TestPointGeometricProperties:
    """Test geometric properties and invariants."""
    
    @given(point_numeric_strategy, point_numeric_strategy, point_numeric_strategy)
    def test_point_hull_associativity(self, p1: Point, p2: Point, p3: Point) -> None:
        """Test that hull operation is associative."""
        hull1 = p1.hull_with(p2).hull_with(p3)
        hull2 = p1.hull_with(p2.hull_with(p3))
        
        # Both hulls should contain all three points
        for p in [p1, p2, p3]:
            assert hull1.contains(p)
            assert hull2.contains(p)
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_manhattan_distance_properties(self, p1: Point, p2: Point) -> None:
        """Test properties of Manhattan distance."""
        dist = p1.min_dist_with(p2)
        
        # Manhattan distance should be non-negative
        assert dist >= 0
        
        # Should equal absolute sum of coordinate differences for numeric points
        expected = abs(p1.xcoord - p2.xcoord) + abs(p1.ycoord - p2.ycoord)
        assert dist == expected
    
    @given(point_numeric_strategy, numeric_values, numeric_values)
    def test_point_enlarge_contains_original(self, p: Point, dx: float, dy: float) -> None:
        """Test that enlarged point contains original point."""
        enlarged = p.enlarge_with(dx)
        assert enlarged.contains(p)
    
    @given(point_numeric_strategy, point_numeric_strategy)
    def test_point_intersection_commutativity(self, p1: Point, p2: Point) -> None:
        """Test that intersection is commutative."""
        intersection1 = p1.intersect_with(p2)
        intersection2 = p2.intersect_with(p1)
        assert intersection1 == intersection2