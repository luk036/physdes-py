from physdes.point import Point
from physdes.router.global_router import GlobalRouter


def test_global_router_init():
    source = Point(0, 0)
    terminals = [Point(10, 0), Point(1, 0), Point(5, 0)]
    router = GlobalRouter(source, terminals)
    assert router.terminal_positions == [Point(10, 0), Point(5, 0), Point(1, 0)]


def test_route_simple():
    source = Point(0, 0)
    terminals = [Point(1, 1), Point(2, 2)]
    router = GlobalRouter(source, terminals)
    router.route_simple()
    wirelength = router.tree.calculate_wirelength()
    assert wirelength == 6.0


def test_route_with_steiners():
    source = Point(0, 0)
    terminals = [Point(1, 1), Point(2, 2)]
    router = GlobalRouter(source, terminals)
    router.route_with_steiners()
    wirelength = router.tree.calculate_wirelength()
    assert wirelength == 4.0
