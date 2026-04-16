from physdes.router.global_router import GlobalRouter
from physdes.router.routing_visualizer import (
    save_routing_tree_svg,
    visualize_routing_tree_svg,
)
from tests.conftest import generate_random_points


def test_route_with_delay_constraint_4() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.4)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 14852
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_6() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.6)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 14090
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_8() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.8)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 10960
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_9() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.9)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 10628
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_99() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.99)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 8599
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_999() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.999)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 8599
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_9994() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.9994)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 8599
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_9996() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.9996)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 8599
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_9998() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.9998)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 8599
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103
    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha9998.svg")


def test_route_with_delay_constraint_99985() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.99985)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6379
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_9999() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(0.9999)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6379
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103


def test_route_with_delay_constraint_10() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.0)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 6379
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3103
    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha10.svg")


def test_route_with_delay_constraint_12() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.2)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 5867
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3129
    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha12.svg")


def test_route_with_delay_constraint_14() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.4)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 5854
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3871
    # Generate and print SVG
    svg_output = visualize_routing_tree_svg(router.tree, width=1000, height=1000)
    print(svg_output)

    # Save to file
    save_routing_tree_svg(router.tree, filename="alpha14.svg")


def test_route_with_delay_constraint_16() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.6)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 5854
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3871


def test_route_with_delay_constraint_18() -> None:
    """Test routing with delay constraints."""
    source, terminals = generate_random_points()
    router = GlobalRouter(source, terminals)
    router.route_with_constraints(1.8)
    wirelength = router.tree.calculate_total_wirelength()
    assert wirelength == 5854
    wirelength = router.tree.calculate_worst_wirelength()
    assert wirelength == 3871
