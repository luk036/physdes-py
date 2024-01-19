from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.rpolygon import (
    RPolygon,
    create_test_rpolygon,
    create_xmono_rpolygon,
    create_ymono_rpolygon,
    point_in_rpolygon,
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
    P = RPolygon(S)
    assert not is_cw
    assert P.signed_area == 45
    Q = RPolygon(S)
    Q += Vector2(4, 5)
    Q -= Vector2(4, 5)
    assert Q == P


def test_RPolygon2():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(20)]
    S, is_cw = create_ymono_rpolygon(
        [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    )
    for p1, p2 in zip(S, S[1:] + [S[0]]):
        print("{},{} {},{}".format(p1.xcoord, p1.ycoord, p2.xcoord, p1.ycoord), end=" ")
    P = RPolygon(S)
    assert is_cw
    assert P.signed_area == -1871424


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
    for p1, p2 in zip(S, S[1:] + [S[0]]):
        print("{},{} {},{}".format(p1.xcoord, p1.ycoord, p2.xcoord, p1.ycoord), end=" ")
    P = RPolygon(S)
    assert not is_anticw
    assert P.signed_area == -53


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
    P = RPolygon(S)
    assert is_anticw
    assert P.signed_area == 2001024


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
    P = RPolygon(S)
    assert P.signed_area == -2176416
    assert point_in_rpolygon(S, Point(qx, qy))
