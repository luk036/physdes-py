import pytest
from hypothesis import given
from hypothesis.strategies import integers

from physdes.generic import contain, displacement, intersection, min_dist, overlap
from physdes.interval import Interval, enlarge, hull


@given(
    integers(min_value=-1000, max_value=1000), integers(min_value=-1000, max_value=1000)
)
def test_interval_hypo(a1: int, a2: int) -> None:
    a = Interval(min(a1, a2), max(a1, a2))
    assert a.lb <= a.ub


def test_interval_arithmetic_hypo() -> None:
    @given(
        integers(min_value=-1000, max_value=1000),
        integers(min_value=0, max_value=1000),
        integers(min_value=-1000, max_value=1000),
    )
    def test_add_sub(a1, a2, v) -> None:
        a = Interval(min(a1, a2), max(a1, a2))
        assert (a + v) - v == a

    test_add_sub()


def test_interval() -> None:
    a = Interval(4, 8)
    b = Interval(5, 6)

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

    assert a.contains(4)
    assert a.contains(8)
    assert a.intersect_with(8) == Interval(8, 8)
    assert a.contains(b)
    assert a.intersect_with(b) == b


class TestIntervalEdgeCases:
    """Test edge cases for Interval class"""

    def test_interval_zero_length(self) -> None:
        """Test interval with zero length"""
        a = Interval(5, 5)
        assert a.lb == 5
        assert a.ub == 5
        assert a.contains(5)
        assert not a.contains(4)
        assert not a.contains(6)

    def test_interval_negative_bounds(self) -> None:
        """Test interval with negative bounds"""
        a = Interval(-10, -5)
        assert a.contains(-10)
        assert a.contains(-5)
        assert a.contains(-7)
        assert not a.contains(-11)
        assert not a.contains(-4)

    def test_interval_cross_zero(self) -> None:
        """Test interval that crosses zero"""
        a = Interval(-5, 5)
        assert a.contains(0)
        assert a.contains(-5)
        assert a.contains(5)
        assert not a.contains(-6)
        assert not a.contains(6)

    def test_interval_comparison_strict(self) -> None:
        """Test strict comparison operators"""
        a = Interval(1, 3)
        b = Interval(4, 6)

        assert a < b
        assert b > a
        assert not (b < a)
        assert not (a > b)

    def test_interval_comparison_equal(self) -> None:
        """Test comparison with equal intervals"""
        a = Interval(1, 3)
        b = Interval(1, 3)

        assert not (a < b)
        assert not (b < a)
        assert a <= b
        assert b <= a
        assert a >= b
        assert b >= a
        assert a == b
        assert not (a != b)

    def test_interval_intersect_with_disjoint(self) -> None:
        """Test intersection with disjoint intervals"""
        a = Interval(1, 3)
        b = Interval(5, 7)

        result = a.intersect_with(b)
        # Returns an invalid interval (lb > ub) for disjoint intervals
        assert result.lb > result.ub

    def test_interval_intersect_with_adjacent(self) -> None:
        """Test intersection with adjacent intervals"""
        a = Interval(1, 3)
        b = Interval(3, 5)

        result = a.intersect_with(b)
        # Adjacent intervals intersect at the boundary point
        assert result == Interval(3, 3)

    def test_interval_intersect_with_point(self) -> None:
        """Test intersection with a point"""
        a = Interval(1, 5)
        point = 3

        result = a.intersect_with(point)
        assert result == Interval(3, 3)

    def test_interval_intersect_with_point_outside(self) -> None:
        """Test intersection with point outside interval"""
        a = Interval(1, 5)
        point = 10

        result = a.intersect_with(point)
        # Returns an invalid interval for points outside
        assert result.lb > result.ub

    def test_interval_contains_interval_partial(self) -> None:
        """Test contains with partially overlapping interval"""
        a = Interval(1, 10)
        b = Interval(5, 15)

        assert not a.contains(b)
        assert not b.contains(a)

    def test_interval_contains_interval_complete(self) -> None:
        """Test contains when one interval completely contains another"""
        a = Interval(1, 10)
        b = Interval(3, 7)

        assert a.contains(b)
        assert not b.contains(a)

    def test_interval_addition(self) -> None:
        """Test interval addition"""
        a = Interval(1, 3)
        b = Interval(2, 4)

        result = a + b
        assert result == Interval(3, 7)

    def test_interval_subtraction(self) -> None:
        """Test interval subtraction"""
        a = Interval(5, 10)
        b = Interval(2, 3)

        result = a - b
        assert result == Interval(3, 7)

    def test_interval_addition_with_scalar(self) -> None:
        """Test interval addition with scalar"""
        a = Interval(1, 3)
        scalar = 5

        result = a + scalar
        assert result == Interval(6, 8)

    def test_interval_subtraction_with_scalar(self) -> None:
        """Test interval subtraction with scalar"""
        a = Interval(5, 10)
        scalar = 2

        result = a - scalar
        assert result == Interval(3, 8)

    def test_interval_str_representation(self) -> None:
        """Test string representation"""
        a = Interval(1, 5)
        str_repr = str(a)
        assert "1" in str_repr
        assert "5" in str_repr

    def test_interval_repr(self) -> None:
        """Test repr representation"""
        a = Interval(1, 5)
        repr_str = repr(a)
        assert "Interval" in repr_str


