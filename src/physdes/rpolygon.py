from itertools import filterfalse, tee
from typing import List

from .point import Point
from .vector2 import Vector2


class RPolygon:
    def __init__(self, pointset: List[Point]):
        """[summary]

        Args:
            coords ([type]): [description]
        """
        self._origin = pointset[0]
        self._vecs = list(c - pointset[0] for c in pointset[1:])

    def __iadd__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]
        """
        self._origin += rhs
        return self

    def signed_area(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> coords = [
            ...     (0, -4),
            ...     (0, -1),
            ...     (3, -3),
            ...     (5, 1),
            ...     (2, 2),
            ...     (3, 3),
            ...     (1, 4),
            ...     (-2, 4),
            ...     (-2, 2),
            ...     (-4, 3),
            ...     (-5, 1),
            ...     (-6, -2),
            ...     (-3, -3),
            ...     (-3, -4),
            ... ]
            ...
            >>> S = [Point(x, y) for x, y in coords]
            >>> P = RPolygon(S)
            >>> P.signed_area()
            54
        """
        assert len(self._vecs) >= 1
        vecs = self._vecs
        res = vecs[0].x * vecs[0].y
        for v0, v1 in zip(vecs[:-1], vecs[1:]):
            res += v1.x * (v1.y - v0.y)
        return res

    # def contains(self, p):
    #     """inclusively contains a Point p

    #     Args:
    #         p ([type]): [description]

    #     Returns:
    #         [type]: [description]
    #     """
    #     q = p - self._origin
    #     o = Vector2(0, 0)
    #     c = False
    #     for v0, v1 in zip([o] + self._vecs, self._vecs + [o]):
    #         if (v1.y <= q.y and q.y < v0.y) or (v0.y <= q.y and q.y < v1.y):
    #             if v1.x > q.x:
    #                 c = not c
    #     return c

    def to_polygon(self):
        """@todo"""
        pass


def partition(pred, iterable):
    "Use a predicate to partition entries into true entries and false entries"
    # partition(is_odd, range(10)) --> 1 9 3 7 5 and 4 0 8 2 6
    t1, t2 = tee(iterable)
    return filter(pred, t1), filterfalse(pred, t2)


def create_ymono_rpolygon(lst):
    """[summary]

    Args:
        lst ([type]): [description]

    Returns:
        [type]: [description]
    """
    assert len(lst) >= 2

    botmost = min(lst, key=lambda a: (a.y, a.x))
    topmost = max(lst, key=lambda a: (a.y, a.x))
    is_anticlockwise = topmost.x >= botmost.x
    if is_anticlockwise:
        [lst1, lst2] = partition(lambda a: a.x >= botmost.x, lst)
    else:
        [lst1, lst2] = partition(lambda a: a.x <= botmost.x, lst)
    lst1 = sorted(lst1, key=lambda a: (a.y, a.x))
    lst2 = sorted(lst2, key=lambda a: (a.y, a.x), reverse=True)
    return lst1 + lst2, is_anticlockwise


def create_xmono_rpolygon(lst):
    """[summary]

    Args:
        lst ([type]): [description]

    Returns:
        [type]: [description]
    """
    assert len(lst) >= 2

    leftmost = min(lst)
    rightmost = max(lst)
    is_anticlockwise = rightmost.y <= leftmost.y
    if is_anticlockwise:
        [lst1, lst2] = partition(lambda a: a.y <= leftmost.y, lst)
    else:
        [lst1, lst2] = partition(lambda a: a.y >= leftmost.y, lst)
    lst1 = sorted(lst1)
    lst2 = sorted(lst2, reverse=True)
    return lst1 + lst2, is_anticlockwise


