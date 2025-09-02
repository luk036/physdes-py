from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.polygon import (
    Polygon,
    create_test_polygon,
    create_xmono_polygon,
    create_ymono_polygon,
    point_in_polygon,
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
    P = Polygon.from_pointset(S)
    assert P.signed_area_x2 == 4074624


def test_polygon3():
    hgen = Halton([2, 3], [11, 7])
    coords = [hgen.pop() for _ in range(20)]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    S = create_xmono_polygon(S)
    P = Polygon.from_pointset(S)
    assert P.signed_area_x2 == 3862080


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
    assert convex_polygon.is_convex() is True

    # Test case 2: Non-convex polygon
    non_convex_coords = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2)]
    non_convex_points = [Point(x, y) for x, y in non_convex_coords]
    non_convex_polygon = Polygon.from_pointset(non_convex_points)
    assert non_convex_polygon.is_convex() is False

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