class TestIntervalFunctions:
    """Test interval utility functions"""

    def test_enlarge(self) -> None:
        """Test enlarge function"""
        a = Interval(1, 5)
        enlarged = enlarge(a, 2)

        assert enlarged.lb == -1
        assert enlarged.ub == 7

    def test_enlarge_zero(self) -> None:
        """Test enlarge with zero amount"""
        a = Interval(1, 5)
        enlarged = enlarge(a, 0)

        assert enlarged == a

    def test_enlarge_negative(self) -> None:
        """Test enlarge with negative amount"""
        a = Interval(1, 5)
        enlarged = enlarge(a, -1)

        assert enlarged.lb == 2
        assert enlarged.ub == 4

    def test_hull(self) -> None:
        """Test hull function"""
        a = Interval(1, 5)
        b = Interval(3, 8)

        result = hull(a, b)
        assert result == Interval(1, 8)

    def test_hull_disjoint(self) -> None:
        """Test hull with disjoint intervals"""
        a = Interval(1, 3)
        b = Interval(6, 8)

        result = hull(a, b)
        assert result == Interval(1, 8)

    def test_hull_identical(self) -> None:
        """Test hull with identical intervals"""
        a = Interval(1, 5)
        b = Interval(1, 5)

        result = hull(a, b)
        assert result == Interval(1, 5)

    def test_contain_function(self) -> None:
        """Test contain function from generic module"""
        a = Interval(1, 5)
        b = Interval(2, 4)

        assert contain(a, b)
        assert not contain(b, a)

    def test_intersection_function(self) -> None:
        """Test intersection function"""
        a = Interval(1, 5)
        b = Interval(3, 8)

        result = intersection(a, b)
        assert result == Interval(3, 5)

    def test_intersection_function_disjoint(self) -> None:
        """Test intersection function with disjoint intervals"""
        a = Interval(1, 3)
        b = Interval(5, 8)

        result = intersection(a, b)
        # Returns invalid interval for disjoint intervals
        assert result.lb > result.ub

    def test_min_dist_function(self) -> None:
        """Test min_dist function"""
        a = Interval(1, 3)
        b = Interval(6, 8)

        result = min_dist(a, b)
        assert result == 3  # Distance between 3 and 6

    def test_min_dist_overlapping(self) -> None:
        """Test min_dist with overlapping intervals"""
        a = Interval(1, 5)
        b = Interval(3, 8)

        result = min_dist(a, b)
        assert result == 0

    def test_overlap_function(self) -> None:
        """Test overlap function"""
        a = Interval(1, 5)
        b = Interval(3, 8)

        assert overlap(a, b)
        assert overlap(b, a)

    def test_overlap_function_disjoint(self) -> None:
        """Test overlap with disjoint intervals"""
        a = Interval(1, 3)
        b = Interval(5, 8)

        assert not overlap(a, b)
        assert not overlap(b, a)

    def test_overlap_function_adjacent(self) -> None:
        """Test overlap with adjacent intervals"""
        a = Interval(1, 3)
        b = Interval(3, 5)

        assert overlap(a, b)
        assert overlap(b, a)
        assert not b.contains(a)
        assert a.overlaps(b)
        assert b.overlaps(a)
        assert min_dist(a, b) == 0


