from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.interval import Interval
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_tree import (
    save_routing_tree_svg,
    visualize_routing_tree_svg,
)


def test_route_with_steiner_and_keepout():
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

    # Save to file
    save_routing_tree_svg(
        router.tree, keepouts, filename="example_route_with_steiner_and_keepout.svg"
    )


def test_route_with_keepouts():
    # Create a sample routing tree (using the provided class)
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [hgen.pop() for _ in range(7)]
    terminals = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    src_coord = hgen.pop()
    source = Point(src_coord[0], src_coord[1])
    # source = Point(300, 100)
    # terminals = [Point(200, 400), Point(400, 600), Point(700, 200), Point(600, 300)]
    keepouts = [
        Point(Interval(1600, 1900), Interval(1000, 1500)),
        Point(Interval(500, 800), Interval(600, 900)),
    ]

    router = GlobalRouter(source, terminals, keepouts)
    router.route_with_constraints(1.0)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(
        router.tree, keepouts, width=1000, height=1000
    )
    print(svg_output)

    # Save to file
    save_routing_tree_svg(
        router.tree, keepouts, filename="example_route_with_keepouts.svg"
    )
