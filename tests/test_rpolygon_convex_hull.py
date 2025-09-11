from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.rpolygon import (
    create_test_rpolygon,
    rpolygon_is_convex,
    rpolygon_is_xmonotone,
    rpolygon_is_ymonotone,
    rpolygon_make_convex_hull,
)


def test_rpolygon_make_convex_hull():
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(100)]
    S = create_test_rpolygon([Point(xcoord, ycoord) for xcoord, ycoord in coords])
    assert not rpolygon_is_xmonotone(S)
    assert not rpolygon_is_ymonotone(S)

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

    C = rpolygon_make_convex_hull(S, False)
    print('  <polygon points="', end=" ")
    p0 = C[-1]
    for p1 in C:
        print("{},{} {},{}".format(p0.xcoord, p0.ycoord, p1.xcoord, p0.ycoord), end=" ")
        p0 = p1
    print('"')
    print('  fill="#D088C0" stroke="black" opacity="0.3"/>')

    print("</svg>")
    assert rpolygon_is_convex(C)
