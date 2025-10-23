from random import randint

from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_tree import (
    visualize_routing_tree3d_svg,
    save_routing_tree3d_svg,
)


def test_route3d_with_steiner():
    scale_z = 100
    # Create a sample routing tree (using the provided class)
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [hgen.pop() for _ in range(7)]
    terminals = [
        Point(Point(xcoord, randint(0, 3) * scale_z), ycoord)
        for xcoord, ycoord in coords
    ]
    src_coord = hgen.pop()
    source = Point(Point(src_coord[0], randint(0, 3) * scale_z), src_coord[1])
    # source = Point(Point(30, 1), 10)
    # terminals = [Point(Point(20, 4), 40), Point(Point(40, 6), 60), Point(Point(70, 2), 20), Point(Point(60, 3), 30)]
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree3d_svg(
        router.tree, None, scale_z, width=1000, height=1000
    )
    print(svg_output)

    # Save to file
    save_routing_tree3d_svg(
        router.tree, None, scale_z, "example_route3d_with_steiner.svg"
    )


def test_route3d_with_constraints():
    scale_z = 100
    # Create a sample routing tree (using the provided class)
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [hgen.pop() for _ in range(7)]
    terminals = [
        Point(Point(xcoord, randint(0, 3) * scale_z), ycoord)
        for xcoord, ycoord in coords
    ]
    src_coord = hgen.pop()
    source = Point(Point(src_coord[0], randint(0, 3) * scale_z), src_coord[1])
    # source = Point(Point(30, 1), 10)
    # terminals = [Point(Point(20, 4), 40), Point(Point(40, 6), 60), Point(Point(70, 2), 20), Point(Point(60, 3), 30)]
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.0)

    # Generate and print SVG
    svg_output = visualize_routing_tree3d_svg(
        router.tree, None, scale_z, width=1000, height=1000
    )
    print(svg_output)

    # Save to file
    save_routing_tree3d_svg(
        router.tree, None, scale_z, "example_route3d_with_constraint.svg"
    )
