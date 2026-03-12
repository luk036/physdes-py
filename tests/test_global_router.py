from physdes.router.global_router import GlobalRouter
from physdes.router.routing_visualizer import (
    save_routing_tree_svg,
    visualize_routing_tree_svg,
)
from tests.conftest import generate_random_points, generate_special_points


def test_route_with_steiner() -> None:
    """Test routing with Steiner points."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="example_route_with_steiner.svg")


def test_route_with_delay_constraint() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.0)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="example_route_with_delay_constraint.svg")


def test_route_with_steiner_special() -> None:
    """Test routing with Steiner points for a special case."""
    source, terminals = generate_special_points()
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="example_route_with_steiner_special.svg")


def test_route_with_constraints_special() -> None:
    """Test routing with constraints for a special case."""
    source, terminals = generate_special_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.0)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="neg_specical10.svg")
