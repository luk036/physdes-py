r"""
Polygon Module (src\physdes\polygon.py)

This code defines a Polygon class and related functions for working with polygons in a 2D space. The purpose of this module is to provide tools for creating, manipulating, and analyzing polygons.

The Polygon class represents a polygon using a list of points (vertices). It takes a list of Point objects as input when creating a new Polygon. The class provides methods for basic operations like adding or subtracting vectors from the polygon (which moves it), calculating its area, and comparing polygons for equality.

The module also includes several functions for creating special types of polygons:

1. create_mono_polygon: Creates a monotone polygon, which means the polygon is sorted in a specific direction.
2. create_ymono_polygon: Creates a y-monotone polygon, sorted based on y-coordinates.
3. create_xmono_polygon: Creates an x-monotone polygon, sorted based on x-coordinates.
4. create_test_polygon: Creates a test polygon with a specific shape for testing purposes.

One of the key functions in this module is point_in_polygon, which determines whether a given point is inside a polygon. This function takes a list of points representing the polygon and a single point to check. It returns a boolean value: True if the point is inside the polygon, and False if it's outside.

The point_in_polygon function uses a clever algorithm called the ray-casting algorithm. It works by imagining a horizontal line (ray) extending from the point to the right. It then counts how many times this line intersects with the edges of the polygon. If the number of intersections is odd, the point is inside the polygon; if it's even, the point is outside.

Throughout the code, there are several important data transformations happening. For example, when creating a Polygon, the input points are converted into vectors relative to the first point (the origin). This makes it easier to perform calculations and transformations on the polygon.

The module uses generic types (T) for coordinates, allowing it to work with both integer and floating-point coordinates. This flexibility makes the code more versatile and reusable in different contexts.

Overall, this module provides a comprehensive set of tools for working with polygons, from basic creation and manipulation to more complex operations like determining if a point is inside a polygon. It's designed to be flexible and efficient, making it useful for various applications involving 2D geometry.
"""

from functools import cached_property
from itertools import filterfalse, tee
from typing import Callable, Generic, List, TypeVar

from .point import Point
from .vector2 import Vector2

T = TypeVar("T", int, float)
PointSet = List[Point[T, T]]


class Polygon(Generic[T]):
    _origin: Point[T, T]
    _vecs: List[Vector2[T, T]]

    def __init__(self, pointset: PointSet) -> None:
        """
        The function initializes an object with a given point set, setting the origin to the first point and
        creating a list of vectors by displacing each point from the origin.

        :param pointset: The `pointset` parameter is of type `PointSet`. It is a collection of points that
            represents a set of vertices. The first element of the `pointset` is considered as the origin point,
            and the remaining elements are considered as displacement vectors from the origin

        :type pointset: PointSet

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
            >>> print(P._origin)
            (0, -4)
        """
        self._origin = pointset[0]
        self._vecs = list(vtx.displace(self._origin) for vtx in pointset[1:])

    def __eq__(self, rhs: object) -> bool:
        """
        The `__eq__` method compares two `Polygon` objects and returns a boolean value indicating whether
        they are equal or not.

        :param rhs: The parameter `rhs` is of type `object`. It represents the right-hand side of the
        equality comparison.

        :type rhs: object

        :return: The method is returning a boolean value.

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
            >>> Q = Polygon(S)
            >>> print(P == Q)
            True
        """
        if not isinstance(rhs, Polygon):
            return NotImplemented
        return self._origin == rhs._origin and self._vecs == rhs._vecs

    def __iadd__(self, rhs: Vector2) -> "Polygon[T]":
        """
        The `__iadd__` method adds a `Vector2` to the `_origin` attribute of the `Polygon` object and
        returns itself.

        :param rhs: The parameter `rhs` is of type `Vector2`. It represents the right-hand side of the
            addition operation

        :type rhs: Vector2

        :return: The method is returning `self`, which is an instance of the `Polygon[T]` class.

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
            >>> P += Vector2(1, 1)
            >>> print(P._origin)
            (1, -3)
        """
        self._origin += rhs
        return self

    def __isub__(self, rhs: Vector2) -> "Polygon[T]":
        """
        The `__isub__` method subtracts a `Vector2` from the `_origin` attribute of the `Polygon` object
        and returns itself.

        :param rhs: The parameter `rhs` is of type `Vector2`. It represents the right-hand side of the
            subtraction operation

        :type rhs: Vector2

        :return: The method is returning `self`, which is an instance of the `Polygon[T]` class.

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
            >>> P -= Vector2(1, 1)
            >>> print(P._origin)
            (-1, -5)
        """
        self._origin -= rhs
        return self

    @cached_property
    def signed_area_x2(self) -> T:
        """
        The `signed_area_x2` function calculates the signed area of a polygon multiplied by 2.

        :return: The `signed_area_x2` method returns the signed area of the polygon multiplied by 2.

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
            >>> P.signed_area_x2
            110
        """
        assert len(self._vecs) >= 2
        itr = iter(self._vecs)
        vec0 = next(itr)
        vec1 = next(itr)
        res = vec0.x * vec1.y - self._vecs[-1].x * self._vecs[-2].y
        for vec2 in itr:
            res += vec1.x * (vec2.y - vec0.y)
            vec0 = vec1
            vec1 = vec2
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
#
#     Arguments:
#         lst {[type]} -- [description]
#
#     Returns:
#         [type] -- [description]
#     """
#     assert len(lst) >= 3
#
#     leftmost = min(lst)
#     rightmost = max(lst)
#     d = rightmost - leftmost
#     [lst1, lst2] = partition(lambda a: d.cross(a - leftmost) <= 0, lst)
#     lst1 = sorted(lst1)
#     lst2 = sorted(lst2, reverse=True)
#     return lst1 + lst2


