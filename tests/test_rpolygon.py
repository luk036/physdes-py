from physdes.halton_int import halton
from physdes.point import point
from physdes.rpolygon import (
    create_test_rpolygon,
    create_xmono_rpolygon,
    create_ymono_rpolygon,
    point_in_rpolygon,
    rpolygon,
)


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
    S, is_anticw = create_ymono_rpolygon([point(x, y) for x, y in coords])
    for p1, p2 in zip(S, S[1:] + [S[0]]):
        print("{},{} {},{}".format(p1.x, p1.y, p2.x, p1.y), end=" ")
    P = rpolygon(S)
    assert is_anticw
    assert P.signed_area() == 45


def test_RPolygon2():
    hgen = halton([3, 2], [7, 11])
    coords = [hgen() for _ in range(20)]
    S, is_anticw = create_ymono_rpolygon([point(x, y) for x, y in coords])
    for p1, p2 in zip(S, S[1:] + [S[0]]):
        print("{},{} {},{}".format(p1.x, p1.y, p2.x, p1.y), end=" ")
    P = rpolygon(S)
    assert not is_anticw
    assert P.signed_area() == -1871424


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
    S, is_anticw = create_xmono_rpolygon([point(x, y) for x, y in coords])
    for p1, p2 in zip(S, S[1:] + [S[0]]):
        print("{},{} {},{}".format(p1.x, p1.y, p2.x, p1.y), end=" ")
    P = rpolygon(S)
    assert not is_anticw
    assert P.signed_area() == -53


def test_RPolygon4():
    hgen = halton([3, 2], [7, 11])
    coords = [hgen() for _ in range(20)]
    S, is_anticw = create_xmono_rpolygon([point(x, y) for x, y in coords])
    p0 = S[-1]
    for p1 in S:
        print("{},{} {},{}".format(p0.x, p0.y, p1.x, p0.y), end=" ")
        p0 = p1
    P = rpolygon(S)
    assert is_anticw
    assert P.signed_area() == 2001024


def test_RPolygon5():
    hgen = halton([3, 2], [7, 11])
    coords = [hgen() for _ in range(50)]
    S = create_test_rpolygon([point(x, y) for x, y in coords])
    # for p1, p2 in zip(S, S[1:] + [S[0]]):
    #     print("{},{} {},{}".format(p1.x, p1.y, p2.x, p1.y), end=' ')
    print('<svg viewBox="0 0 2187 2048" xmlns="http://www.w3.org/2000/svg">')
    print('  <polygon points="', end=" ")
    p0 = S[-1]
    for p1 in S:
        print("{},{} {},{}".format(p0.x, p0.y, p1.x, p0.y), end=" ")
        p0 = p1
    print('"')
    print('  fill="#88C0D0" stroke="black" />')
    for p in S:
        print('  <circle cx="{}" cy="{}" r="10" />'.format(p.x, p.y))
    qx, qy = hgen()
    print('  <circle cx="{}" cy="{}" r="10" fill="#BF616A" />'.format(qx, qy))
    print("</svg>")
    P = rpolygon(S)
    assert P.signed_area() == -2176416
    assert point_in_rpolygon(S, point(qx, qy))
