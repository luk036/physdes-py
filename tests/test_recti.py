from random import randint

from physdes.interval import Interval
from physdes.point import Point
from physdes.recti import HSegment, Rectangle, VSegment

# class my_point(Point):
#     def __init__(self, xcoord, ycoord, data: float):
#         Point.__init__(self, xcoord, ycoord)
#         self._data = data


def test_Point():
    a = Point(4, 8)
    b = Point(5, 6)
    assert a < b
    assert a <= b
    assert not (a == b)
    assert a != b
    assert b > a
    assert b >= a


def test_Interval():
    a = Interval(4, 8)
    b = Interval(5, 6)
    assert 3 < a
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
    assert a.contains(b)
    assert not b.contains(a)


def test_Rectangle():
    xrng1 = Interval(4, 8)
    yrng1 = Interval(5, 7)
    r1 = Rectangle(xrng1, yrng1)
    assert r1.ll == Point(4, 5)
    assert r1.ur == Point(8, 7)
    assert r1.width() == 4
    assert r1.height() == 2
    assert r1.area() == 8
    assert r1.flip() == Rectangle(yrng1, xrng1)
    p = Point(7, 6)
    assert r1.contains(p)


def test_segment():
    rng1 = Interval(4, 8)
    vseg = VSegment(5, rng1)
    assert vseg.contains(Point(5, 6))
    hseg = vseg.flip()
    assert hseg.contains(Point(6, 5))
    assert hseg.contains(Point(7, 5))
    assert hseg == HSegment(rng1, 5)
    assert hseg.flip() == vseg


def test_Rectilinear():
    N = 20
    lst = []

    for i in range(N):
        ii = i * 100
        for j in range(N):
            jj = j * 100
            xrng = Interval(ii, ii + randint(0, 99))
            yrng = Interval(jj, jj + randint(0, 99))
            r = Rectangle(xrng, yrng)
            lst += [r]


#     S = set()  # set of maximal non-overlapped rectangles
#     L = []  # list of the removed rectangles
#
#     for r in lst:
#         if r in S:
#             L += [r]
#         else:
#             S.add(r)
