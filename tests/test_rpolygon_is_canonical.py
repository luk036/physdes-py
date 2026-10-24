from physdes.point import Point
from physdes.rpolygon import RPolygon, is_canonical


def test_is_canonical_two_point_vertical_segment() -> None:
    pointset = [Point(2, 1), Point(2, 0)]
    assert is_canonical(pointset) is False
    assert RPolygon.from_pointset(pointset).is_canonical() is False


def test_is_canonical_two_point_canonical_form() -> None:
    pointset = [Point(2, 1), Point(3, -3)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_zero_change_reduces_to_two_points() -> None:
    pointset = [Point(2, 1), Point(2, 0), Point(3, -3)]
    assert is_canonical(pointset) is False
    assert RPolygon.from_pointset(pointset).is_canonical() is False


def test_is_canonical_zero_change_is_not_allowed() -> None:
    pointset = [Point(0, 0), Point(0, 1), Point(2, 0)]
    assert is_canonical(pointset) is False
    assert RPolygon.from_pointset(pointset).is_canonical() is False


def test_is_canonical_rectangle() -> None:
    pointset = [Point(0, 0), Point(1, 1)]
    assert is_canonical(pointset) is True
    assert RPolygon.from_pointset(pointset).is_canonical() is True


def test_is_canonical_l_shape() -> None:
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
