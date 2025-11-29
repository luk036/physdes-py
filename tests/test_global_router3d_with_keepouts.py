from physdes.point import Point
from physdes.interval import Interval
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_visualizer import (
    visualize_routing_tree3d_svg,
    save_routing_tree3d_svg,
)
from tests.conftest import generate_3d_random_points_with_index
from icecream import ic
from physdes.router.routing_tree import NodeType


def test_route3d_with_steiner_and_keepouts() -> None:
    """Test 3D routing with Steiner points and keepouts."""
    source, terminals, scale_z = generate_3d_random_points_with_index()
    keepouts = [
        Point(Point(Interval(600, 900), Interval(-1000, 1000)), Interval(0, 500)),
        Point(Point(Interval(-500, -200), Interval(-1000, 1000)), Interval(-400, -100)),
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


def test_route3d_with_constraints_and_keepouts() -> None:
    """Test 3D routing with constraints and keepouts."""
    source, terminals, scale_z = generate_3d_random_points_with_index()
    keepouts = [
        Point(Point(Interval(600, 900), Interval(-1000, 1000)), Interval(0, 500)),
        Point(Point(Interval(-500, -200), Interval(-1000, 1000)), Interval(-400, -100)),
    ]
    ic(terminals)
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
    ic(keepouts)
    all_nodes = list(router.tree.nodes.values())
    for node in all_nodes:
        if node.type == NodeType.SOURCE:
            node_type = "NODE_TYPES.SOURCE"
        elif node.type == NodeType.STEINER:
            node_type = "NODE_TYPES.STEINER"
        elif node.type == NodeType.TERMINAL:
            node_type = "NODE_TYPES.TERMINAL"
        else:
            node_type = "NODE_TYPES.UNKNOWN"

        print(
            f"{{ id: '{node.id}', type: {node_type}, position: {{x: {node.pt.xcoord.xcoord}, y: {node.pt.xcoord.ycoord}, z: {node.pt.ycoord}}} }},"
        )
        # { id: 'S', type: NODE_TYPES.SOURCE, position: { x: 27, y: 0, z: 1728 } },

    def draw_connections(node):
        for child in node.children:
            print(
                f"{{ from: '{node.id}', to: '{child.id}', type: CONNECTION_TYPES.ROUTED }},"
            )

        for child in node.children:
            draw_connections(child)

    # { from: 'S', to: 'T3', type: CONNECTION_TYPES.DIRECT },

    # Draw all connections starting from source
    draw_connections(router.tree.source)

    # assert False
