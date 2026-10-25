from typing import List

from physdes.point import Point
from physdes.rpolygon import RPolygon, canonicalize, expand_even_index, is_canonical

PointSet = List[Point[int, int]]


def test_is_canonical_two_point_vertical_segment() -> None:
    pointset = [Point(2, 1), Point(2, 0)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_two_point_canonical_form() -> None:
    pointset = [Point(2, 1), Point(3, -3)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_spike_is_allowed() -> None:
    pointset = [Point(2, 1), Point(2, 0), Point(3, -3)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_spike_with_shared_x() -> None:
    pointset = [Point(0, 0), Point(0, 1), Point(2, 0)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_rectangle() -> None:
    pointset = [Point(0, 0), Point(1, 1)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_l_shape() -> None:
    pointset = [Point(0, 0), Point(3, 1), Point(1, 3)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_collinear_stored_points() -> None:
    pointset = [Point(0, 0), Point(3, 3), Point(1, 1)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_consecutive_vertical() -> None:
    pointset = [Point(0, 0), Point(0, 1), Point(0, 2)]
    assert is_canonical(pointset) is False
    assert RPolygon.from_pointset(pointset).is_canonical() is False


def test_is_canonical_consecutive_horizontal() -> None:
    pointset = [Point(0, 0), Point(1, 0), Point(2, 0)]
    assert is_canonical(pointset) is False
    assert RPolygon.from_pointset(pointset).is_canonical() is False


def test_is_canonical_duplicate_point() -> None:
    pointset = [Point(0, 0), Point(0, 0)]
    assert is_canonical(pointset) is False
    assert RPolygon.from_pointset(pointset).is_canonical() is False


def test_is_canonical_repeated_nonadjacent_point() -> None:
    pointset = [Point(0, 0), Point(1, 1), Point(0, 0), Point(2, 2)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def _perimeter(pointset: PointSet) -> int:
    return sum(
        abs(nxt.xcoord - curr.xcoord) + abs(nxt.ycoord - curr.ycoord)
        for curr, nxt in zip(pointset, pointset[1:] + pointset[:1])
    )


def _area2(pointset: PointSet) -> int:
    boundary = expand_even_index(pointset)
    return sum(
        curr.xcoord * nxt.ycoord - nxt.xcoord * curr.ycoord
        for curr, nxt in zip(boundary, boundary[1:] + boundary[:1])
    )


def test_canonicalize_removes_redundant_vertex() -> None:
    pointset = [Point(0, 0), Point(1, 0), Point(2, 1)]
    result = canonicalize(pointset)
    assert result == [Point(0, 0), Point(2, 1)]
    assert is_canonical(result) is True


def test_canonicalize_keeps_nonadjacent_duplicate() -> None:
    pointset = [Point(0, 0), Point(1, 1), Point(0, 0), Point(2, 2)]
    result = canonicalize(pointset)
    assert result == pointset
    assert is_canonical(result) is True


def test_canonicalize_removes_consecutive_duplicate() -> None:
    pointset = [Point(0, 0), Point(1, 1), Point(1, 1), Point(2, 2)]
    result = canonicalize(pointset)
    assert result == [Point(0, 0), Point(1, 1), Point(2, 2)]
    assert is_canonical(result) is True


def test_canonicalize_collapses_duplicate_pair() -> None:
    pointset = [Point(0, 0), Point(0, 0)]
    assert canonicalize(pointset) == [Point(0, 0)]


def test_canonicalize_keeps_vertical_segment() -> None:
    pointset = [Point(2, 1), Point(2, 0)]
    assert canonicalize(pointset) == pointset
    assert is_canonical(pointset) is True


def test_canonicalize_collapses_axis_run() -> None:
    pointset = [Point(0, 0), Point(0, 1), Point(0, 2)]
    result = canonicalize(pointset)
    assert result == [Point(0, 0), Point(0, 2)]
    assert is_canonical(result) is True


def test_canonicalize_keeps_spike() -> None:
    pointset = [Point(0, 0), Point(2, 0), Point(1, 1)]
    assert canonicalize(pointset) == pointset
    assert is_canonical(pointset) is True


def test_canonicalize_is_idempotent() -> None:
    pointset = [Point(0, 2), Point(4, 0), Point(2, 4)]
    once = canonicalize(pointset)
    assert once == pointset
    assert canonicalize(once) == once
    assert is_canonical(once) is True


def test_canonicalize_preserves_perimeter() -> None:
    pointset = [Point(0, 0), Point(1, 0), Point(2, 1)]
    assert _perimeter(canonicalize(pointset)) == _perimeter(pointset)


def test_canonicalize_preserves_area() -> None:
    pointset = [Point(0, 0), Point(1, 0), Point(2, 1)]
    assert _area2(canonicalize(pointset)) == _area2(pointset)


def test_canonicalize_keeps_area_changing_vertex() -> None:
    pointset = [Point(0, 0), Point(3, 3), Point(1, 1)]
    assert canonicalize(pointset) == pointset
    assert is_canonical(pointset) is True
