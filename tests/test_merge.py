from physdes.interval import Interval, min_dist
from physdes.manhattan_arc import ManhattanArc
from physdes.point import Point
from hypothesis import given
from hypothesis.strategies import integers


def test_ManhattanArc() -> None:
    r1 = ManhattanArc.construct(4, 5)
    r2 = ManhattanArc.construct(7, 9)
    # v = Vector2(5, 6)

    assert r1 != r2
    # assert (r1 - v) + v == r1
    # assert not overlap(r1, r2)
    assert r1.min_dist_with(r2) == 7
    assert min_dist(r1, r2) == 7
    assert repr(r1) == "ManhattanArc(-1, 9)"


def test_merge_2() -> None:
    a = ManhattanArc(4 - 5, 4 + 5)
    b = ManhattanArc(7 - 9, 7 + 9)
    assert a == ManhattanArc(4 - 5, 4 + 5)
    r1 = a.enlarge_with(3)
    assert r1 == ManhattanArc(Interval(-4, 2), Interval(6, 12))
    r2 = b.enlarge_with(4)
    assert r2 == ManhattanArc(Interval(-6, 2), Interval(12, 20))
    r3 = r1.intersect_with(r2)
    assert r3 == ManhattanArc(Interval(-4, 2), Interval(12, 12))


def test_merge_3() -> None:
    s1 = ManhattanArc(1, 1)
    s2 = ManhattanArc(3, 3)
    m1 = s1.merge_with(s2, 2)
    assert m1 == ManhattanArc(Interval(3, 3), Interval(3, 3))


def test_min_dist() -> None:
    pa = Point(-8, 2)
    pb = Point(3, 4)
    dab = pa.min_dist_with(pb)
    ma = ManhattanArc.from_point(pa)
    mb = ManhattanArc.from_point(pb)
    dmab = ma.min_dist_with(mb)
    assert dab == dmab


def test_min_dist3D() -> None:
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
def test_min_dist3D_h(a1, b1, c1, a2, b2, c2) -> None:
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


def test_repr() -> None:
    a = ManhattanArc(-1, 9)
    assert repr(a) == "ManhattanArc(-1, 9)"
