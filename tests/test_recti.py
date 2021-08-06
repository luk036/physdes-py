from random import randint

from physdes.recti import interval, point, rectangle


class my_point(point):
    def __init__(self, x, y, data: float):
        point.__init__(self, x, y)
        self._data = data


def test_Point():
    a = my_point(4, 8, 3.4)
    b = my_point(5, 6, 1.0)

    assert a < b
    assert a <= b
    assert not (a == b)
    assert a != b
    assert b > a
    assert b >= a


def test_Interval():
    a = interval(4, 8)
    b = interval(5, 6)

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
    xrng1 = interval(4, 8)
    yrng1 = interval(5, 7)
    r1 = rectangle(xrng1, yrng1)
    p = point(7, 6)
    assert r1.contains(p)
    # assert r2 in r1


def test_Rectilinear():
    N = 20
    lst = []

    for i in range(N):
        ii = i * 100
        for j in range(N):
            jj = j * 100
            xrng = interval(ii, ii + randint(0, 99))
            yrng = interval(jj, jj + randint(0, 99))
            r = rectangle(xrng, yrng)
            lst += [r]

#     S = set()  # set of maximal non-overlapped rectangles
#     L = []  # list of the removed rectangles

#     for r in lst:
#         if r in S:
#             L += [r]
#         else:
#             S.add(r)
