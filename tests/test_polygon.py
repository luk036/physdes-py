import pytest
from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.polygon import (
    Polygon,
    create_test_polygon,
    create_xmono_polygon,
    create_ymono_polygon,
    point_in_polygon,
    polygon_is_anticlockwise,
    polygon_is_xmonotone,
    polygon_is_ymonotone,
    polygon_make_convex_hull,
)
from physdes.vector2 import Vector2


def test_polygon():
    coords = [
        (-2, 2),
        (0, -1),
        (-5, 1),
        (-2, 4),
        (0, -4),
        (-4, 3),
        (-6, -2),
        (5, 1),
        (2, 2),
        (3, -3),
        (-3, -3),
        (3, 3),
        (-3, -4),
        (1, 4),
    ]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    S = create_test_polygon(S)
    assert polygon_is_anticlockwise(S)
    for p in S:
        print("{},{}".format(p.xcoord, p.ycoord), end=" ")
    P = Polygon.from_pointset(S)
    assert P.signed_area_x2 == 110
    assert P.is_anticlockwise()
    Q = Polygon.from_pointset(S)
    Q += Vector2(4, 5)
    Q -= Vector2(4, 5)
    assert Q == P


def test_ymono_polygon():
    coords = [
        (-2, 2),
        (0, -1),
        (-5, 1),
        (-2, 4),
        (0, -4),
        (-4, 3),
        (-6, -2),
        (5, 1),
        (2, 2),
        (3, -3),
        (-3, -3),
        (3, 3),
        (-3, -4),
        (1, 4),
    ]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    S = create_ymono_polygon(S)
    assert polygon_is_ymonotone(S)
    assert not polygon_is_xmonotone(S)
    assert polygon_is_anticlockwise(S)

    for p in S:
        print("{},{}".format(p.xcoord, p.ycoord), end=" ")
    P = Polygon.from_pointset(S)
    assert P.signed_area_x2 == 102
    assert P.is_anticlockwise()


def test_xmono_polygon():
    coords = [
        (-2, 2),
        (0, -1),
        (-5, 1),
        (-2, 4),
        (0, -4),
        (-4, 3),
        (-6, -2),
        (5, 1),
        (2, 2),
        (3, -3),
        (-3, -3),
        (3, 3),
        (-3, -4),
        (1, 4),
    ]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    S = create_xmono_polygon(S)
    assert polygon_is_xmonotone(S)
    assert not polygon_is_ymonotone(S)
    assert polygon_is_anticlockwise(S)
    for p in S:
        print("{},{}".format(p.xcoord, p.ycoord), end=" ")
    P = Polygon.from_pointset(S)
    assert P.signed_area_x2 == 111
    assert P.is_anticlockwise()


def test_polygon2():
    hgen = Halton([2, 3], [11, 7])
    coords = [hgen.pop() for _ in range(20)]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    S = create_ymono_polygon(S)
    assert polygon_is_ymonotone(S)
    assert not polygon_is_xmonotone(S)
    assert polygon_is_anticlockwise(S)
    P = Polygon.from_pointset(S)
    assert P.signed_area_x2 == 4074624
    assert P.is_anticlockwise()


def test_polygon3():
    hgen = Halton([2, 3], [11, 7])
    coords = [hgen.pop() for _ in range(20)]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    S = create_xmono_polygon(S)
    assert polygon_is_xmonotone(S)
    assert not polygon_is_ymonotone(S)
    assert polygon_is_anticlockwise(S)
    P = Polygon.from_pointset(S)
    assert P.signed_area_x2 == 3862080
    assert P.is_anticlockwise()


