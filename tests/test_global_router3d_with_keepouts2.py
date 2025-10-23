from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.interval import Interval
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_tree import (
    visualize_routing_tree3d_svg,
)


def test_route3d_with_steiner_and_keepouts():
    scale_z = 100
    # Create a sample routing tree (using the provided class)
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [(hgen.pop(), i) for i in range(7)]
    terminals = [
        Point(Point(xcoord, (i % 4) * scale_z), ycoord)
        for ([xcoord, ycoord], i) in coords
    ]
    src_coord = hgen.pop()
    source = Point(Point(src_coord[0], 0), src_coord[1])
    keepouts = [
        Point(Point(Interval(1600, 1900), Interval(-1000, 1000)), Interval(1000, 1500)),
        Point(Point(Interval(500, 800), Interval(-1000, 1000)), Interval(600, 900)),
    ]

    router = GlobalRouter(source, terminals, keepouts)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree3d_svg(
        router.tree, keepouts, scale_z, width=1000, height=1000
    )
    print(svg_output)


def test_route3d_with_keepouts_increases_wirelength():
    """Test that adding keepouts increases the wirelength of the 3D routing tree."""
    source = Point(Point(0, 0), 0)
    terminals = [Point(Point(10, 0), 10), Point(Point(20, 0), 20)]

    # Route without keepouts
    router_no_keepouts = GlobalRouter(source, terminals)
    router_no_keepouts.route_with_steiners()
    wirelength_no_keepouts = router_no_keepouts.tree.calculate_wirelength()

    # Route with keepouts that obstruct the direct path
    keepouts = [Point(Point(Interval(5, 15), Interval(-1, 1)), Interval(5, 15))]
    router_with_keepouts = GlobalRouter(source, terminals, keepouts)
    router_with_keepouts.route_with_steiners()
    wirelength_with_keepouts = router_with_keepouts.tree.calculate_wirelength()

    assert wirelength_with_keepouts > wirelength_no_keepouts
