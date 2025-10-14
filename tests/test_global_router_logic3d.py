from physdes.point import Point
from physdes.router.global_router3d import GlobalRouter3d


def test_global_router3d_init():
    source = Point(Point(0, 0), 0)
    terminals = [Point(Point(10, 0), 0), Point(Point(1, 0), 0), Point(Point(5, 0), 0)]
    router = GlobalRouter3d(source, terminals)
    assert router.terminal_positions == [
        Point(Point(10, 0), 0),
        Point(Point(5, 0), 0),
        Point(Point(1, 0), 0),
    ]


def test_route_simple():
    source = Point(Point(0, 0), 0)
    terminals = [Point(Point(1, 1), 1), Point(Point(2, 2), 2)]
    router = GlobalRouter3d(source, terminals)
    router.route_simple()
    wirelength = router.tree.calculate_wirelength()
    assert wirelength == 9


def test_route_with_steiners():
    source = Point(Point(0, 0), 0)
    terminals = [Point(Point(1, 1), 1), Point(Point(2, 2), 2)]
    router = GlobalRouter3d(source, terminals)
    router.route_with_steiners()
    wirelength = router.tree.calculate_wirelength()
    assert wirelength == 6
