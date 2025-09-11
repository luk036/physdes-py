import pytest
from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.polygon import Polygon
from physdes.rpolygon import (
    RPolygon,
    create_test_rpolygon,
    create_xmono_rpolygon,
    create_ymono_rpolygon,
    point_in_rpolygon,
    rpolygon_is_convex,
    rpolygon_is_monotone,
    rpolygon_is_xmonotone,
    rpolygon_is_ymonotone,
    rpolygon_make_xmonotone_hull,
    rpolygon_make_ymonotone_hull,
)
from physdes.vector2 import Vector2


def test_RPolygon():
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
        (-3, -4),
        (1, 4),
    ]
    S, is_cw = create_ymono_rpolygon(
        [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    )
    for p1, p2 in zip(S, S[1:] + [S[0]]):
        print(f"{p1.xcoord}, {p1.ycoord} {p2.xcoord}, {p1.ycoord})", end=" ")
    P = RPolygon.from_pointset(S)
    assert not is_cw
    assert P.is_anticlockwise()
    G = P.to_polygon()
    assert P.signed_area * 2 == G.signed_area_x2
    assert P.signed_area > 0

    Q = RPolygon.from_pointset(S)
    Q += Vector2(4, 5)
    Q -= Vector2(4, 5)
    assert Q == P


def test_RPolygon2():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(40)]
    S, is_cw = create_ymono_rpolygon(
        [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    )
    assert rpolygon_is_ymonotone(S)
    assert not rpolygon_is_xmonotone(S)
    assert not rpolygon_is_convex(S)

    for p1, p2 in zip(S, S[1:] + [S[0]]):
        print("{},{} {},{}".format(p1.xcoord, p1.ycoord, p2.xcoord, p1.ycoord), end=" ")
    P = RPolygon.from_pointset(S)
    G = P.to_polygon()
    assert P.signed_area * 2 == G.signed_area_x2
    assert P.signed_area < 0

    assert is_cw
    assert not P.is_anticlockwise()


def test_RPolygon3():
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
        (-3, -4),
        (1, 4),
    ]
    S, is_anticw = create_xmono_rpolygon(
        [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    )
    assert rpolygon_is_xmonotone(S)
    assert not rpolygon_is_ymonotone(S)
    assert not rpolygon_is_convex(S)

    for p1, p2 in zip(S, S[1:] + [S[0]]):
        print("{},{} {},{}".format(p1.xcoord, p1.ycoord, p2.xcoord, p1.ycoord), end=" ")
    P = RPolygon.from_pointset(S)
    assert is_anticw
    assert P.is_anticlockwise()


def test_RPolygon4():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(20)]
    S, is_anticw = create_xmono_rpolygon(
        [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    )
    p0 = S[-1]
    for p1 in S:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    P = RPolygon.from_pointset(S)
    assert not is_anticw
    assert not P.is_anticlockwise()


def test_RPolygon5():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(50)]
    S = create_test_rpolygon([Point(xcoord, ycoord) for xcoord, ycoord in coords])
    print('<svg viewBox="0 0 2187 2048" xmlns="http://www.w3.org/2000/svg">')
    print('  <polygon points="', end=" ")
    p0 = S[-1]
    for p1 in S:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    print('"')
    print('  fill="#88C0D0" stroke="black" />')
    for p in S:
        print('  <circle cx="{}" cy="{}" r="10" />'.format(p.xcoord, p.ycoord))
    qx, qy = hgen.pop()
    print('  <circle cx="{}" cy="{}" r="10" fill="#BF616A" />'.format(qx, qy))
    print("</svg>")
    P = RPolygon.from_pointset(S)
    assert P.signed_area == -2176416
    assert not P.is_anticlockwise()
    assert point_in_rpolygon(S, Point(qx, qy))


def test_to_polygon():
    coords = [(0, 0), (10, 10), (5, 5)]
    point_set = [Point(x, y) for x, y in coords]
    r_poly = RPolygon.from_pointset(point_set)
    poly = r_poly.to_polygon()

    expected_coords = [(0, 0), (10, 0), (10, 10), (5, 10), (5, 5), (0, 5)]
    expected_point_set = [Point(x, y) for x, y in expected_coords]
    expected_poly = Polygon.from_pointset(expected_point_set)

    assert poly == expected_poly


def test_rpolygon_eq_different_type():
    coords = [(0, 0), (0, 1), (1, 1), (1, 0)]
    points = [Point(x, y) for x, y in coords]
    rpolygon = RPolygon.from_pointset(points)
    assert (rpolygon == 1) is False


