from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.rpolygon import (
    create_test_rpolygon,
    rpolygon_is_convex,
    rpolygon_is_xmonotone,
    rpolygon_is_ymonotone,
    rpolygon_make_convex_hull,
)
from tests.conftest import get_circle_svg_elements, get_polygon_svg_elements


def test_rpolygon_make_convex_hull() -> None:
    hgen = Halton([3, 2], [7, 11])
    coords = [hgen.pop() for _ in range(100)]
    S = create_test_rpolygon([Point(xcoord, ycoord) for xcoord, ycoord in coords])
    assert not rpolygon_is_xmonotone(S)
    assert not rpolygon_is_ymonotone(S)

    svg_parts = []
    svg_parts.append('<svg viewBox="0 0 2187 2048" xmlns="http://www.w3.org/2000/svg">')
    svg_parts.append(
        get_polygon_svg_elements(
            S, fill_color="#88C0D0", stroke_color="black", opacity="0.5"
        )
    )
    svg_parts.append(get_circle_svg_elements(S, circle_radius=10))

    C = rpolygon_make_convex_hull(S, False)
    svg_parts.append(
        get_polygon_svg_elements(
            C, fill_color="#D088C0", stroke_color="black", opacity="0.3"
        )
    )
    svg_parts.append("</svg>")
    print("\n".join(svg_parts))
    assert rpolygon_is_convex(C)
