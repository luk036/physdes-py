from physdes.interval import Interval
from physdes.point import Point
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_tree import NodeType
from physdes.router.routing_visualizer import (
    save_routing_tree3d_svg,
    visualize_routing_tree3d_svg,
)
from tests.conftest import generate_3d_random_points_with_index


def test_route3d_with_steiner_and_keepouts() -> None:
    """Test 3D routing with Steiner points and keepouts."""
    source, terminals, scale_z = generate_3d_random_points_with_index()
    keepouts = [
        Point(Point(Interval(600, 900), Interval(-1000, 1000)), Interval(0, 500)),
        Point(Point(Interval(-500, -200), Interval(-1000, 1000)), Interval(-400, -100)),
    ]

    router = GlobalRouter(source, terminals, keepouts)
    router.route_with_steiners()

    svg_output = visualize_routing_tree3d_svg(router.tree, keepouts, scale_z, width=1000, height=1000)
    assert svg_output.startswith("<svg")

    save_routing_tree3d_svg(router.tree, keepouts, scale_z, "example_route3d_with_steiner_and_keepouts.svg")

    assert len(router.tree.get_all_terminals()) == len(terminals)


def test_route3d_with_constraints_and_keepouts() -> None:
    """Test 3D routing with constraints and keepouts."""
    source, terminals, scale_z = generate_3d_random_points_with_index()
    keepouts = [
        Point(Point(Interval(600, 900), Interval(-1000, 1000)), Interval(0, 500)),
        Point(Point(Interval(-500, -200), Interval(-1000, 1000)), Interval(-400, -100)),
    ]

    router = GlobalRouter(source, terminals, keepouts)
    router.route_with_constraints(1.0)

    svg_output = visualize_routing_tree3d_svg(router.tree, keepouts, scale_z, width=1000, height=1000)
    assert svg_output.startswith("<svg")

    save_routing_tree3d_svg(
        router.tree,
        keepouts,
        scale_z,
        "example_route3d_with_constraint_and_keepouts.svg",
    )

    assert len(router.tree.get_all_terminals()) == len(terminals)
    assert all(isinstance(node.type, NodeType) for node in router.tree.nodes.values())
    assert all(child.parent is node for node in router.tree.nodes.values() for child in node.children)