def test_polygon4():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(50)]
    S = create_test_polygon([Point(xcoord, ycoord) for xcoord, ycoord in coords])
    print('<svg viewBox="0 0 2187 2048" xmlns="http://www.w3.org/2000/svg">')
    print('  <polygon points="', end=" ")
    for p in S:
        print("{},{}".format(p.xcoord, p.ycoord), end=" ")
    print('"')
    print('  fill="#88C0D0" stroke="black" />')
    for p in S:
        print('  <circle cx="{}" cy="{}" r="10" />'.format(p.xcoord, p.ycoord))
    qx, qy = hgen.pop()
    print('  <circle cx="{}" cy="{}" r="10" fill="#BF616A" />'.format(qx, qy))
    print("</svg>")
    P = Polygon.from_pointset(S)
    assert P.signed_area_x2 == -4449600
    assert point_in_polygon(S, Point(qx, qy))


# def test_polygon3():
#     hgen = Halton([2, 3], [11, 7])
#     coords = [hgen() for _ in range(40)]
#     S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
#     S = create_ymono_polygon(S)
#     for p in S:
#         print("{},{}".format(p.xcoord, p.ycoord), end=' ')
#     P = Polygon.from_pointset(S)
#     assert P.signed_area_x2 == 3198528000


def test_is_rectilinear():
    # Create a rectilinear polygon
    rectilinear_coords = [(0, 0), (0, 1), (1, 1), (1, 0)]
    rectilinear_points = [Point(x, y) for x, y in rectilinear_coords]
    rectilinear_polygon = Polygon.from_pointset(rectilinear_points)
    assert rectilinear_polygon.is_rectilinear() is True

    # Create a non-rectilinear polygon
    non_rectilinear_coords = [(0, 0), (1, 1), (2, 0)]
    non_rectilinear_points = [Point(x, y) for x, y in non_rectilinear_coords]
    non_rectilinear_polygon = Polygon.from_pointset(non_rectilinear_points)
    assert non_rectilinear_polygon.is_rectilinear() is False


def test_is_convex():
    # Test case 1: Convex polygon
    convex_coords = [(0, 0), (2, 0), (2, 2), (0, 2)]
    convex_points = [Point(x, y) for x, y in convex_coords]
    convex_polygon = Polygon.from_pointset(convex_points)
    assert convex_polygon.is_convex(True) is True

    # Test case 2: Non-convex polygon
    non_convex_coords = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)]
    non_convex_points = [Point(x, y) for x, y in non_convex_coords]
    non_convex_polygon = Polygon.from_pointset(non_convex_points)
    assert non_convex_polygon.is_convex(True) is False

    # Test case 3: Triangle (always convex)
    triangle_coords = [(0, 0), (2, 0), (1, 2)]
    triangle_points = [Point(x, y) for x, y in triangle_coords]
    triangle = Polygon.from_pointset(triangle_points)
    assert triangle.is_convex() is True


def test_is_anticlockwise():
    # Clockwise polygon
    clockwise_coords = [(0, 0), (0, 1), (1, 1), (1, 0)]
    clockwise_points = [Point(x, y) for x, y in clockwise_coords]
    clockwise_polygon = Polygon.from_pointset(clockwise_points)
    assert clockwise_polygon.is_anticlockwise() is False

    # Counter-clockwise polygon
    counter_clockwise_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
    counter_clockwise_points = [Point(x, y) for x, y in counter_clockwise_coords]
    counter_clockwise_polygon = Polygon.from_pointset(counter_clockwise_points)
    assert counter_clockwise_polygon.is_anticlockwise() is True


def test_polygon_eq_different_type():
    coords = [(0, 0), (0, 1), (1, 1), (1, 0)]
    points = [Point(x, y) for x, y in coords]
    polygon = Polygon.from_pointset(points)
    assert (polygon == 1) is False


def test_is_convex_clockwise():
    # Convex clockwise polygon
    convex_coords = [(0, 0), (0, 2), (2, 2), (2, 0)]
    convex_points = [Point(x, y) for x, y in convex_coords]
    convex_polygon = Polygon.from_pointset(convex_points)
    assert convex_polygon.is_convex(False) is True

    # Non-convex clockwise polygon
    non_convex_coords = [(0, 0), (0, 2), (1, 1), (2, 2), (2, 0)]
    non_convex_points = [Point(x, y) for x, y in non_convex_coords]
    non_convex_polygon = Polygon.from_pointset(non_convex_points)
    assert non_convex_polygon.is_convex(False) is False