def create_mono_polygon(lst: PointSet, dir: Callable) -> PointSet:
    """
    The `create_mono_polygon` function creates a monotone polygon for a given point set by partitioning
    the points based on a direction and sorting them.

    :param lst: A list of points representing a point set. Each point is represented as a tuple of two
        integers, (x, y), where x and y are the coordinates of the point

    :type lst: PointSet

    :param dir: The `dir` parameter is a callable function that determines the direction in which the
        points are sorted. It takes a point as input and returns a value that represents the direction. The
        points are sorted based on this direction

    :type dir: Callable

    :return: The `create_mono_polygon` function returns a list of points representing a monotone polygon.

    :rtype: PointSet

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
        ...     (-2, 4),
        ...     (-2, 2),
        ...     (-4, 3),
        ...     (-5, 1),
        ...     (-6, -2),
        ...     (-3, -3),
        ...     (-3, -4),
        ...     (1, 4),
        ...     (-2, 4),
        ... ]
        ...
        >>> S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
        >>> _ = create_mono_polygon(S, lambda pt: (pt.ycoord, pt.xcoord))
    """
    assert len(lst) >= 3

    max_pt = max(lst, key=dir)
    min_pt = min(lst, key=dir)
    vec = max_pt.displace(min_pt)
    lst1, lst2 = partition(lambda pt: vec.cross(pt.displace(min_pt)) <= 0, lst)
    lst1 = sorted(lst1, key=dir)
    lst2 = sorted(lst2, key=dir, reverse=True)
    return lst1 + lst2


def create_ymono_polygon(lst: PointSet) -> PointSet:
    """
    The function creates a y-monotone polygon from a given point set.

    :param lst: The parameter `lst` is a `PointSet`, which is a collection of points
    :type lst: PointSet
    :return: The function `create_ymono_polygon` returns a `PointSet` object.

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
        >>> _ = create_ymono_polygon(S)

    """
    return create_mono_polygon(lst, lambda pt: (pt.ycoord, pt.xcoord))


def create_xmono_polygon(lst: PointSet) -> PointSet:
    """
    The function creates a x-monotone polygon from a given point set.

    :param lst: The parameter `lst` is a `PointSet`, which is a collection of points
    :type lst: PointSet
    :return: The function `create_xmono_polygon` returns a `PointSet` object.

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
        >>> _ = create_xmono_polygon(S)
    """
    return create_mono_polygon(lst, lambda pt: (pt.xcoord, pt.ycoord))


def create_test_polygon(lst: PointSet) -> PointSet:
    """Create a test polygon for a given point set.

    The `create_test_polygon` function takes a point set as input and returns a test polygon created
    from that point set.

    :param lst: The parameter `lst` is a `PointSet`, which is a collection of points. Each point in the
        `PointSet` has an `xcoord` and `ycoord` attribute, representing its coordinates

    :type lst: PointSet

    :return: The function `create_test_polygon` returns a `PointSet`, which is a list of `Point` objects.

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
    dnmost = min(lst, key=dir1)
    vec = upmost.displace(dnmost)

    lst1, lst2 = partition(lambda pt: vec.cross(pt.displace(dnmost)) < 0, lst)
    lst1 = list(lst1)  # note!!!!
    lst2 = list(lst2)  # note!!!!
    rightmost = max(lst1)
    lst3, lst4 = partition(lambda a: a.ycoord < rightmost.ycoord, lst1)
    leftmost = min(lst2)
    lst5, lst6 = partition(lambda a: a.ycoord > leftmost.ycoord, lst2)

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


def point_in_polygon(pointset: PointSet, ptq: Point[T, T]) -> bool:
    """
    The function `point_in_polygon` determines if a given point is within a polygon.

    The code below is from Wm. Randolph Franklin <wrf@ecse.rpi.edu>
    (see URL below) with some minor modifications for integer. It returns
    true for strictly interior points, false for strictly exterior, and ub
    for points on the boundary.  The boundary behavior is complex but
    determined; in particular, for a partition of a region into polygons,
    each Point is "in" exactly one Polygon.
    (See p.243 of [O'Rourke (C)] for a discussion of boundary behavior.)

    See http://www.faqs.org/faqs/graphics/algorithms-faq/ Subject 2.03

    :param pointset: The `pointset` parameter is a list of points that define the vertices of a polygon.
        Each point in the list is an instance of the `Point` class, which has `xcoord` and `ycoord`
        attributes representing the x and y coordinates of the point

    :type pointset: PointSet

    :param ptq: ptq is a Point object representing the point to be checked if it is within the polygon

    :type ptq: Point[T, T]

    :return: a boolean value indicating whether the given point `ptq` is within the polygon defined by
        the `pointset`.

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
        if (pt1.ycoord <= ptq.ycoord < pt0.ycoord) or (
            pt0.ycoord <= ptq.ycoord < pt1.ycoord
        ):
            det = ptq.displace(pt0).cross(pt1.displace(pt0))
            if pt1.ycoord > pt0.ycoord:
                if det < 0:
                    res = not res
            else:  # v1.ycoord < v0.ycoord
                if det > 0:
                    res = not res
        pt0 = pt1
    return res
