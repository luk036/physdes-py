from physdes.generic import min_dist, overlap
from physdes.merge_obj import merge_obj
from physdes.recti import interval
from physdes.vector2 import vector2


def test_merge_obj():
    r1 = merge_obj(4 + 5, 4 - 5)
    r2 = merge_obj(7 + 9, 7 - 9)
    v = vector2(5, 6)

    assert r1 != r2
    assert (r1 - v) + v == r1
    assert not overlap(r1, r2)
    assert r1.min_dist_with(r2) == 7
    assert min_dist(r1, r2) == 7


def test_merge():
    s1 = merge_obj(200 + 600, 200 - 600)
    s2 = merge_obj(500 + 900, 500 - 900)
    m1 = s1.merge_with(s2)
    assert m1 == merge_obj(interval(1100, 1100), interval(-700, -100))
