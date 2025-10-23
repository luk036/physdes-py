from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.interval import Interval
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_tree import (
    save_routing_tree_svg,
    visualize_routing_tree_svg,
)


def test_route_with_steiner_and_keepouts():
    # Create a sample routing tree (using the provided class)
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [hgen.pop() for _ in range(7)]
    terminals = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    src_coord = hgen.pop()
    source = Point(src_coord[0], src_coord[1])
    keepouts = [
        Point(Interval(1600, 1900), Interval(1000, 1500)),
        Point(Interval(500, 800), Interval(600, 900)),
    ]
    # source = Point(300, 100)
    # terminals = [Point(200, 400), Point(400, 600), Point(700, 200), Point(600, 300)]
    router = GlobalRouter(source, terminals, keepouts)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(
        router.tree, keepouts, width=1000, height=1000
    )
    print(svg_output)


def test_route_with_keepouts_increases_wirelength():
    """Test that adding keepouts increases the wirelength of the routing tree."""
    source = Point(0, 0)
    terminals = [Point(10, 10), Point(20, 20)]

    # Route without keepouts
    router_no_keepouts = GlobalRouter(source, terminals)
    router_no_keepouts.route_with_steiners()
    wirelength_no_keepouts = router_no_keepouts.tree.calculate_wirelength()

    # Route with keepouts that obstruct the direct path
    keepouts = [Point(Interval(5, 15), Interval(5, 15))]
    router_with_keepouts = GlobalRouter(source, terminals, keepouts)
    router_with_keepouts.route_with_steiners()
    wirelength_with_keepouts = router_with_keepouts.tree.calculate_wirelength()

    assert wirelength_with_keepouts > wirelength_no_keepouts
