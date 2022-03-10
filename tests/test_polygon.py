from physdes.halton_int import halton
from physdes.point import Point
from physdes.polygon import (
    create_test_polygon,
    create_xmono_polygon,
    create_ymono_polygon,
    point_in_polygon,
    Polygon,
)


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
    S = [Point(x, y) for x, y in coords]
    S = create_test_polygon(S)
    for p in S:
        print("{},{}".format(p.x, p.y), end=" ")
    P = Polygon(S)
    assert P.signed_area_x2() == 110


def test_polygon2():
    hgen = halton([2, 3], [11, 7])
    coords = [hgen() for _ in range(20)]
    S = [Point(x, y) for x, y in coords]
    S = create_ymono_polygon(S)
    P = Polygon(S)
    assert P.signed_area_x2() == 4074624


def test_polygon3():
    hgen = halton([2, 3], [11, 7])
    coords = [hgen() for _ in range(20)]
    S = [Point(x, y) for x, y in coords]
    S = create_xmono_polygon(S)
    P = Polygon(S)
    assert P.signed_area_x2() == 3862080


def test_polygon4():
    hgen = halton([3, 2], [7, 11])
    coords = [hgen() for _ in range(50)]
    S = create_test_polygon([Point(x, y) for x, y in coords])
    print('<svg viewBox="0 0 2187 2048" xmlns="http://www.w3.org/2000/svg">')
    print('  <polygon points="', end=" ")
    for p in S:
        print("{},{}".format(p.x, p.y), end=" ")
    print('"')
    print('  fill="#88C0D0" stroke="black" />')
    for p in S:
        print('  <circle cx="{}" cy="{}" r="10" />'.format(p.x, p.y))
    qx, qy = hgen()
    print('  <circle cx="{}" cy="{}" r="10" fill="#BF616A" />'.format(qx, qy))
    print("</svg>")
    P = Polygon(S)
    assert P.signed_area_x2() == -4449600
    assert point_in_polygon(S, Point(qx, qy))


# def test_polygon3():
#     hgen = halton([2, 3], [11, 7])
#     coords = [hgen() for _ in range(40)]
#     S = [Point(x, y) for x, y in coords]
#     S = create_ymono_polygon(S)
#     for p in S:
#         print("{},{}".format(p.x, p.y), end=' ')
#     P = Polygon(S)
#     assert P.signed_area_x2() == 3198528000
