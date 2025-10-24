from physdes.router.global_router import GlobalRouter
from physdes.router.routing_tree import (
    visualize_routing_tree3d_svg,
    # save_routing_tree3d_svg,
)
from tests.conftest import generate_3d_random_points


def test_route3d_with_steiner():
    """Test 3D routing with Steiner points."""
    source, terminals, scale_z = generate_3d_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree3d_svg(
        router.tree, None, scale_z, width=1000, height=1000
    )
    print(svg_output)

    # Save to file
    # save_routing_tree3d_svg(
    #     router.tree, None, scale_z, "example_route3d_with_steiner.svg"
    # )


def test_route3d_with_constraints():
    """Test 3D routing with constraints."""
    source, terminals, scale_z = generate_3d_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.0)

    # Generate and print SVG
    svg_output = visualize_routing_tree3d_svg(
        router.tree, None, scale_z, width=1000, height=1000
    )
    print(svg_output)

    # Save to file
    # save_routing_tree3d_svg(
    #     router.tree, None, scale_z, "example_route3d_with_constraint.svg"
    # )
