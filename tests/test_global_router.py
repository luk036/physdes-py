from lds_gen.ilds import Halton

from physdes.router.routing_tree import (
    visualize_routing_tree_svg,
    save_routing_tree_svg,
)
from physdes.point import Point
from physdes.router.global_router import GlobalRouter


# def test_route_simple():
#     # Create a sample routing tree (using the provided class)
#     source = Point(3, 1)
#     terminals = [Point(2, 8), Point(3, 6), Point(5, 2)]
#     router = GlobalRouter(source, terminals)
#     router.route_simple()

#     # Generate and print SVG
#     svg_output = visualize_routing_tree_svg(router.tree)
#     print(svg_output)

#     # Save to file
#     save_routing_tree_svg(router.tree, "example_route_simple.svg")


def test_route_with_steiner():
    # Create a sample routing tree (using the provided class)
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [hgen.pop() for _ in range(7)]
    terminals = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    src_coord = hgen.pop()
    source = Point(src_coord[0], src_coord[1])
    # source = Point(300, 100)
    # terminals = [Point(200, 400), Point(400, 600), Point(700, 200), Point(600, 300)]
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, "example_route_with_steiner.svg")

def test_route_with_constraints():
    # Create a sample routing tree (using the provided class)
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [hgen.pop() for _ in range(7)]
    terminals = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    src_coord = hgen.pop()
    source = Point(src_coord[0], src_coord[1])
    # source = Point(300, 100)
    # terminals = [Point(200, 400), Point(400, 600), Point(700, 200), Point(600, 300)]
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.9)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, "example_route_with_constraint.svg")
