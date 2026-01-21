"""
Hypothesis tests for Recti class operations.

This module contains property-based tests for the Rectangle, VSegment, and HSegment
classes using the hypothesis library. These tests verify mathematical properties and
invariants that should hold for all valid inputs.
"""

from hypothesis import given
from hypothesis import strategies as st

from physdes.interval import Interval
from physdes.point import Point
from physdes.recti import HSegment, Rectangle, VSegment

# Strategy for generating integer values
int_values = st.integers(min_value=-100, max_value=100)

# Strategy for generating Interval objects with integer bounds
interval_strategy = st.builds(Interval, lb=int_values, ub=int_values).filter(lambda interval: interval.lb <= interval.ub)

# Strategy for generating Rectangle objects
rectangle_strategy = st.builds(Rectangle, xcoord=interval_strategy, ycoord=interval_strategy)

# Strategy for generating VSegment objects
vsegment_strategy = st.builds(VSegment, xcoord=int_values, ycoord=interval_strategy)

# Strategy for generating HSegment objects
hsegment_strategy = st.builds(HSegment, xcoord=interval_strategy, ycoord=int_values)

# Strategy for generating Point objects with integer coordinates
point_strategy = st.builds(Point, xcoord=int_values, ycoord=int_values)


class TestRectangleProperties:
    """Test properties of Rectangle class."""

    @given(rectangle_strategy)
    def test_rectangle_bounds_consistency(self, rect: Rectangle) -> None:
        """Test that rectangle bounds are consistent."""
        # Lower-left corner should have lower bounds
        assert rect.ll.xcoord == rect.xcoord.lb
        assert rect.ll.ycoord == rect.ycoord.lb

        # Upper-right corner should have upper bounds
        assert rect.ur.xcoord == rect.xcoord.ub
        assert rect.ur.ycoord == rect.ycoord.ub

    @given(rectangle_strategy)
    def test_rectangle_non_negative_dimensions(self, rect: Rectangle) -> None:
        """Test that rectangle dimensions are non-negative."""
        assert rect.width() >= 0
        assert rect.height() >= 0
        assert rect.area() >= 0

    @given(rectangle_strategy)
    def test_rectangle_area_calculation(self, rect: Rectangle) -> None:
        """Test that area is calculated correctly."""
        expected_area = rect.width() * rect.height()
        assert rect.area() == expected_area

    @given(rectangle_strategy)
    def test_rectangle_flip_properties(self, rect: Rectangle) -> None:
        """Test properties of rectangle flip operation."""
        flipped = rect.flip()

        # Flipped rectangle should swap dimensions
        assert flipped.xcoord == rect.ycoord
        assert flipped.ycoord == rect.xcoord

        # Double flip should return original
        assert flipped.flip().xcoord == rect.xcoord
        assert flipped.flip().ycoord == rect.ycoord

    @given(rectangle_strategy)
    def test_rectangle_contains_self(self, rect: Rectangle) -> None:
        """Test that rectangle contains itself."""
        assert rect.contains(rect)

    @given(rectangle_strategy, point_strategy)
    def test_rectangle_point_containment(self, rect: Rectangle, point: Point) -> None:
        """Test point containment in rectangle."""
        contains = rect.contains(point)

        # If point is contained, its coordinates should be within rectangle bounds
        if contains:
            assert rect.xcoord.lb <= point.xcoord <= rect.xcoord.ub
            assert rect.ycoord.lb <= point.ycoord <= rect.ycoord.ub

    @given(rectangle_strategy, rectangle_strategy)
    def test_rectangle_containment_properties(self, rect1: Rectangle, rect2: Rectangle) -> None:
        """Test rectangle containment properties."""
        # If rect1 contains rect2, then rect1 should contain rect2's corners
        if rect1.contains(rect2):
            assert rect1.contains(rect2.ll)
            assert rect1.contains(rect2.ur)

    @given(rectangle_strategy, rectangle_strategy)
    def test_rectangle_overlap_symmetry(self, rect1: Rectangle, rect2: Rectangle) -> None:
        """Test that overlap is symmetric."""
        assert rect1.overlaps(rect2) == rect2.overlaps(rect1)

    @given(rectangle_strategy, rectangle_strategy)
    def test_rectangle_containment_implication_overlap(self, rect1: Rectangle, rect2: Rectangle) -> None:
        """Test that containment implies overlap."""
        if rect1.contains(rect2):
            assert rect1.overlaps(rect2)

    @given(rectangle_strategy, rectangle_strategy)
    def test_rectangle_intersection_properties(self, rect1: Rectangle, rect2: Rectangle) -> None:
        """Test properties of rectangle intersection."""
        intersection = rect1.intersect_with(rect2)

        # Check if intersection is valid (both x and y intervals are non-empty)
        if (
            isinstance(intersection.xcoord, Interval)
            and intersection.xcoord.lb <= intersection.xcoord.ub
            and isinstance(intersection.ycoord, Interval)
            and intersection.ycoord.lb <= intersection.ycoord.ub
        ):
            # Valid intersection should be contained in both rectangles
            assert rect1.contains(intersection)
            assert rect2.contains(intersection)

    @given(rectangle_strategy, rectangle_strategy)
    def test_rectangle_hull_properties(self, rect1: Rectangle, rect2: Rectangle) -> None:
        """Test properties of rectangle hull."""
        hull = rect1.hull_with(rect2)

        # Hull should contain both rectangles
        assert hull.contains(rect1)
        assert hull.contains(rect2)

        # Hull bounds should encompass both rectangles
        assert hull.xcoord.lb <= min(rect1.xcoord.lb, rect2.xcoord.lb)
        assert hull.xcoord.ub >= max(rect1.xcoord.ub, rect2.xcoord.ub)
        assert hull.ycoord.lb <= min(rect1.ycoord.lb, rect2.ycoord.lb)
        assert hull.ycoord.ub >= max(rect1.ycoord.ub, rect2.ycoord.ub)

    @given(rectangle_strategy, rectangle_strategy)
    def test_rectangle_hull_commutativity(self, rect1: Rectangle, rect2: Rectangle) -> None:
        """Test that hull operation is commutative."""
        hull1 = rect1.hull_with(rect2)
        hull2 = rect2.hull_with(rect1)
        assert hull1 == hull2

    @given(rectangle_strategy, rectangle_strategy)
    def test_rectangle_min_distance_properties(self, rect1: Rectangle, rect2: Rectangle) -> None:
        """Test properties of minimum distance between rectangles."""
        dist = rect1.min_dist_with(rect2)

        # Distance should be non-negative
        assert dist >= 0

        # Distance should be zero if rectangles overlap
        if rect1.overlaps(rect2):
            assert dist == 0

    @given(rectangle_strategy, rectangle_strategy)
    def test_rectangle_min_distance_symmetry(self, rect1: Rectangle, rect2: Rectangle) -> None:
        """Test that minimum distance is symmetric."""
        dist1 = rect1.min_dist_with(rect2)
        dist2 = rect2.min_dist_with(rect1)
        assert dist1 == dist2


