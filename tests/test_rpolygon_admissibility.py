from typing import List

from physdes.point import Point
from physdes.rpolygon import (
    cleanup_collinear,
    expand_even_index,
    is_canonical,
    is_simple,
    rpolygon_is_orthogonally_convex,
)
from physdes.rpolygon_cut import rpolygon_cut_convex

PointSet = List[Point[int, int]]


def _area2(pointset: PointSet) -> int:
    boundary = expand_even_index(pointset)
    return sum(
        curr.xcoord * nxt.ycoord - nxt.xcoord * curr.ycoord
        for curr, nxt in zip(boundary, boundary[1:] + boundary[:1])
    )


def test_is_canonical_requires_two_points() -> None:
    assert is_canonical([]) is False
    assert is_canonical([Point(0, 0)]) is False


def test_canonical_is_not_simple() -> None:
    pointset = [Point(0, 2), Point(4, 0), Point(2, 4)]
    assert is_canonical(pointset) is True
    assert is_simple(pointset) is False


def test_cleanup_removes_point_between_neighbours() -> None:
    pointset = [Point(0, 0), Point(1, 0), Point(2, 1)]
    cleaned, admissible = cleanup_collinear(pointset)
    assert admissible is True
    assert [(p.xcoord, p.ycoord) for p in cleaned] == [(0, 0), (2, 1)]
    assert is_simple(cleaned) is True


def test_cleanup_rejects_spike() -> None:
    pointset = [Point(0, 0), Point(2, 0), Point(1, 1)]
    cleaned, admissible = cleanup_collinear(pointset)
    assert admissible is False
    assert [(p.xcoord, p.ycoord) for p in cleaned] == [
        (p.xcoord, p.ycoord) for p in pointset
    ]
    assert is_simple(cleaned) is False


def test_cleanup_rejects_axis_runs() -> None:
    vertical = [Point(0, 0), Point(0, 1), Point(0, 2)]
    horizontal = [Point(0, 0), Point(1, 0), Point(2, 0)]
    assert cleanup_collinear(vertical)[1] is False
    assert cleanup_collinear(horizontal)[1] is False


def test_cut_twelve_point_fixture_is_valid() -> None:
    pointset = [
        Point(-1, 1),
        Point(0, 0),
        Point(1, -1),
        Point(3, 0),
        Point(4, 1),
        Point(6, 2),
        Point(5, 5),
        Point(4, 4),
        Point(3, 2),
        Point(2, 3),
        Point(1, 2),
        Point(0, 3),
    ]
    pieces = rpolygon_cut_convex(pointset, True)
    assert len(pieces) == 3
    for piece in pieces:
        assert is_canonical(piece) is True
        assert is_simple(piece) is True
        assert rpolygon_is_orthogonally_convex(piece) is True
    assert sum(_area2(piece) for piece in pieces) == _area2(pointset)


def test_cut_discards_zero_width_sliver() -> None:
    pointset = [
        Point(0, -2),
        Point(1, -3),
        Point(3, -2),
        Point(2, -1),
        Point(4, 1),
        Point(3, 0),
        Point(2, 1),
    ]
    pieces = rpolygon_cut_convex(pointset, True)
    assert len(pieces) == 2
    for piece in pieces:
        assert is_canonical(piece) is True
        assert is_simple(piece) is True
        assert rpolygon_is_orthogonally_convex(piece) is True
    assert sum(_area2(piece) for piece in pieces) == _area2(pointset)