def test_point_in_polygon_missed_branches():
    coords = [(0, 0), (10, 0), (10, 10), (0, 10)]
    pointset = [Point(x, y) for x, y in coords]
    # Test case where ptq.ycoord == pt0.ycoord
    assert point_in_polygon(pointset, Point(5, 10)) is False
    # Test case where ptq.ycoord == pt1.ycoord
    assert (
        point_in_polygon(pointset, Point(5, 0)) is True
    )  # because of the strict inequality
    # Test case where det == 0 (point on edge)
    assert point_in_polygon(pointset, Point(5, 0)) is True


def test_polygon_is_anticlockwise_less_than_3_points():
    with pytest.raises(ValueError):
        coords = [(0, 0), (0, 1)]
        points = [Point(x, y) for x, y in coords]
        polygon_is_anticlockwise(points)


def test_is_anticlockwise_less_than_3_points():
    with pytest.raises(ValueError):
        coords = [(0, 0), (0, 1)]
        points = [Point(x, y) for x, y in coords]
        polygon = Polygon.from_pointset(points)
        polygon.is_anticlockwise()


def test_is_convex_more():
    # Non-convex anti-clockwise polygon
    non_convex_coords = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)]
    non_convex_points = [Point(x, y) for x, y in non_convex_coords]
    non_convex_polygon = Polygon.from_pointset(non_convex_points)
    assert non_convex_polygon.is_convex(True) is False

    # Convex anti-clockwise polygon
    convex_coords = [(0, 0), (2, 0), (2, 2), (0, 2)]
    convex_points = [Point(x, y) for x, y in convex_coords]
    convex_polygon = Polygon.from_pointset(convex_points)
    assert convex_polygon.is_convex(True) is True


def test_point_in_polygon_more():
    # Create a polygon that will trigger the missed branches
    coords = [(0, 0), (10, 5), (0, 10)]
    pointset = [Point(x, y) for x, y in coords]

    # This should trigger `det > 0`
    assert point_in_polygon(pointset, Point(1, 5)) is True

    # Create a clockwise polygon to trigger `det < 0`
    coords_cw = [(0, 0), (0, 10), (10, 5)]
    pointset_cw = [Point(x, y) for x, y in coords_cw]
    assert point_in_polygon(pointset_cw, Point(1, 5)) is True


def test_make_convex_hull():
    coords = [
        (-2, 5),
        (-4, 2),
        (-2, -4),
        (6, -3),
        (5, 0),
        (4, 2),
        (3, 3),
        (1, 4),
        (7, 5),
        (2, 6),
    ]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    assert polygon_is_anticlockwise(S)
    C = polygon_make_convex_hull(S)
    for p in C:
        print("({},{})".format(p.xcoord, p.ycoord), end=" ")
    assert polygon_is_anticlockwise(C)


def test_convex_hull():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(50)]
    S = create_test_polygon([Point(xcoord, ycoord) for xcoord, ycoord in coords])
    C = polygon_make_convex_hull(S)

    print('<svg viewBox="0 0 2187 2048" xmlns="http://www.w3.org/2000/svg">')

    print('  <polygon points="', end=" ")
    for p in C:
        print("{},{}".format(p.xcoord, p.ycoord), end=" ")
    print('"')
    print('  fill="#C0D088" stroke="black" opacity="0.3" />')

    print('  <polygon points="', end=" ")
    for p in S:
        print("{},{}".format(p.xcoord, p.ycoord), end=" ")
    print('"')
    print('  fill="#88C0D0" stroke="black" opacity="0.5" />')
    for p in S:
        print('  <circle cx="{}" cy="{}" r="10" />'.format(p.xcoord, p.ycoord))

    print("</svg>")

    assert not polygon_is_anticlockwise(C)
