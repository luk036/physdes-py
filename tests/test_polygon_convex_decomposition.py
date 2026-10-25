"""
Unit tests for Polygon convex decomposition algorithms.

This module tests that the convex decomposition algorithms preserve the signed area
of the original polygon - the sum of the signed areas of the convex pieces should
equal the signed area of the original polygon.
"""

from typing import List

from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.polygon import Polygon
from physdes.rpolygon import (
    RPolygon,
    create_test_rpolygon,
    is_canonical,
    is_simple,
    rpolygon_is_orthogonally_convex,
    rpolygon_make_convex_hull,
)
from physdes.rpolygon_cut import rpolygon_cut_convex


def _even_index_to_boundary(pointset: List[Point[int, int]]) -> List[Point[int, int]]:
    """Expand a canonical even-index representation into the full polygon boundary.

    The omitted vertex between two stored vertices is recovered by moving x first,
    then y, i.e. ``(next.x, curr.y)``.
    """
    boundary: List[Point[int, int]] = []
    for curr, nxt in zip(pointset, pointset[1:] + pointset[:1]):
        boundary.append(curr)
        boundary.append(Point(nxt.xcoord, curr.ycoord))
    return boundary


def test_rpolygon_cut_convex_area_preservation() -> None:
    """Test that rpolygon_cut_convex preserves the signed area of the original polygon."""
    # Test with a randomly generated polygon
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(15)]
    S0 = create_test_rpolygon([Point(xcoord, ycoord) for xcoord, ycoord in coords])

    # Create a convex hull to ensure we have a valid polygon
    P = RPolygon.from_pointset(S0)
    is_anticlockwise = P.is_anticlockwise()
    S = rpolygon_make_convex_hull(S0, is_anticlockwise)

    # Calculate the signed area of the original polygon
    original_polygon = Polygon.from_pointset(S)
    original_area = original_polygon.signed_area_x2

    # Decompose the polygon into convex pieces
    convex_pieces = rpolygon_cut_convex(S, is_anticlockwise)

    # Calculate the sum of signed areas of all convex pieces
    total_area = 0
    for piece in convex_pieces:
        piece_polygon = Polygon.from_pointset(piece)
        total_area += piece_polygon.signed_area_x2

    # The sum of areas should equal the original area
    assert (
        total_area == original_area
    ), f"Area mismatch: original={original_area}, sum={total_area}"


def test_convex_decomposition_with_even_index_polygon() -> None:
    """Test area preservation for a polygon given in even-index representation."""
    coords = [(0, -2), (1, -3), (3, -2), (2, -1), (4, 1), (3, 0), (2, 1)]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]

    original_area = Polygon.from_pointset(_even_index_to_boundary(S)).signed_area_x2

    convex_pieces = rpolygon_cut_convex(S, True)
    assert len(convex_pieces) > 1, "the non-convex polygon should be cut"
    for piece in convex_pieces:
        assert is_canonical(piece), f"piece is not canonical: {piece}"
        assert is_simple(piece), f"piece is not simple: {piece}"
        assert rpolygon_is_orthogonally_convex(
            piece
        ), f"piece is not orthogonally convex: {piece}"

    total_area = 0
    for piece in convex_pieces:
        piece_polygon = Polygon.from_pointset(_even_index_to_boundary(piece))
        total_area += piece_polygon.signed_area_x2

    assert (
        total_area == original_area
    ), f"Convex cut area mismatch: original={original_area}, sum={total_area}"


def test_convex_decomposition_with_twelve_point_even_index_polygon() -> None:
    """Test area preservation and convexity for a non-convex 12-point even-index polygon."""
    coords = [
        (-1, 1),
        (0, 0),
        (1, -1),
        (3, 0),
        (4, 1),
        (6, 2),
        (5, 5),
        (4, 4),
        (3, 2),
        (2, 3),
        (1, 2),
        (0, 3),
    ]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]

    original_area = Polygon.from_pointset(_even_index_to_boundary(S)).signed_area_x2
    assert original_area > 0, "the test polygon should be anticlockwise"

    convex_pieces = rpolygon_cut_convex(S, True)
    assert len(convex_pieces) > 1, "the non-convex polygon should be cut"
    for piece in convex_pieces:
        assert is_canonical(piece), f"piece is not canonical: {piece}"
        assert is_simple(piece), f"piece is not simple: {piece}"
        assert rpolygon_is_orthogonally_convex(
            piece
        ), f"piece is not orthogonally convex: {piece}"

    total_area = 0
    for piece in convex_pieces:
        piece_polygon = Polygon.from_pointset(_even_index_to_boundary(piece))
        total_area += piece_polygon.signed_area_x2

    assert (
        total_area == original_area
    ), f"Convex cut area mismatch: original={original_area}, sum={total_area}"


def test_multiple_random_polygons() -> None:
    """Test area preservation with multiple randomly generated polygons."""
    for seed in [(3, 2), (2, 3), (5, 7), (7, 5)]:
        for size in [10, 15, 20]:
            hgen = Halton(seed, [7, 11])
            coords = [hgen.pop() for _ in range(size)]
            S0 = create_test_rpolygon(
                [Point(xcoord, ycoord) for xcoord, ycoord in coords]
            )

            # Create a convex hull to ensure we have a valid polygon
            P = RPolygon.from_pointset(S0)
            is_anticlockwise = P.is_anticlockwise()
            S = rpolygon_make_convex_hull(S0, is_anticlockwise)

            # Calculate the signed area of the original polygon
            original_polygon = Polygon.from_pointset(S)
            original_area = original_polygon.signed_area_x2

            # Decompose the polygon into convex pieces
            convex_pieces = rpolygon_cut_convex(S, is_anticlockwise)

            # Calculate the sum of signed areas of all convex pieces
            total_area = 0
            for piece in convex_pieces:
                piece_polygon = Polygon.from_pointset(piece)
                total_area += piece_polygon.signed_area_x2

            # The sum of areas should equal the original area
            assert (
                total_area == original_area
            ), f"Area mismatch for seed={seed}, size={size}: original={original_area}, sum={total_area}"
