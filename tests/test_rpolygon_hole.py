from typing import List

from physdes.point import Point
from physdes.rpolygon import (
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


def test_convex_decomposition_of_bridged_hole() -> None:
    # The bridge from the outer boundary to the hole is traversed twice, so
    # the expanded boundary touches itself; the stored list remains admissible.
    pointset = [
        Point(4, 1),
        Point(10, 7),
        Point(7, 5),
        Point(9, 2),
        Point(6, 5),
        Point(7, 7),
    ]
    assert is_canonical(pointset) is True
    assert is_simple(pointset) is False

    pieces = rpolygon_cut_convex(pointset, True)
    assert len(pieces) == 3
    assert sorted(_area2(piece) for piece in pieces) == [4, 20, 30]
    assert sum(_area2(piece) for piece in pieces) == _area2(pointset)
    for piece in pieces:
        assert is_canonical(piece) is True
        assert is_simple(piece) is True
        assert rpolygon_is_orthogonally_convex(piece) is True