class TestVSegmentProperties:
    """Test properties of VSegment class."""

    @given(vsegment_strategy)
    def test_vsegment_bounds_consistency(self, seg: VSegment) -> None:
        """Test that vertical segment bounds are consistent."""
        # X coordinate should be constant
        assert seg.xcoord == seg.xcoord

        # Y coordinates should define the segment
        assert seg.ycoord.lb <= seg.ycoord.ub

    @given(vsegment_strategy)
    def test_vsegment_non_negative_length(self, seg: VSegment) -> None:
        """Test that segment length is non-negative."""
        assert seg.height() >= 0

    @given(vsegment_strategy)
    def test_vsegment_flip_properties(self, seg: VSegment) -> None:
        """Test properties of vertical segment flip operation."""
        flipped = seg.flip()

        # Flipped segment should become horizontal
        assert isinstance(flipped, HSegment)

        # Coordinates should be swapped
        assert flipped.xcoord == seg.ycoord
        assert flipped.ycoord == seg.xcoord

        # Double flip should return original type
        assert flipped.flip().__class__ == VSegment

    @given(vsegment_strategy)
    def test_vsegment_contains_self(self, seg: VSegment) -> None:
        """Test that segment contains itself."""
        assert seg.contains(seg)

    @given(vsegment_strategy, point_strategy)
    def test_vsegment_point_containment(self, seg: VSegment, point: Point) -> None:
        """Test point containment in vertical segment."""
        contains = seg.contains(point)

        # If point is contained, its x coordinate should match and y should be within bounds
        if contains:
            assert point.xcoord == seg.xcoord
            assert seg.ycoord.lb <= point.ycoord <= seg.ycoord.ub

    @given(vsegment_strategy, vsegment_strategy)
    def test_vsegment_overlap_symmetry(self, seg1: VSegment, seg2: VSegment) -> None:
        """Test that overlap is symmetric."""
        assert seg1.overlaps(seg2) == seg2.overlaps(seg1)

    @given(vsegment_strategy, vsegment_strategy)
    def test_vsegment_containment_implication_overlap(self, seg1: VSegment, seg2: VSegment) -> None:
        """Test that containment implies overlap."""
        if seg1.contains(seg2):
            assert seg1.overlaps(seg2)


