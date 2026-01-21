from typing import Union

import pytest

from physdes.generic import (
    contain,
    displacement,
    intersection,
    min_dist,
    nearest,
    overlap,
)
from physdes.interval import Interval
from physdes.point import Point
from physdes.vector2 import Vector2


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
