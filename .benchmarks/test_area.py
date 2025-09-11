import pytest

from physdes.point import Point
from physdes.polygon import Polygon
from physdes.rpolygon import RPolygon

RECTILINEAR_POLYGON_COORDS = [
    (0, 0),
    (10, 10),
    (5, 5),
]


@pytest.fixture
def rectilinear_polygon_points():
    return [Point(x, y) for x, y in RECTILINEAR_POLYGON_COORDS]


def test_polygon_signed_area(benchmark, rectilinear_polygon_points):
    rp = RPolygon(rectilinear_polygon_points)
    p: Polygon = rp.to_polygon()
    result = benchmark(lambda: p.signed_area_x2)
    assert abs(result) == 150


def test_rpolygon_signed_area(benchmark, rectilinear_polygon_points):
    rp = RPolygon(rectilinear_polygon_points)
    result = benchmark(lambda: rp.signed_area)
    assert abs(result) == 75
