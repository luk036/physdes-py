from physdes.manhattan_arc_3d import ManhattanArc3D
from physdes.point import Point


def test_nearest_point_to():
    p1 = Point(Point(1, 2), 3)
    ma1 = ManhattanArc3D.from_point(p1)
    p2 = Point(Point(4, 5), 6)
    p3 = ma1.nearest_point_to(p2)
    assert p1 == p3
