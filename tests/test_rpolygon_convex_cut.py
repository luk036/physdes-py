from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.rpolygon import (
    RPolygon,
    create_test_rpolygon,
    rpolygon_is_convex,
    rpolygon_is_xmonotone,
    rpolygon_is_ymonotone,
)
from physdes.rpolygon_cut import rpolygon_cut_convex
from tests.conftest import get_circle_svg_elements, get_polygon_svg_elements


def test_rpolygon_convex_cut() -> None:
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(5)]
    S = create_test_rpolygon([Point(xcoord, ycoord) for xcoord, ycoord in coords])
    assert not rpolygon_is_xmonotone(S) or not rpolygon_is_ymonotone(S)

    P = RPolygon.from_pointset(S)
    is_anticlockwise = P.is_anticlockwise()

    svg_parts = []
    svg_parts.append('<svg viewBox="0 0 2187 2048" xmlns="http://www.w3.org/2000/svg">')
    svg_parts.append(get_polygon_svg_elements(S, fill_color="#88C0D0", stroke_color="black", opacity="0.5"))
    svg_parts.append(get_circle_svg_elements(S, circle_radius=10))

    L = rpolygon_cut_convex(S, is_anticlockwise)
    for C in L:
        svg_parts.append(get_polygon_svg_elements(C, fill_color="#D088C0", stroke_color="black", opacity="0.3"))
        # for p in C:
        #     svg_parts.append(f'  <circle cx="{p.xcoord}" cy="{p.ycoord}" r="10" fill="red"/>')

    svg_parts.append("</svg>")
    print("\n".join(svg_parts))
    for C in L:
        assert rpolygon_is_convex(C)
