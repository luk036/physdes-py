from physdes.generic import overlap, contain, intersection, min_dist, nearest, displacement
from physdes.interval import Interval
from physdes.point import Point
from physdes.vector2 import Vector2

def test_overlap_scalar():
    assert overlap(1, 1) is True
    assert overlap(1, 3) is False

def test_overlap_interval():
    assert overlap(Interval(1, 2), Interval(2, 3)) is True
    assert overlap(Interval(1, 2), Interval(3, 4)) is False
    assert overlap(Interval(1, 2), 2) is True
    assert overlap(Interval(1, 2), 4) is False
    assert overlap(2, Interval(2, 3)) is True
    assert overlap(1, Interval(3, 4)) is False
    assert overlap(1, Interval(1, 2)) is True

def test_contain_scalar():
    assert contain(1, 1) is True
    assert contain(1, 3) is False

def test_contain_interval():
    assert contain(Interval(1, 4), Interval(2, 3)) is True
    assert contain(Interval(1, 2), Interval(3, 4)) is False
    assert contain(Interval(1, 2), 2) is True
    assert contain(Interval(1, 2), 4) is False
    assert contain(2, Interval(2, 3)) is False
    assert contain(1, Interval(3, 4)) is False

def test_intersection_scalar():
    assert intersection(1, 1) == 1

def test_intersection_interval():
    assert intersection(Interval(1, 2), Interval(2, 3)) == Interval(2, 2)
    assert intersection(Interval(1, 2), 2) == Interval(2, 2)
    assert intersection(2, Interval(2, 3)) == Interval(2, 2)
    assert intersection(1, Interval(1, 2)) == Interval(1, 1)
    assert intersection(Interval(1, 2), Interval(1, 2)) == Interval(1, 2)
    assert intersection(Interval(1, 2), Interval(2, 3)) == Interval(2, 2)
    assert intersection(Interval(1, 2), 2) == Interval(2, 2)

def test_min_dist_scalar():
    assert min_dist(1, 1) == 0
    assert min_dist(1, 3) == 2

def test_min_dist_interval():
    assert min_dist(Interval(1, 2), Interval(2, 3)) == 0
    assert min_dist(Interval(1, 2), Interval(3, 4)) == 1
    assert min_dist(Interval(1, 2), 2) == 0
    assert min_dist(Interval(1, 2), 4) == 2
    assert min_dist(2, Interval(2, 3)) == 0
    assert min_dist(1, Interval(3, 4)) == 2
    assert min_dist(1, Interval(1, 2)) == 0
    assert min_dist(Interval(1, 2), Interval(1, 2)) == 0
    assert min_dist(Interval(1, 2), Interval(2, 3)) == 0
    assert min_dist(Interval(1, 2), 2) == 0

def test_nearest_scalar():
    assert nearest(1, 1) == 1
    assert nearest(1, 3) == 1

def test_displacement_scalar():
    assert displacement(1, 1) == 0
    assert displacement(1, 3) == -2

def test_displacement_interval():
    assert displacement(Interval(1, 2), Interval(2, 3)) == Interval(-1, -1)
    assert displacement(Interval(1, 2), Interval(3, 4)) == Interval(-2, -2)

def test_displacement_point():
    assert displacement(Point(1, 2), Point(3, 4)) == Vector2(-2, -2)