class TestHSegmentProperties:
    """Test properties of HSegment class."""

    @given(hsegment_strategy)
    def test_hsegment_bounds_consistency(self, seg: HSegment) -> None:
        """Test that horizontal segment bounds are consistent."""
        # Y coordinate should be constant
        assert seg.ycoord == seg.ycoord

        # X coordinates should define the segment
        assert seg.xcoord.lb <= seg.xcoord.ub

    @given(hsegment_strategy)
    def test_hsegment_non_negative_length(self, seg: HSegment) -> None:
        """Test that segment length is non-negative."""
        assert seg.width() >= 0

    @given(hsegment_strategy)
    def test_hsegment_flip_properties(self, seg: HSegment) -> None:
        """Test properties of horizontal segment flip operation."""
        flipped = seg.flip()

        # Flipped segment should become vertical
        assert isinstance(flipped, VSegment)

        # Coordinates should be swapped
        assert flipped.xcoord == seg.ycoord
        assert flipped.ycoord == seg.xcoord

        # Double flip should return original type
        assert flipped.flip().__class__ == HSegment

    @given(hsegment_strategy)
    def test_hsegment_contains_self(self, seg: HSegment) -> None:
        """Test that segment contains itself."""
        assert seg.contains(seg)

    @given(hsegment_strategy, point_strategy)
    def test_hsegment_point_containment(self, seg: HSegment, point: Point) -> None:
        """Test point containment in horizontal segment."""
        contains = seg.contains(point)

        # If point is contained, its y coordinate should match and x should be within bounds
        if contains:
            assert point.ycoord == seg.ycoord
            assert seg.xcoord.lb <= point.xcoord <= seg.xcoord.ub

    @given(hsegment_strategy, hsegment_strategy)
    def test_hsegment_overlap_symmetry(self, seg1: HSegment, seg2: HSegment) -> None:
        """Test that overlap is symmetric."""
        assert seg1.overlaps(seg2) == seg2.overlaps(seg1)

    @given(hsegment_strategy, hsegment_strategy)
    def test_hsegment_containment_implication_overlap(self, seg1: HSegment, seg2: HSegment) -> None:
        """Test that containment implies overlap."""
        if seg1.contains(seg2):
            assert seg1.overlaps(seg2)


class TestSegmentRectangleInteractions:
    """Test interactions between segments and rectangles."""

    @given(rectangle_strategy, vsegment_strategy)
    def test_rectangle_vsegment_overlap(self, rect: Rectangle, seg: VSegment) -> None:
        """Test overlap between rectangle and vertical segment."""
        # Overlap should be symmetric
        assert rect.overlaps(seg) == seg.overlaps(rect)

    @given(rectangle_strategy, hsegment_strategy)
    def test_rectangle_hsegment_overlap(self, rect: Rectangle, seg: HSegment) -> None:
        """Test overlap between rectangle and horizontal segment."""
        # Overlap should be symmetric
        assert rect.overlaps(seg) == seg.overlaps(rect)

    @given(rectangle_strategy, vsegment_strategy)
    def test_rectangle_vsegment_containment(self, rect: Rectangle, seg: VSegment) -> None:
        """Test containment between rectangle and vertical segment."""
        # If rectangle contains segment, it should contain segment's endpoints
        if rect.contains(seg):
            # Check endpoints of the segment
            lower_point = Point(seg.xcoord, seg.ycoord.lb)
            upper_point = Point(seg.xcoord, seg.ycoord.ub)
            assert rect.contains(lower_point)
            assert rect.contains(upper_point)

    @given(rectangle_strategy, hsegment_strategy)
    def test_rectangle_hsegment_containment(self, rect: Rectangle, seg: HSegment) -> None:
        """Test containment between rectangle and horizontal segment."""
        # If rectangle contains segment, it should contain segment's endpoints
        if rect.contains(seg):
            # Check endpoints of the segment
            lower_point = Point(seg.xcoord.lb, seg.ycoord)
            upper_point = Point(seg.xcoord.ub, seg.ycoord)
            assert rect.contains(lower_point)
            assert rect.contains(upper_point)


