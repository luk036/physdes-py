from physdes.interval import Interval, min_dist
from physdes.merge_obj import MergeObj
from physdes.vector2 import Vector2


def test_MergeObj():
    r1 = MergeObj.construct(4, 5)
    r2 = MergeObj.construct(7, 9)
    # v = Vector2(5, 6)

    assert r1 != r2
    # assert (r1 - v) + v == r1
    # assert not overlap(r1, r2)
    assert r1.min_dist_with(r2) == 7
    assert min_dist(r1, r2) == 7
    assert repr(r1) == "MergeObj(9, -1)"


def test_merge():
    s1 = MergeObj(200 + 600, 200 - 600)
    s2 = MergeObj(500 + 900, 500 - 900)
    m1 = s1.merge_with(s2)
    print(m1)
    assert m1 == MergeObj(Interval(1100, 1100), Interval(-700, -100))


def test_merge_2():
    a = MergeObj(4 + 5, 4 - 5)
    b = MergeObj(7 + 9, 7 - 9)
    v = Vector2(2, 3)
    a += v
    a -= v
    assert a == MergeObj(4 + 5, 4 - 5)
    r1 = a.enlarge_with(3)
    assert r1 == MergeObj(Interval(6, 12), Interval(-4, 2))
    r2 = b.enlarge_with(4)
    assert r2 == MergeObj(Interval(12, 20), Interval(-6, 2))
    r3 = r1.intersect_with(r2)
    assert r3 == MergeObj(Interval(12, 12), Interval(-4, 2))


def test_merge_3():
    s1 = MergeObj(1, 1)
    s2 = MergeObj(3, 3)
    m1 = s1.merge_with(s2)
    assert m1 == MergeObj(Interval(2, 2), Interval(2, 2))


def test_repr():
    a = MergeObj(9, -1)
    assert repr(a) == "MergeObj(9, -1)"
