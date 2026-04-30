from typing import Union

import pytest

from physdes.generic import (
    center,
    contain,
    displacement,
    intersection,
    lower,
    measure_of,
    min_dist,
    nearest,
    overlap,
    upper,
)
from physdes.interval import Interval
from physdes.point import Point
from physdes.vector2 import Vector2


class TestMeasureOf:
    """Tests for measure_of function"""

    def test_measure_of_scalar(self) -> None:
        assert measure_of(1) == 1

    def test_measure_of_interval(self) -> None:
        assert measure_of(Interval(1, 3)) == 2


class TestCenter:
    """Tests for center function"""

    def test_center_scalar(self) -> None:
        assert center(5) == 5

    def test_center_interval(self) -> None:
        assert center(Interval(1, 5)) == 3

    def test_center_point(self) -> None:
        pt = Point(Interval(1, 5), Interval(2, 6))
        result = center(pt)
        assert result == Point(3, 4)


class TestLower:
    """Tests for lower function"""

    def test_lower_scalar(self) -> None:
        assert lower(5) == 5

    def test_lower_interval(self) -> None:
        assert lower(Interval(1, 5)) == 1

    def test_lower_point(self) -> None:
        pt = Point(Interval(1, 5), Interval(2, 6))
        result = lower(pt)
        assert result == Point(1, 2)


class TestUpper:
    """Tests for upper function"""

    def test_upper_scalar(self) -> None:
        assert upper(5) == 5

    def test_upper_interval(self) -> None:
        assert upper(Interval(1, 5)) == 5

    def test_upper_point(self) -> None:
        pt = Point(Interval(1, 5), Interval(2, 6))
        result = upper(pt)
        assert result == Point(5, 6)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 1, True),
        (1, 3, False),
        (Interval(1, 2), Interval(2, 3), True),
        (Interval(1, 2), Interval(3, 4), False),
        (Interval(1, 2), 2, True),
        (Interval(1, 2), 4, False),
        (2, Interval(2, 3), True),
        (1, Interval(3, 4), False),
        (1, Interval(1, 2), True),
    ],
)
def test_overlap(
    a: Union[int, Interval], b: Union[int, Interval], expected: bool
) -> None:
    assert overlap(a, b) is expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 1, True),
        (1, 3, False),
        (Interval(1, 4), Interval(2, 3), True),
        (Interval(1, 2), Interval(3, 4), False),
        (Interval(1, 2), 2, True),
        (Interval(1, 2), 4, False),
        (2, Interval(2, 3), False),
        (1, Interval(3, 4), False),
    ],
)
def test_contain(
    a: Union[int, Interval], b: Union[int, Interval], expected: bool
) -> None:
    assert contain(a, b) is expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 1, 1),
        (Interval(1, 2), Interval(2, 3), Interval(2, 2)),
        (Interval(1, 2), 2, Interval(2, 2)),
        (2, Interval(2, 3), Interval(2, 2)),
        (1, Interval(1, 2), Interval(1, 1)),
        (Interval(1, 2), Interval(1, 2), Interval(1, 2)),
    ],
)
def test_intersection(
    a: Union[int, Interval], b: Union[int, Interval], expected: Union[int, Interval]
) -> None:
    assert intersection(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 1, 0),
        (1, 3, 2),
        (Interval(1, 2), Interval(2, 3), 0),
        (Interval(1, 2), Interval(3, 4), 1),
        (Interval(1, 2), 2, 0),
        (Interval(1, 2), 4, 2),
        (2, Interval(2, 3), 0),
        (1, Interval(3, 4), 2),
        (1, Interval(1, 2), 0),
        (Interval(1, 2), Interval(1, 2), 0),
    ],
)
def test_min_dist(
    a: Union[int, Interval], b: Union[int, Interval], expected: int
) -> None:
    assert min_dist(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 1, 1),
        (1, 3, 1),
        (Interval(1, 5), 8, 5),
        (Interval(1, 5), 0, 1),
        (Interval(1, 5), 4, 4),
    ],
)
def test_nearest(
    a: Union[int, Interval], b: Union[int, Interval], expected: int
) -> None:
    assert nearest(a, b) == expected


def test_nearest_point() -> None:
    p_of_i = Point(Interval(2, 5), Interval(3, 8))
    a = Point(1, 1)
    b = Point(6, 10)
    c = Point(3, 5)
    assert nearest(p_of_i, a) == Point(2, 3)
    assert nearest(p_of_i, b) == Point(5, 8)
    assert nearest(p_of_i, c) == Point(3, 5)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 1, 0),
        (1, 3, -2),
        (Interval(1, 2), Interval(2, 3), Interval(-1, -1)),
        (Interval(1, 2), Interval(3, 4), Interval(-2, -2)),
    ],
)
def test_displacement(
    a: Union[int, Interval], b: Union[int, Interval], expected: Union[int, Interval]
) -> None:
    assert displacement(a, b) == expected


def test_displacement_point() -> None:
    assert displacement(Point(1, 2), Point(3, 4)) == Vector2(-2, -2)
