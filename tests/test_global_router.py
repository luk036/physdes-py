from physdes.router.routing_tree import visualize_routing_tree_svg, save_routing_tree_svg
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
    source = Point(3, 1)
    terminals = [Point(2, 4), Point(4, 6), Point(7, 2), Point(6, 3)]
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, "example_route_with_steiner.svg")
