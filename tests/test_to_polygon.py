from physdes.point import Point
from physdes.polygon import Polygon
from physdes.rpolygon import RPolygon
from physdes.to_polygon import to_polygon


def test_to_polygon() -> None:
    coords = [(0, 0), (10, 10), (5, 5)]
    point_set = [Point(x, y) for x, y in coords]
    r_poly = RPolygon.from_pointset(point_set)
    poly = to_polygon(r_poly)

    expected_coords = [(0, 0), (10, 0), (10, 10), (5, 10), (5, 5), (0, 5)]
    expected_point_set = [Point(x, y) for x, y in expected_coords]
    expected_poly = Polygon.from_pointset(expected_point_set)

    assert poly == expected_poly


def test_to_polygon_non_rectilinear() -> None:
    coords = [(0, 0), (1, 1), (2, 0)]
    points = [Point(x, y) for x, y in coords]
    rpolygon = RPolygon.from_pointset(points)
    polygon = to_polygon(rpolygon)
    # The expected polygon should have extra points to make it rectilinear
    expected_coords = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0)]
    expected_points = [Point(x, y) for x, y in expected_coords]
    expected_polygon = Polygon.from_pointset(expected_points)
    assert polygon._vecs == expected_polygon._vecs
