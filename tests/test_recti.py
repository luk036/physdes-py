from random import randint

from physdes.interval import Interval
from physdes.point import Point
from physdes.recti import HSegment, Rectangle, VSegment, detect_overlap

# class my_point(Point):
#     def __init__(self, xcoord, ycoord, data: float):
#         Point.__init__(self, xcoord, ycoord)
#         self._data = data


def test_point() -> None:
    a = Point(4, 8)
    b = Point(5, 6)
    assert a < b
    assert a <= b
    assert not (a == b)
    assert a != b
    assert b > a
    assert b >= a


def test_interval() -> None:
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


def test_rectangle() -> None:
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


def test_segment() -> None:
    rng1 = Interval(4, 8)
    vseg = VSegment(5, rng1)
    assert vseg.contains(Point(5, 6))  # type: ignore[arg-type]
    hseg = vseg.flip()
    assert hseg.contains(Point(6, 5))  # type: ignore[arg-type]
    assert hseg.contains(Point(7, 5))  # type: ignore[arg-type]
    assert hseg == HSegment(rng1, 5)
    assert hseg.flip() == vseg


def test_rectilinear() -> None:
    N = 20
    lst = []

    for idx in range(N):
        ii_val = idx * 100
        for jdx in range(N):
            jj_val = jdx * 100
            xrng = Interval(ii_val, ii_val + randint(0, 99))
            yrng = Interval(jj_val, jj_val + randint(0, 99))
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


def test_detect_overlap_basic() -> None:
    r1 = Rectangle(Interval(0, 5), Interval(0, 5))
    r2 = Rectangle(Interval(3, 8), Interval(3, 8))
    result = detect_overlap([r1, r2])
    assert result is not None
    r_a, r_b = result
    assert (r_a.xcoord == r1.xcoord and r_a.ycoord == r1.ycoord) or (
        r_a.xcoord == r2.xcoord and r_a.ycoord == r2.ycoord
    )


def test_detect_overlap_no_overlap() -> None:
    r3 = Rectangle(Interval(0, 2), Interval(0, 2))
    r4 = Rectangle(Interval(3, 5), Interval(3, 5))
    assert detect_overlap([r3, r4]) is None


def test_detect_overlap_multiple_rectangles() -> None:
    r1 = Rectangle(Interval(0, 2), Interval(0, 2))
    r2 = Rectangle(Interval(1, 3), Interval(1, 3))
    r3 = Rectangle(Interval(10, 12), Interval(10, 12))
    result = detect_overlap([r1, r2, r3])
    assert result is not None
    r_a, r_b = result
    assert r_a.xcoord.lb <= 2 and r_b.xcoord.lb <= 2


def test_detect_overlap_single_rectangle() -> None:
    r1 = Rectangle(Interval(0, 5), Interval(0, 5))
    assert detect_overlap([r1]) is None


def test_detect_overlap_empty_list() -> None:
    assert detect_overlap([]) is None


def test_detect_overlap_touching_edges() -> None:
    r1 = Rectangle(Interval(0, 5), Interval(0, 5))
    r2 = Rectangle(Interval(5, 10), Interval(5, 10))
    result = detect_overlap([r1, r2])
    assert result is None


def test_detect_overlap_partial_y_overlap() -> None:
    r1 = Rectangle(Interval(0, 5), Interval(0, 3))
    r2 = Rectangle(Interval(3, 8), Interval(2, 6))
    result = detect_overlap([r1, r2])
    assert result is not None


def test_detect_overlap_no_x_overlap() -> None:
    r1 = Rectangle(Interval(0, 2), Interval(0, 5))
    r2 = Rectangle(Interval(3, 5), Interval(0, 5))
    assert detect_overlap([r1, r2]) is None


def test_detect_overlap_invalid_rectangle() -> None:
    r1 = Rectangle(Interval(0, 5), Interval(0, 5))
    r2 = Rectangle(Interval(5, 3), Interval(5, 3))
    result = detect_overlap([r1, r2])
    assert result is None
