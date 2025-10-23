from physdes.point import Point
from physdes.router.global_router import GlobalRouter
from tests.conftest import (
    generate_2d_init_points,
    generate_3d_init_points,
    generate_2d_simple_points,
    generate_3d_simple_points,
)


def test_global_router_init():
    source, terminals = generate_2d_init_points()
    router = GlobalRouter(source, terminals)
    assert router.terminal_positions == [Point(10, 0), Point(5, 0), Point(1, 0)]


def test_route_simple():
    source, terminals = generate_2d_simple_points()
    router = GlobalRouter(source, terminals)
    router.route_simple()
    wirelength = router.tree.calculate_wirelength()
    assert wirelength == 6.0


def test_route_with_steiners():
    source, terminals = generate_2d_simple_points()
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()
    wirelength = router.tree.calculate_wirelength()
    assert wirelength == 4.0


def test_global_router3d_init():
    source, terminals = generate_3d_init_points()
    router = GlobalRouter(source, terminals)
    assert router.terminal_positions == [
        Point(Point(10, 0), 0),
        Point(Point(5, 0), 0),
        Point(Point(1, 0), 0),
    ]


def test_route3d_simple():
    source, terminals = generate_3d_simple_points()
    router = GlobalRouter(source, terminals)
    router.route_simple()
    wirelength = router.tree.calculate_wirelength()
    assert wirelength == 9


def test_route3d_with_steiners():
    source, terminals = generate_3d_simple_points()
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()
    wirelength = router.tree.calculate_wirelength()
    assert wirelength == 6
