from physdes.router.global_router import GlobalRouter
from physdes.router.routing_visualizer import (
    save_routing_tree_svg,
    visualize_routing_tree_svg,
)
from tests.conftest import generate_random_points

source, terminals = generate_random_points()


def test_route_with_delay_constraint_4() -> None:
    """Test routing with delay constraints."""
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.4)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6379
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_6() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.6)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6379
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_8() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.8)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha8.svg")

    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6928
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_9() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.9)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6379
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_9998() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.9998)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha9998.svg")

    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6379
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_10() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.0)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha10.svg")

    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6379
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_12() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.2)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha12.svg")

    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 5867
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3129


def test_route_with_delay_constraint_14() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.4)

    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha14.svg")

    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 5854
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3871


def test_route_with_delay_constraint_16() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.6)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 5854
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3871


def test_route_with_delay_constraint_18() -> None:
    """Test routing with delay constraints."""
    # source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.8)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 5854
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3871
