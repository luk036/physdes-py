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
    P = Polygon(S)
    assert P.signed_area_x2 == 110
    Q = Polygon(S)
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
    P = Polygon(S)
    assert P.signed_area_x2 == 102


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
    P = Polygon(S)
    assert P.signed_area_x2 == 111


def test_polygon2():
    hgen = Halton([2, 3], [11, 7])
    coords = [hgen.pop() for _ in range(20)]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    S = create_ymono_polygon(S)
    P = Polygon(S)
    assert P.signed_area_x2 == 4074624


def test_polygon3():
    hgen = Halton([2, 3], [11, 7])
    coords = [hgen.pop() for _ in range(20)]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    S = create_xmono_polygon(S)
    P = Polygon(S)
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
    P = Polygon(S)
    assert P.signed_area_x2 == -4449600
    assert point_in_polygon(S, Point(qx, qy))


# def test_polygon3():
#     hgen = Halton([2, 3], [11, 7])
#     coords = [hgen() for _ in range(40)]
#     S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
#     S = create_ymono_polygon(S)
#     for p in S:
#         print("{},{}".format(p.xcoord, p.ycoord), end=' ')
#     P = Polygon(S)
#     assert P.signed_area_x2 == 3198528000
