from itertools import filterfalse, tee
from typing import List

from .point import Point
from .vector2 import Vector2


class Polygon:
    def __init__(self, pointset: List[Point]):
        """[summary]

        Args:
            pointset ([type]): [description]
        """
        self._origin = pointset[0]
        self._vecs = list(vtx.displace(self._origin) for vtx in pointset[1:])

    def __iadd__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]
        """
        self._origin += rhs
        return self

    def signed_area_x2(self):
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
            >>> S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
            >>> P = Polygon(S)
            >>> P.signed_area_x2()
            110
        """
        assert len(self._vecs) >= 2
        vecs = self._vecs
        res = vecs[0].x * vecs[1].y - vecs[-1].x * vecs[-2].y
        for v0, v1, v2 in zip(vecs[:-2], vecs[1:-1], vecs[2:]):
            res += v1.x * (v2.y - v0.y)
        return res

    def is_rectilinear(self):
        """@todo"""
        pass


def partition(pred, iterable):
    "Use a predicate to partition entries into true entries and false entries"
    # partition(is_odd, range(10)) --> 1 9 3 7 5 and 4 0 8 2 6
    t1, t2 = tee(iterable)
    return filter(pred, t1), filterfalse(pred, t2)


# def create_xmono_polygon(lst):
#     """[summary]

#     Arguments:
#         lst {[type]} -- [description]

#     Returns:
#         [type] -- [description]
#     """
#     assert len(lst) >= 3

#     leftmost = min(lst)
#     rightmost = max(lst)
#     d = rightmost - leftmost
#     [lst1, lst2] = partition(lambda a: d.cross(a - leftmost) <= 0, lst)
#     lst1 = sorted(lst1)
#     lst2 = sorted(lst2, reverse=True)
#     return lst1 + lst2


def create_mono_polygon(lst, dir):
    """[summary]

    Args:
        lst ([type]): [description]

    Returns:
        [type]: [description]
    """
    assert len(lst) >= 3

    max_pt = max(lst, key=dir)
    min_pt = min(lst, key=dir)
    vec = max_pt.displace(min_pt)
    [lst1, lst2] = partition(lambda pt: vec.cross(pt.displace(min_pt)) <= 0, lst)
    lst1 = sorted(lst1, key=dir)
    lst2 = sorted(lst2, key=dir, reverse=True)
    return lst1 + lst2


def create_ymono_polygon(lst):
    return create_mono_polygon(lst, lambda pt: (pt.ycoord, pt.xcoord))


def create_xmono_polygon(lst):
    return create_mono_polygon(lst, lambda pt: (pt.xcoord, pt.ycoord))


def create_test_polygon(lst):
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
        >>> S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
        >>> S = create_test_polygon(S)
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
    def dir1(pt):
        return (pt.ycoord, pt.xcoord)

    upmost = max(lst, key=dir1)
    downmost = min(lst, key=dir1)
    vec = upmost.displace(downmost)

    [lst1, lst2] = partition(lambda pt: vec.cross(pt.displace(downmost)) < 0, lst)
    lst1 = list(lst1)  # note!!!!
    lst2 = list(lst2)  # note!!!!
    rightmost = max(lst1)
    [lst3, lst4] = partition(lambda a: a.ycoord < rightmost.ycoord, lst1)
    leftmost = min(lst2)
    [lst5, lst6] = partition(lambda a: a.ycoord > leftmost.ycoord, lst2)

    if vec.x < 0:
        lsta = sorted(lst6, reverse=True)
        lstb = sorted(lst5, key=dir1)
        lstc = sorted(lst4)
        lstd = sorted(lst3, key=dir1, reverse=True)
    else:
        lsta = sorted(lst3)
        lstb = sorted(lst4, key=dir1)
        lstc = sorted(lst5, reverse=True)
        lstd = sorted(lst6, key=dir1, reverse=True)
    return lsta + lstb + lstc + lstd


def point_in_polygon(pointset, ptq):
    """determine if a Point is within a Polygon

    The code below is from Wm. Randolph Franklin <wrf@ecse.rpi.edu>
    (see URL below) with some minor modifications for integer. It returns
    true for strictly interior points, false for strictly exterior, and ub
    for points on the boundary.  The boundary behavior is complex but
    determined; in particular, for a partition of a region into polygons,
    each Point is "in" exactly one Polygon.
    (See p.243 of [O'Rourke (C)] for a discussion of boundary behavior.)

    See http://www.faqs.org/faqs/graphics/algorithms-faq/ Subject 2.03

    Args:
        pointset ([type]): [description]
        ptq ([type]): [description]

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
        >>> pointset = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
        >>> point_in_polygon(pointset, Point(0, 1))
        True
    """
    res = False
    pt0 = pointset[-1]
    for pt1 in pointset:
        if (pt1.ycoord <= ptq.ycoord < pt0.ycoord) or \
                (pt0.ycoord <= ptq.ycoord < pt1.ycoord):
            det = ptq.displace(pt0).cross(pt1.displace(pt0))
            if pt1.ycoord > pt0.ycoord:
                if det < 0:
                    res = not res
            else:  # v1.ycoord < v0.ycoord
                if det > 0:
                    res = not res
        pt0 = pt1
    return res
