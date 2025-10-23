from physdes.point import Point
from physdes.interval import Interval
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_tree import (
    visualize_routing_tree3d_svg,
    save_routing_tree3d_svg,
)
from tests.conftest import generate_3d_random_points_with_index


def test_route3d_with_steiner_and_keepouts():
    """Test 3D routing with Steiner points and keepouts."""
    source, terminals, scale_z = generate_3d_random_points_with_index()
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

    # Save to file
    save_routing_tree3d_svg(
        router.tree, keepouts, scale_z, "example_route3d_with_steiner_and_keepouts.svg"
    )


def test_route3d_with_constraints_and_keepouts():
    """Test 3D routing with constraints and keepouts."""
    source, terminals, scale_z = generate_3d_random_points_with_index()
    keepouts = [
        Point(Point(Interval(1600, 1900), Interval(-1000, 1000)), Interval(1000, 1500)),
        Point(Point(Interval(500, 800), Interval(-1000, 1000)), Interval(600, 900)),
    ]

    router = GlobalRouter(source, terminals, keepouts)
    router.route_with_constraints(1.0)

    # Generate and print SVG
    svg_output = visualize_routing_tree3d_svg(
        router.tree, keepouts, scale_z, width=1000, height=1000
    )
    print(svg_output)

    # Save to file
    save_routing_tree3d_svg(
        router.tree,
        keepouts,
        scale_z,
        "example_route3d_with_constraint_and_keepouts.svg",
    )