@pytest.mark.parametrize(
    ("interval", "op", "value", "expected"),
    [
        (Interval(3, 5), "+", 1, Interval(4, 6)),
        (Interval(3, 5), "-", 1, Interval(2, 4)),
        (Interval(3, 5), "*", 2, Interval(6, 10)),
        (Interval(3, 5), "neg", None, Interval(-5, -3)),
        (Interval(3, 5), "+=", 1, Interval(4, 6)),
        (Interval(4, 6), "-=", 1, Interval(3, 5)),
        (Interval(3, 5), "*=", 2, Interval(6, 10)),
    ],
)
def test_arithmetic(interval, op, value, expected) -> None:
    if op == "+":
        assert interval + value == expected
    elif op == "-":
        assert interval - value == expected
    elif op == "*":
        assert interval * value == expected
    elif op == "neg":
        assert -interval == expected
    elif op == "+=":
        interval += value
        assert interval == expected
    elif op == "-=":
        interval -= value
        assert interval == expected
    elif op == "*=":
        interval *= value
        assert interval == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), True),
        (Interval(5, 7), Interval(7, 8), True),
        (Interval(3, 5), Interval(7, 8), False),
        (Interval(7, 8), Interval(3, 5), False),
        (Interval(3, 5), 4, True),
        (Interval(3, 5), 6, False),
        (4, Interval(3, 5), True),
        (6, Interval(3, 5), False),
        (4, 4, True),
    ],
)
def test_overlap(a, b, expected) -> None:
    assert overlap(a, b) is expected
    if isinstance(a, Interval):
        assert a.overlaps(b) is expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), False),
        (Interval(5, 7), Interval(7, 8), False),
        (Interval(3, 5), Interval(7, 8), False),
        (Interval(7, 8), Interval(3, 5), False),
        (Interval(3, 5), 4, True),
        (Interval(3, 5), 6, False),
        (4, Interval(3, 5), False),
        (4, 4, True),
    ],
)
def test_contains(a, b, expected) -> None:
    assert contain(a, b) is expected
    if isinstance(a, Interval):
        assert a.contains(b) is expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), Interval(5, 5)),
        (Interval(5, 7), Interval(7, 8), Interval(7, 7)),
        (Interval(3, 5), Interval(7, 8), None),
        (Interval(3, 5), 4, Interval(4, 4)),
        (Interval(3, 5), 6, None),
        (4, Interval(3, 5), Interval(4, 4)),
        (4, 4, 4),
    ],
)
def test_intersection(a, b, expected) -> None:
    if expected is not None:
        assert intersection(a, b) == expected
        if isinstance(a, Interval):
            assert a.intersect_with(b) == expected
    else:
        if isinstance(a, Interval):
            assert a.intersect_with(b).is_invalid()


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), Interval(3, 7)),
        (Interval(5, 7), Interval(7, 8), Interval(5, 8)),
        (Interval(3, 5), Interval(7, 8), Interval(3, 8)),
        (Interval(3, 5), 4, Interval(3, 5)),
        (Interval(3, 5), 6, Interval(3, 6)),
        (4, Interval(3, 5), Interval(3, 5)),
        (6, Interval(3, 5), Interval(3, 6)),
        (4, 6, Interval(4, 6)),
    ],
)
def test_hull(a, b, expected) -> None:
    assert hull(a, b) == expected
    if isinstance(a, Interval):
        assert a.hull_with(b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), 0),
        (Interval(3, 5), Interval(7, 8), 2),
        (Interval(5, 7), Interval(7, 8), 0),
        (Interval(3, 5), 4, 0),
        (4, Interval(3, 5), 0),
        (Interval(3, 5), 6, 1),
        (6, Interval(3, 5), 1),
    ],
)
def test_min_dist(a, b, expected) -> None:
    assert min_dist(a, b) == expected
    if isinstance(a, Interval):
        assert a.min_dist_with(b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), Interval(5, 7), Interval(-2, -2)),
        (Interval(3, 5), Interval(7, 8), Interval(-4, -3)),
        (Interval(5, 7), Interval(7, 8), Interval(-2, -1)),
        (4, 4, 0),
        (4, 6, -2),
        (6, 4, 2),
    ],
)
def test_displacement(a, b, expected) -> None:
    assert displacement(a, b) == expected
    if isinstance(a, Interval):
        assert a.displace(b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (Interval(3, 5), 2, Interval(1, 7)),
        (4, 6, Interval(-2, 10)),
        (6, 4, Interval(2, 10)),
    ],
)
def test_enlarge(a, b, expected) -> None:
    assert enlarge(a, b) == expected
    if isinstance(a, Interval):
        assert a.enlarge_with(b) == expected


# def test_interval_of_interval() -> None:
#     a = Interval(Interval(3, 4), Interval(8, 9))
#     b = Interval(Interval(5, 6), Interval(6, 7))
#     v = 3

#     assert not (a < b)
#     assert not (b < a)
#     assert not (a > b)
#     assert not (b > a)
#     assert a <= b
#     assert b <= a
#     assert a >= b
#     assert b >= a

#     assert not (b == a)
#     assert b != a

#     assert (a - v) + v == a

#     assert a.contains(Interval(4, 5))
#     assert a.contains(Interval(7, 8))
#     assert a.overlaps(Interval(7, 8))

#     # print(max(Interval(3, 4), 7))
#     # print(min(Interval(8, 9), 8))
#     # print(a.intersect_with(Interval(7, 8)))

#     # The following depends on how max() and min() are implemented!!!!
#     assert a.intersect_with(Interval(7, 8)) == Interval(7, Interval(8, 9))

#     assert a.contains(b)
#     assert a.intersect_with(b) == b
#     assert not b.contains(a)
#     assert a.overlaps(b)
#     assert b.overlaps(a)
#     assert min_dist(a, b) == 0