def create_test_rpolygon(lst):
    """[summary]

    Args:
        lst ([type]): [description]

    Returns:
        [type]: [description]

    Examples:
        >>> coords = [
        ...     (-2, 2),
        ...     (0, -1),
        ...     (-5, 1),
        ...     (-2, 4),
        ...     (0, -4),
        ...     (-4, 3),
        ...     (-6, -2),
        ...     (5, 1),
        ...     (2, 2),
        ...     (3, -3),
        ...     (-3, -3),
        ...     (3, 3),
        ...     (-3, -4),
        ...     (1, 4),
        ... ]
        ...
        >>> S = [Point(x, y) for x, y in coords]
        >>> S = create_test_rpolygon(S)
        >>> for p in S:
        ...     print("{},".format(p))
        ...
        (0, -4),
        (0, -1),
        (3, -3),
        (5, 1),
        (2, 2),
        (3, 3),
        (1, 4),
        (-2, 4),
        (-2, 2),
        (-4, 3),
        (-5, 1),
        (-6, -2),
        (-3, -3),
        (-3, -4),
    """
    max_pt = max(lst, key=lambda a: (a.y, a.x))
    min_pt = min(lst, key=lambda a: (a.y, a.x))
    dx = max_pt.x - min_pt.x
    dy = max_pt.y - min_pt.y

    def right_left(a):
        return dx * (a.y - min_pt.y) < (a.x - min_pt.x) * dy

    [lst1, lst2] = partition(right_left, lst)
    lst1 = list(lst1)  # note!!!!
    lst2 = list(lst2)  # note!!!!
    max_pt1 = max(lst1, key=lambda a: (a.x, a.y))
    [lst3, lst4] = partition(lambda a: a.y < max_pt1.y, lst1)
    min_pt2 = min(lst2, key=lambda a: (a.x, a.y))
    [lst5, lst6] = partition(lambda a: a.y > min_pt2.y, lst2)

    if dx < 0:
        lsta = sorted(lst6, key=lambda a: (a.x, a.y), reverse=True)
        lstb = sorted(lst5, key=lambda a: (a.y, a.x))
        lstc = sorted(lst4, key=lambda a: (a.x, a.y))
        lstd = sorted(lst3, key=lambda a: (a.y, a.x), reverse=True)
    else:
        lsta = sorted(lst3, key=lambda a: (a.x, a.y))
        lstb = sorted(lst4, key=lambda a: (a.y, a.x))
        lstc = sorted(lst5, key=lambda a: (a.x, a.y), reverse=True)
        lstd = sorted(lst6, key=lambda a: (a.y, a.x), reverse=True)
    return lsta + lstb + lstc + lstd


def point_in_rpolygon(S, q):
    """determine if a Point is within a RPolygon

    The code below is from Wm. Randolph Franklin <wrf@ecse.rpi.edu>
    (see URL below) with some minor modifications for rectilinear. It returns
    true for strictly interior points, false for strictly exterior, and ub
    for points on the boundary.  The boundary behavior is complex but
    determined; in particular, for a partition of a region into polygons,
    each Point is "in" exactly one Polygon.
    (See p.243 of [O'Rourke (C)] for a discussion of boundary behavior.)

    See http://www.faqs.org/faqs/graphics/algorithms-faq/ Subject 2.03

    Args:
        S ([type]): [description]
        q ([type]): [description]

    Returns:
        [type]: [description]

    Examples:
        >>> coords = [
        ...     (0, -4),
        ...     (0, -1),
        ...     (3, -3),
        ...     (5, 1),
        ...     (2, 2),
        ...     (3, 3),
        ...     (1, 4),
        ...     (-2, 4),
        ...     (-2, 2),
        ...     (-4, 3),
        ...     (-5, 1),
        ...     (-6, -2),
        ...     (-3, -3),
        ...     (-3, -4),
        ... ]
        ...
        >>> S = [Point(x, y) for x, y in coords]
        >>> point_in_rpolygon(S, Point(0, 1))
        True
    """
    c = False
    p0 = S[-1]
    for p1 in S:
        if (p1.y <= q.y < p0.y) or (p0.y <= q.y < p1.y):
            if p1.x > q.x:
                c = not c
        p0 = p1
    return c
