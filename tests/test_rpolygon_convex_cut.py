from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.rpolygon import (
    RPolygon,
    create_test_rpolygon,
    rpolygon_cut_convex,
    rpolygon_is_convex,
    rpolygon_is_xmonotone,
    rpolygon_is_ymonotone,
)


def test_rpolygon_convex_cut():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(30)]
    S = create_test_rpolygon([Point(xcoord, ycoord) for xcoord, ycoord in coords])
    assert not rpolygon_is_xmonotone(S) or not rpolygon_is_ymonotone(S)

    P = RPolygon.from_pointset(S)
    is_anticlockwise = P.is_anticlockwise()

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

    L = rpolygon_cut_convex(S, is_anticlockwise)
    for C in L:
        print('  <polygon points="', end=" ")
        p0 = C[-1]
        for p1 in C:
            print(
                "{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord),
                end=" ",
            )
            p0 = p1
        print('"')
        print('  fill="#D088C0" stroke="black" opacity="0.3"/>')
        # for p in C:
        #     print('  <circle cx="{}" cy="{}" r="10" fill="red"/>'.format(p.xcoord, p.ycoord))

    print("</svg>")
    for C in L:
        assert rpolygon_is_convex(C)
