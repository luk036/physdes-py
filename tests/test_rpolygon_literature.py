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


def _assert_convex_pieces(pointset: PointSet, expected_area2: List[int]) -> None:
    pieces = rpolygon_cut_convex(pointset, True)
    assert sorted(_area2(piece) for piece in pieces) == expected_area2
    assert sum(_area2(piece) for piece in pieces) == _area2(pointset)
    for piece in pieces:
        assert is_canonical(piece) is True
        assert is_simple(piece) is True
        assert rpolygon_is_orthogonally_convex(piece) is True


def test_agplib_rand_10_1() -> None:
    # AGPLIB/AGPVG, rand-10-1.pol. Couto, de Souza, and de Rezende,
    # "An Exact and Efficient Algorithm for the Orthogonal Art Gallery
    # Problem", SIBGRAPI 2007.
    full = [
        Point(4, 1),
        Point(5, 1),
        Point(5, 5),
        Point(3, 5),
        Point(3, 4),
        Point(1, 4),
        Point(1, 2),
        Point(2, 2),
        Point(2, 3),
        Point(4, 3),
    ]
    stored = full[::2]
    assert is_canonical(stored) is True
    assert is_simple(stored) is True
    assert rpolygon_is_orthogonally_convex(stored) is False
    _assert_convex_pieces(stored, [4, 14])


def test_agplib_rand_12_6() -> None:
    # AGPLIB/AGPVG, rand-12-6.pol. The same source as rand-10-1.
    full = [
        Point(4, 1),
        Point(6, 1),
        Point(6, 6),
        Point(5, 6),
        Point(5, 4),
        Point(2, 4),
        Point(2, 5),
        Point(1, 5),
        Point(1, 2),
        Point(3, 2),
        Point(3, 3),
        Point(4, 3),
    ]
    stored = full[::2]
    assert is_canonical(stored) is True
    assert is_simple(stored) is True
    assert rpolygon_is_orthogonally_convex(stored) is False
    _assert_convex_pieces(stored, [4, 10, 14])