def test_is_anticlockwise_less_than_2_points():
    with pytest.raises(ValueError):
        coords = [(0, 0)]
        points = [Point(x, y) for x, y in coords]
        rpolygon = RPolygon.from_pointset(points)
        rpolygon.is_anticlockwise()


def test_to_polygon_non_rectilinear():
    coords = [(0, 0), (1, 1), (2, 0)]
    points = [Point(x, y) for x, y in coords]
    rpolygon = RPolygon.from_pointset(points)
    polygon = rpolygon.to_polygon()
    # The expected polygon should have extra points to make it rectilinear
    expected_coords = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0)]
    expected_points = [Point(x, y) for x, y in expected_coords]
    expected_polygon = Polygon.from_pointset(expected_points)
    assert polygon._vecs == expected_polygon._vecs


def test_create_test_rpolygon_vec_lt_0():
    coords = [(0, 10), (10, 0), (5, 6)]
    points = [Point(x, y) for x, y in coords]
    create_test_rpolygon(points)


def test_rpolygon_is_monotone_small_list():
    coords = [(0, 0), (1, 1)]
    points = [Point(x, y) for x, y in coords]
    assert rpolygon_is_monotone(points, lambda p: (p.xcoord, p.ycoord)) is True


def test_rpolygon_is_monotone_break():
    coords = [(0, 0), (3, 1), (1, 2), (2, 3)]
    points = [Point(x, y) for x, y in coords]
    assert rpolygon_is_monotone(points, lambda p: (p.xcoord, p.ycoord)) is False


def test_rpolygon_make_xmonotone_hull():
    coords = [
        (-10, 50),
        (-40, 40),
        (-60, -40),
        (-20, -50),
        (90, -2),
        (60, 10),
        (50, 20),
        (10, 40),
        (80, 60),
    ]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    assert not rpolygon_is_xmonotone(S)
    print('<svg viewBox="-100 -100 200 200" xmlns="http://www.w3.org/2000/svg">')

    print('  <polygon points="', end=" ")
    p0 = S[-1]
    for p1 in S:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    print('"')
    print('  fill="#88C0D0" stroke="black" opacity="0.5"/>')
    for p in S:
        print('  <circle cx="{}" cy="{}" r="1" />'.format(p.xcoord, p.ycoord))

    C = rpolygon_make_xmonotone_hull(S, True)
    print('  <polygon points="', end=" ")
    p0 = C[-1]
    for p1 in C:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    print('"')
    print('  fill="#D088C0" stroke="black" opacity="0.3"/>')

    print("</svg>")

    assert rpolygon_is_xmonotone(C)


def test_rpolygon_make_ymonotone_hull():
    coords = [
        (90, -10),
        (40, -40),
        (-40, -60),
        (-50, -20),
        (-20, 90),
        (10, 60),
        (20, 50),
        (30, 10),
        (60, 80),
    ]
    S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    assert not rpolygon_is_ymonotone(S)

    print('<svg viewBox="-100 -100 200 200" xmlns="http://www.w3.org/2000/svg">')

    print('  <polygon points="', end=" ")
    p0 = S[-1]
    for p1 in S:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    print('"')
    print('  fill="#88C0D0" stroke="black" opacity="0.5"/>')
    for p in S:
        print('  <circle cx="{}" cy="{}" r="1" />'.format(p.xcoord, p.ycoord))

    C = rpolygon_make_ymonotone_hull(S, False)
    print('  <polygon points="', end=" ")
    p0 = C[-1]
    for p1 in C:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    print('"')
    print('  fill="#D088C0" stroke="black" opacity="0.3"/>')

    print("</svg>")

    assert rpolygon_is_ymonotone(C)


def test_rpolygon_make_convex_hull():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(100)]
    S, is_anticlockwise = create_xmono_rpolygon(
        [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    )
    assert rpolygon_is_xmonotone(S)
    assert not is_anticlockwise

    print('<svg viewBox="0 0 2187 2048" xmlns="http://www.w3.org/2000/svg">')

    print('  <polygon points="', end=" ")
    p0 = S[-1]
    for p1 in S:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    print('"')
    print('  fill="#88C0D0" stroke="black" opacity="0.5"/>')
    for p in S:
        print('  <circle cx="{}" cy="{}" r="10" />'.format(p.xcoord, p.ycoord))

    C = rpolygon_make_ymonotone_hull(S, is_anticlockwise)
    print('  <polygon points="', end=" ")
    p0 = C[-1]
    for p1 in C:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    print('"')
    print('  fill="#D088C0" stroke="black" opacity="0.3"/>')

    print("</svg>")
    assert rpolygon_is_convex(C)
