from physdes.generic import min_dist, overlap
from physdes.merge_obj import MergeObj
from physdes.recti import Interval
from physdes.vector2 import Vector2


def test_MergeObj():
    r1 = MergeObj(4 + 5, 4 - 5)
    r2 = MergeObj(7 + 9, 7 - 9)
    v = Vector2(5, 6)

    assert r1 != r2
    # assert (r1 - v) + v == r1
    # assert not overlap(r1, r2)
    assert r1.min_dist_with(r2) == 7
    assert min_dist(r1, r2) == 7


def test_merge():
    s1 = MergeObj(200 + 600, 200 - 600)
    s2 = MergeObj(500 + 900, 500 - 900)
    m1 = s1.merge_with(s2)
    print(m1)
    assert m1 == MergeObj(Interval(1100, 1100), Interval(-700, -100))