class TestGeometricInvariants:
    """Test geometric invariants across all shape types."""

    @given(rectangle_strategy, rectangle_strategy, rectangle_strategy)
    def test_rectangle_hull_associativity_weak(self, rect1: Rectangle, rect2: Rectangle, rect3: Rectangle) -> None:
        """Test weak associativity of rectangle hull operation."""
        hull12 = rect1.hull_with(rect2)
        hull23 = rect2.hull_with(rect3)

        # Both (rect1 ∪ rect2) ∪ rect3 and rect1 ∪ (rect2 ∪ rect3) should contain all three rectangles
        final_hull1 = hull12.hull_with(rect3)
        final_hull2 = rect1.hull_with(hull23)

        for rect in [rect1, rect2, rect3]:
            assert final_hull1.contains(rect)
            assert final_hull2.contains(rect)

    @given(rectangle_strategy)
    def test_rectangle_enlarge_properties(self, rect: Rectangle) -> None:
        """Test properties of rectangle enlargement."""
        delta = 5
        enlarged = rect.enlarge_with(delta)

        # Enlarged rectangle should contain original
        assert enlarged.contains(rect)

        # Enlarged bounds should be original ± delta
        assert enlarged.xcoord.lb <= rect.xcoord.lb - delta
        assert enlarged.xcoord.ub >= rect.xcoord.ub + delta
        assert enlarged.ycoord.lb <= rect.ycoord.lb - delta
        assert enlarged.ycoord.ub >= rect.ycoord.ub + delta

    @given(vsegment_strategy, vsegment_strategy)
    def test_vsegment_intersection_properties(self, seg1: VSegment, seg2: VSegment) -> None:
        """Test properties of vertical segment intersection."""
        # Only test intersection if segments have the same x-coordinate
        if seg1.xcoord == seg2.xcoord:
            intersection = seg1.intersect_with(seg2)

            # Check if intersection is valid (y interval is non-empty)
            if isinstance(intersection.ycoord, Interval) and intersection.ycoord.lb <= intersection.ycoord.ub:
                # Valid intersection should be contained in both segments
                assert seg1.contains(intersection)
                assert seg2.contains(intersection)

    @given(hsegment_strategy, hsegment_strategy)
    def test_hsegment_intersection_properties(self, seg1: HSegment, seg2: HSegment) -> None:
        """Test properties of horizontal segment intersection."""
        # Only test intersection if segments have the same y-coordinate
        if seg1.ycoord == seg2.ycoord:
            intersection = seg1.intersect_with(seg2)

            # Check if intersection is valid (x interval is non-empty)
            if isinstance(intersection.xcoord, Interval) and intersection.xcoord.lb <= intersection.xcoord.ub:
                # Valid intersection should be contained in both segments
                assert seg1.contains(intersection)
                assert seg2.contains(intersection)

    @given(vsegment_strategy, vsegment_strategy)
    def test_vsegment_min_distance_properties(self, seg1: VSegment, seg2: VSegment) -> None:
        """Test properties of minimum distance between vertical segments."""
        dist = seg1.min_dist_with(seg2)

        # Distance should be non-negative
        assert dist >= 0

        # Distance should be zero if segments overlap
        if seg1.overlaps(seg2):
            assert dist == 0

    @given(hsegment_strategy, hsegment_strategy)
    def test_hsegment_min_distance_properties(self, seg1: HSegment, seg2: HSegment) -> None:
        """Test properties of minimum distance between horizontal segments."""
        dist = seg1.min_dist_with(seg2)

        # Distance should be non-negative
        assert dist >= 0

        # Distance should be zero if segments overlap
        if seg1.overlaps(seg2):
            assert dist == 0


class TestEdgeCases:
    """Test edge cases and special conditions."""

    @given(int_values, int_values, int_values, int_values)
    def test_degenerate_rectangle(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Test handling of degenerate rectangles (lines or points)."""
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        rect = Rectangle(Interval(x1, x2), Interval(y1, y2))

        # Should still compute basic properties
        assert rect.width() >= 0
        assert rect.height() >= 0
        assert rect.area() >= 0

    @given(int_values, int_values, int_values)
    def test_degenerate_vsegment(self, x: int, y1: int, y2: int) -> None:
        """Test handling of degenerate vertical segments (points)."""
        if y1 > y2:
            y1, y2 = y2, y1

        seg = VSegment(x, Interval(y1, y2))

        # Should still compute basic properties
        assert seg.height() >= 0

    @given(int_values, int_values, int_values)
    def test_degenerate_hsegment(self, x1: int, x2: int, y: int) -> None:
        """Test handling of degenerate horizontal segments (points)."""
        if x1 > x2:
            x1, x2 = x2, x1

        seg = HSegment(Interval(x1, x2), y)

        # Should still compute basic properties
        assert seg.width() >= 0

    @given(rectangle_strategy)
    def test_rectangle_equality_properties(self, rect: Rectangle) -> None:
        """Test rectangle equality properties."""
        # Rectangle should be equal to itself
        assert rect == rect

        # Rectangle should not be equal to a different rectangle
        # (This is a basic sanity check)
        other = Rectangle(Interval(0, 1), Interval(0, 1))
        if rect.xcoord != other.xcoord or rect.ycoord != other.ycoord:
            assert rect != other
