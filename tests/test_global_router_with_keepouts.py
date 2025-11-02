from physdes.point import Point
from physdes.interval import Interval
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_visualizer import (
    save_routing_tree_svg,
    visualize_routing_tree_svg,
)
from tests.conftest import generate_random_points


def test_route_with_steiner_and_keepouts():
    """Test routing with Steiner points and keepouts."""
    source, terminals = generate_random_points()
    keepouts = [
        Point(Interval(1600, 1900), Interval(1000, 1500)),
        Point(Interval(500, 800), Interval(600, 900)),
    ]
    router = GlobalRouter(source, terminals, keepouts)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(
        router.tree, keepouts, width=1000, height=1000
    )
    print(svg_output)

    # Save to file
    save_routing_tree_svg(
        router.tree, keepouts, filename="example_route_with_steiner_and_keepouts.svg"
    )


def test_route_with_keepouts():
    """Test routing with keepouts."""
    source, terminals = generate_random_points()
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
