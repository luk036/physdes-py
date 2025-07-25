from hypothesis import given
from hypothesis.strategies import integers

from physdes.generic import contain, displacement, intersection, min_dist, overlap
from physdes.interval import Interval, enlarge, hull


@given(
    integers(min_value=-1000, max_value=1000), integers(min_value=-1000, max_value=1000)
)
def test_interval_hypo(a1: int, a2: int):
    a = Interval(min(a1, a2), max(a1, a2))
    assert a.lb <= a.ub


def test_interval_arithmetic_hypo():
    @given(
        integers(min_value=-1000, max_value=1000),
        integers(min_value=0, max_value=1000),
        integers(min_value=-1000, max_value=1000),
    )
    def test_add_sub(a1, a2, v):
        a = Interval(min(a1, a2), max(a1, a2))
        assert (a + v) - v == a

    test_add_sub()


def test_interval():
    a = Interval(4, 8)
    b = Interval(5, 6)

    assert not (a < b)
    assert not (b < a)
    assert not (a > b)
    assert not (b > a)
    assert a <= b
    assert b <= a
    assert a >= b
    assert b >= a

    assert not (b == a)
    assert b != a

    assert a.contains(4)
    assert a.contains(8)
    assert a.intersect_with(8) == Interval(8, 8)
    assert a.contains(b)
    assert a.intersect_with(b) == b
    assert not b.contains(a)
    assert a.overlaps(b)
    assert b.overlaps(a)
    assert min_dist(a, b) == 0


def test_interval2():
    a = Interval(3, 4)
    assert a.lb == 3
    assert a.ub == 4
    assert a.length() == 1
    assert a.contains(3)
    assert a.contains(4)
    assert not a.contains(5)
    assert a.contains(Interval(3, 4))
    assert not a.contains(Interval(3, 5))
    assert not a.contains(Interval(2, 3))
    assert not a.contains(2)
    assert a.contains(4)
    assert not a.contains(5)


def test_arithmetic():
    a = Interval(3, 5)
    # b = Interval(5, 7)
    # c = Interval(7, 8)
    assert a + 1 == Interval(4, 6)
    assert a - 1 == Interval(2, 4)
    assert a * 2 == Interval(6, 10)
    assert -a == Interval(-5, -3)

    a += 1
    assert a == Interval(4, 6)
    a -= 1
    assert a == Interval(3, 5)
    a *= 2
    assert a == Interval(6, 10)


def test_overlap():
    a = Interval(3, 5)
    b = Interval(5, 7)
    c = Interval(7, 8)
    assert a.overlaps(b)
    assert b.overlaps(c)
    assert not a.overlaps(c)
    assert not c.overlaps(a)
    assert overlap(a, b)
    assert overlap(b, c)
    assert not overlap(a, c)
    assert not overlap(c, a)

    d = 4
    assert a.overlaps(d)
    assert not a.overlaps(6)
    assert overlap(a, d)
    assert overlap(d, a)
    assert overlap(d, d)


def test_contains():
    a = Interval(3, 5)
    b = Interval(5, 7)
    c = Interval(7, 8)
    assert not a.contains(b)
    assert not b.contains(c)
    assert not a.contains(c)
    assert not c.contains(a)
    assert not contain(a, b)
    assert not contain(b, c)
    assert not contain(a, c)

    d = 4
    assert a.contains(d)
    assert not a.contains(6)
    assert contain(a, d)
    assert not contain(d, a)
    assert contain(d, d)


def test_intersection():
    a = Interval(3, 5)
    b = Interval(5, 7)
    c = Interval(7, 8)
    assert a.intersect_with(b) == Interval(5, 5)
    assert b.intersect_with(c) == Interval(7, 7)
    assert a.intersect_with(c).is_invalid()
    assert intersection(a, b) == Interval(5, 5)
    assert intersection(b, c) == Interval(7, 7)

    d = 4
    assert a.intersect_with(d) == Interval(4, 4)
    assert a.intersect_with(6).is_invalid()

    assert intersection(a, d) == Interval(4, 4)
    assert intersection(d, a) == Interval(4, 4)
    assert intersection(d, d) == d


def test_hull():
    a = Interval(3, 5)
    b = Interval(5, 7)
    c = Interval(7, 8)
    assert a.hull_with(b) == Interval(3, 7)
    assert b.hull_with(c) == Interval(5, 8)
    assert a.hull_with(c) == Interval(3, 8)

    d = 4
    assert a.hull_with(d) == Interval(3, 5)
    assert a.hull_with(6) == Interval(3, 6)

    assert hull(a, d) == Interval(3, 5)
    assert hull(a, 6) == Interval(3, 6)
    assert hull(d, a) == Interval(3, 5)
    assert hull(6, a) == Interval(3, 6)
    assert hull(d, 6) == Interval(4, 6)


def test_min_dist():
    a = Interval(3, 5)
    b = Interval(5, 7)
    c = Interval(7, 8)
    assert a.min_dist_with(b) == 0
    assert a.min_dist_with(c) == 2
    assert b.min_dist_with(c) == 0
    assert min_dist(a, b) == 0
    assert min_dist(a, c) == 2
    assert min_dist(b, c) == 0

    d = 4
    assert min_dist(a, d) == 0
    assert min_dist(d, a) == 0
    assert min_dist(a, 6) == 1
    assert min_dist(6, a) == 1


def test_displacement():
    a = Interval(3, 5)
    b = Interval(5, 7)
    c = Interval(7, 8)
    assert a.displace(b) == Interval(-2, -2)
    assert a.displace(c) == Interval(-4, -3)
    assert b.displace(c) == Interval(-2, -1)
    assert displacement(a, b) == Interval(-2, -2)
    assert displacement(a, c) == Interval(-4, -3)
    assert displacement(b, c) == Interval(-2, -1)

    d = 4
    assert displacement(d, d) == 0
    assert displacement(d, 6) == -2
    assert displacement(6, d) == 2


def test_enlarge():
    a = Interval(3, 5)
    # b = Interval(5, 7)
    # c = Interval(7, 8)
    assert a.enlarge_with(2) == Interval(1, 7)
    assert enlarge(a, 2) == Interval(1, 7)

    d = 4
    assert enlarge(d, 6) == Interval(-2, 10)
    assert enlarge(6, d) == Interval(2, 10)


# def test_interval_of_interval():
#     a = Interval(Interval(3, 4), Interval(8, 9))
#     b = Interval(Interval(5, 6), Interval(6, 7))
#     v = 3

#     assert not (a < b)
#     assert not (b < a)
#     assert not (a > b)
#     assert not (b > a)
#     assert a <= b
#     assert b <= a
#     assert a >= b
#     assert b >= a

#     assert not (b == a)
#     assert b != a

#     assert (a - v) + v == a

#     assert a.contains(Interval(4, 5))
#     assert a.contains(Interval(7, 8))
#     assert a.overlaps(Interval(7, 8))

#     # print(max(Interval(3, 4), 7))
#     # print(min(Interval(8, 9), 8))
#     # print(a.intersect_with(Interval(7, 8)))

#     # The following depends on how max() and min() are implemented!!!!
#     assert a.intersect_with(Interval(7, 8)) == Interval(7, Interval(8, 9))

#     assert a.contains(b)
#     assert a.intersect_with(b) == b
#     assert not b.contains(a)
#     assert a.overlaps(b)
#     assert b.overlaps(a)
#     assert min_dist(a, b) == 0
