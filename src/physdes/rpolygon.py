from .point import Point
from .skeleton import _logger
from .vector2 import Vector2
from itertools import filterfalse, tee
from typing import List, Callable, Tuple

PointSet = List[Point[int, int]]


class RPolygon:
    """
    Rectilinear Polygon

                  ┌────1
                  │    │
                  │    │
                  │    │
       ┌──────────2    │
       │               │
       3────────┐      │
                │      │
                0──────┘
    """
    _origin: Point[int, int]
    _vecs: List[Vector2[int, int]]

    def __init__(self, pointset: PointSet) -> None:
        """[summary]

        Args:
            pointset (PointSet): [description]
        """
        self._origin = pointset[0]
        self._vecs = list(vtx.displace(self._origin) for vtx in pointset[1:])

    def __iadd__(self, rhs: Vector2[int, int]) -> "RPolygon":
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            Self: [description]
        """
        self._origin += rhs
        return self

    def signed_area(self) -> int:
        """[summary]

        Returns:
            int: [description]

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
            >>> P = RPolygon(S)
            >>> P.signed_area()
            54
        """
        assert len(self._vecs) >= 1
        vecs = self._vecs
        res = vecs[0].x * vecs[0].y
        for vec0, vec1 in zip(vecs[:-1], vecs[1:]):
            res += vec1.x * (vec1.y - vec0.y)
        return res

    def to_polygon(self):
        """@todo"""
        pass


def partition(pred, iterable):
    "Use a predicate to partition entries into true entries and false entries"
    # partition(is_odd, range(10)) --> 1 9 3 7 5 and 4 0 8 2 6
    t1, t2 = tee(iterable)
    return filter(pred, t1), filterfalse(pred, t2)


def create_mono_rpolygon(
    lst: PointSet, dir: Callable
) -> Tuple[PointSet, bool]:
    """Create a monotone rectilinear polygon for a given point set.

                                       ┌────0
                ┌──────────4           │    │
                │   lst2   │           │    │
           ┌────5          │ ┌────2    │    │
           │               │ │    │    │    │
           │               └─3    └────1    │
           │                                │
      -----0───────┬------------------------┼---- leftmost.ycoord
                   │                        │
                   1────┐                   │
                        │   3────┐  lst1    │
                        2───┘    │          │
                                 │   5──────┘
                                 │   │
                                 4───┘


    Args:
        lst (PointSet): [description]
        dir (Callable): x- or y-first

    Returns:
        PointSet: [description]
        bool: is_clockwise or is_anticlockwise depend on dir <-- Note!!!
    """
    assert len(lst) >= 2
    _logger.debug("creating_mono_rpolygon begin")

    # Use x-monotone as notation
    leftmost = min(lst, key=dir)
    rightmost = max(lst, key=dir)
    is_anticlockwise = dir(leftmost)[1] > dir(rightmost)[1]

    def r2l(pt) -> bool:
        return dir(pt)[1] <= dir(leftmost)[1]

    def l2r(pt) -> bool:
        return dir(pt)[1] >= dir(leftmost)[1]

    [lst1, lst2] = partition(r2l if is_anticlockwise else l2r, lst)
    lst1 = sorted(lst1, key=dir)
    lst2 = sorted(lst2, key=dir, reverse=True)
    return lst1 + lst2, is_anticlockwise  # is_clockwise if y-monotone


def create_xmono_rpolygon(lst: PointSet) -> Tuple[PointSet, bool]:
    """Create an x-monotone rectilinear polygon for a given point set.

    Args:
        lst (PointSet): [description]

    Returns:
        PointSet: [description]
        bool: is_anticlockwise <-- Note!!!
    """
    return create_mono_rpolygon(lst, lambda pt: (pt.xcoord, pt.ycoord))


def create_ymono_rpolygon(lst: PointSet) -> Tuple[PointSet, bool]:
    """Create an y-monotone rectilinear polygon for a given point set.

    Args:
        lst (PointSet): [description]

    Returns:
        PointSet: [description]
        bool: is_clockwise <-- Note!!!
    """
    return create_mono_rpolygon(lst, lambda pt: (pt.ycoord, pt.xcoord))


def create_test_rpolygon(lst: PointSet) -> PointSet:
    """[summary]

    Args:
        lst (PointSet): [description]

    Returns:
        PointSet: [description]

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

    def dir(pt):
        return (pt.ycoord, pt.xcoord)

    max_pt = max(lst, key=dir)
    min_pt = min(lst, key=dir)
    vec = max_pt.displace(min_pt)

    lst1, lst2 = partition(lambda pt: vec.cross(pt.displace(min_pt)) < 0, lst)
    lst1 = list(lst1)  # note!!!!
    lst2 = list(lst2)  # note!!!!
    max_pt1 = max(lst1)
    lst3, lst4 = partition(lambda pt: pt.ycoord < max_pt1.ycoord, lst1)
    min_pt2 = min(lst2)
    lst5, lst6 = partition(lambda pt: pt.ycoord > min_pt2.ycoord, lst2)

    if vec.x < 0:
        lsta = sorted(lst6, reverse=True)
        lstb = sorted(lst5, key=dir)
        lstc = sorted(lst4)
        lstd = sorted(lst3, key=dir, reverse=True)
    else:
        lsta = sorted(lst3)
        lstb = sorted(lst4, key=dir)
        lstc = sorted(lst5, reverse=True)
        lstd = sorted(lst6, key=dir, reverse=True)
    return lsta + lstb + lstc + lstd


def point_in_rpolygon(pointset: PointSet, ptq: Point[int, int]) -> bool:
    """determine if a Point is within a RPolygon

    The code below is from Wm. Randolph Franklin <wrf@ecse.rpi.edu>
    (see URL below) with some minor modifications for rectilinear. It returns
    true for strictly interior points, false for strictly exterior, and ub
    for points on the boundary.  The boundary behavior is complex but
    determined; in particular, for a partition of a region into polygons,
    each Point is "in" exactly one Polygon.
    (See p.243 of [O'Rourke (C)] for a discussion of boundary behavior.)

    See http://www.faqs.org/faqs/graphics/algorithms-faq/ Subject 2.03

       │     │                │    │    │       │
       │     │  o────────┐    │    │    │       │
       │     │  │        │    │    │    │       │
       │     │  │    q───T────F────T────F───────T──────►
       │     │  └──o     │    │    │    │       │
       │     │     │     │    │    │    │       │
       │     │     │     o────┘    │    │       │
       │     │     │               │    │       │

    Args:
        pointset (PointSet): [description]
        ptq (Point[int, int]): [description]

    Returns:
        bool: [description]

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
        >>> point_in_rpolygon(S, Point(0, 1))
        True
    """
    res = False
    pt0 = pointset[-1]
    for pt1 in pointset:
        if (pt1.ycoord <= ptq.ycoord < pt0.ycoord) or (
            pt0.ycoord <= ptq.ycoord < pt1.ycoord
        ):
            if pt1.xcoord > ptq.xcoord:
                res = not res
        pt0 = pt1
    return res
