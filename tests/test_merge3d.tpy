from hypothesis import given
from hypothesis.strategies import integers

from physdes.interval import min_dist
from physdes.manhattan_arc import ManhattanArc
from physdes.manhattan_arc_3d import ManhattanArc3D
from physdes.point import Point


def test_manhattan_arc_3d() -> None:
    r1 = ManhattanArc3D.from_point(Point(Point(4, -5), 5))
    r2 = ManhattanArc3D.from_point(Point(Point(7, -9), 9))
    # v = Vector2(5, 6)

    assert r1 != r2
    # assert (r1 - v) + v == r1
    # assert not overlap(r1, r2)
    assert r1.min_dist_with(r2) == 11
    assert min_dist(r1, r2) == 11
    assert repr(r1) == "ManhattanArc3D(/-1, 9/, /10, 0/, /9, -1/)"


def test_min_dist_3d() -> None:
    pa = Point(Point(8, 3), -2)
    pb = Point(Point(-3, 7), 4)
    dab = pa.min_dist_with(pb)

    ma1 = ManhattanArc.from_point(Point(8, 3))
    ma2 = ManhattanArc.from_point(Point(3, -2))
    ma3 = ManhattanArc.from_point(Point(8, -2))

    mb1 = ManhattanArc.from_point(Point(-3, 7))
    mb2 = ManhattanArc.from_point(Point(7, 4))
    mb3 = ManhattanArc.from_point(Point(-3, 4))

    dmab1 = ma1.min_dist_with(mb1)
    dmab2 = ma2.min_dist_with(mb2)
    dmab3 = ma3.min_dist_with(mb3)
    assert dab == (dmab1 + dmab2 + dmab3) // 2


@given(
    integers(min_value=-100000000000, max_value=1000000000),
    integers(min_value=-100000000000, max_value=1000000000),
    integers(min_value=-100000000000, max_value=1000000000),
    integers(min_value=-100000000000, max_value=1000000000),
    integers(min_value=-100000000000, max_value=1000000000),
    integers(min_value=-100000000000, max_value=1000000000),
)
def test_min_dist_3d_h(a1, b1, c1, a2, b2, c2) -> None:
    pa = Point(Point(a1, b1), c1)
    pb = Point(Point(a2, b2), c2)
    dab = pa.min_dist_with(pb)

    ma1 = ManhattanArc.from_point(Point(a1, b1))
    ma2 = ManhattanArc.from_point(Point(b1, c1))
    ma3 = ManhattanArc.from_point(Point(a1, c1))

    mb1 = ManhattanArc.from_point(Point(a2, b2))
    mb2 = ManhattanArc.from_point(Point(b2, c2))
    mb3 = ManhattanArc.from_point(Point(a2, c2))

    dmab1 = ma1.min_dist_with(mb1)
    dmab2 = ma2.min_dist_with(mb2)
    dmab3 = ma3.min_dist_with(mb3)
    assert dab == (dmab1 + dmab2 + dmab3) // 2
