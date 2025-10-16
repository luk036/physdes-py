"""
RPolygon Class and Related Functions

This code defines a class called RPolygon (Rectilinear Polygon) and several related
    functions for working with polygons. The purpose of this code is to provide tools
    for creating, manipulating, and analyzing rectilinear polygons, which are polygons
    with sides that are either horizontal or vertical.

The main input for this code is a set of points, typically represented as a list of
    Point objects. Each Point object has x and y coordinates. The code can take these
    points and create an RPolygon object, which represents a rectilinear polygon.

The outputs of this code vary depending on which functions are used. Some functions
    return new polygons, while others return information about existing polygons, such
    as whether a point is inside the polygon or the signed area of the polygon.

The RPolygon class achieves its purpose by storing the polygon as an origin point
    and a list of vectors. This representation allows for efficient manipulation and
    analysis of the polygon. The class includes methods for comparing polygons, moving
    polygons, and calculating properties like the signed area.

Some important logic flows in this code include:

1. Creating monotone polygons (polygons that are monotone in either the x or y
    direction) using the create_mono_rpolygon function. This function sorts the input
    points and arranges them to form a valid monotone polygon.

2. Determining if a point is inside a polygon using the point_in_rpolygon function.
    This function uses a ray-casting algorithm to check if a given point is inside the
    polygon.

3. Calculating the signed area of a polygon using the signed_area method. This method
    uses the Shoelace formula to compute the area, which can be positive or negative
    depending on the orientation of the polygon.

The code also includes helper functions like partition, which is used to split a list
of points based on a given condition. This is useful in creating monotone polygons and
in other polygon manipulation tasks.

Overall, this code provides a set of tools for working with rectilinear polygons,
    allowing programmers to create, analyze, and manipulate these shapes in various
    ways. It's designed to be flexible and efficient, making it useful for applications
    in computational geometry, computer graphics, or any field that requires working
    with polygonal shapes.
"""

# from enum import Enum
from functools import cached_property
from itertools import filterfalse, tee
from typing import Callable, List, Tuple

from mywheel.dllist import Dllink

from .point import Point
from .polygon import Polygon
from .rdllist import RDllist
from .skeleton import _logger
from .vector2 import Vector2

PointSet = List[Point[int, int]]


class RPolygon:
    """
    Rectilinear Polygon

    .. svgbob::
       :align: center

          +--<---5 +--<---1
          |      | |      |
          |  4---+ 2---+  |
          |  |         |  ^
          |  +-----<---3  |
          0------->-------+


          +---<---5---<---1
          |       |       |
          |  4-->-2-->-+  |
          |  |  hole   |  ^
          |  +----<----3  |
          0------>--------+
    """

    _origin: Point[int, int]
    _vecs: List[Vector2[int, int]]

    def __init__(self, origin, vecs) -> None:
        """
        Initializes an RPolygon object with an origin point and a list of vectors.

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
            >>> S = [Vector2(xcoord, ycoord) for xcoord, ycoord in coords]
            >>> P = RPolygon(Point(400, 500), S)
            >>> print(P._origin)
            (400, 500)
        """
        self._origin = origin
        self._vecs = vecs

    @classmethod
    def from_pointset(cls, pointset: PointSet):
        """
        The function initializes an object with a given point set, setting the origin to the first point and
        creating a list of vectors by displacing each point from the origin.

        :param pointset: The `pointset` parameter is of type `PointSet`. It represents a collection of
            points. The `__init__` method is a constructor that initializes an instance of a class. In this
            case, it takes a `PointSet` as an argument and assigns the first point in the `

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
            >>> P = RPolygon.from_pointset(S)
            >>> print(P._origin)
            (0, -4)
        """
        origin = pointset[0]
        vecs = list(vtx.displace(origin) for vtx in pointset[1:])
        return cls(origin, vecs)

    def __eq__(self, other: object) -> bool:
        """
        The `__eq__` method is a special method in Python that is used to compare two objects for equality.
        It takes two parameters, `self` and `other`, and returns a boolean value.

        :param other: The parameter `other` is of type `object`. It represents the object to be compared
            with the current object.

        :type other: object

        :return: The method is returning a boolean value, which indicates whether the two objects are equal.

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
            >>> P = RPolygon.from_pointset(S)
            >>> Q = RPolygon.from_pointset(S)
            >>> P == Q
            True
        """
        if not isinstance(other, RPolygon):
            return NotImplemented
        return self._origin == other._origin and self._vecs == other._vecs

    def __iadd__(self, rhs: Vector2[int, int]) -> "RPolygon":
        """
        The `__iadd__` method adds a `Vector2` to the `_origin` attribute of an `RPolygon` object and
        returns the modified object.

        :param rhs: The parameter `rhs` is of type `Vector2[int, int]`. It represents the right-hand side
            operand that is being added to the current object

        :type rhs: Vector2[int, int]

        :return: The method is returning `self`, which is an instance of the `RPolygon` class.

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
            >>> P = RPolygon.from_pointset(S)
            >>> P += Vector2(1, 1)
            >>> print(P._origin)
            (1, -3)
        """
        self._origin += rhs
        return self

    def __isub__(self, rhs: Vector2[int, int]) -> "RPolygon":
        """
        The `__isub__` method subtracts a `Vector2` from the `_origin` attribute of an `RPolygon` object
        and returns the modified object.

        :param rhs: The parameter `rhs` is of type `Vector2[int, int]`. It represents the right-hand side
            operand that is being subtracted from the current object

        :type rhs: Vector2[int, int]

        :return: The method is returning `self`, which is an instance of the `RPolygon` class.

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
            >>> P = RPolygon.from_pointset(S)
            >>> P -= Vector2(1, 1)
            >>> print(P._origin)
            (-1, -5)
        """
        self._origin -= rhs
        return self

    @cached_property
    def signed_area(self) -> int:
        """
        The `signed_area` function calculates the signed area of a polygon using the Shoelace formula.

        :return: The `signed_area` method returns an integer value, which represents the signed area of a polygon.

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
            >>> P = RPolygon.from_pointset(S)
            >>> P.signed_area
            54
        """
        if len(self._vecs) < 1:
            return 0
        vec0 = self._vecs[0]
        return sum(
            [v1.x * (v1.y - v0.y) for v0, v1 in zip(self._vecs[:-1], self._vecs[1:])],
            vec0.x * vec0.y,
        )

    def is_anticlockwise(self) -> bool:
        """
        Check if the polygon is clockwise.

        :return: True if the polygon is clockwise, False otherwise.

        Examples:
            >>> from .point import Point
            >>> from .rpolygon import RPolygon
            >>> coords = [
            ...     (0, 0),
            ...     (0, 1),
            ...     (1, 1),
            ...     (1, 0),
            ... ]
            >>> S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
            >>> P = RPolygon.from_pointset(S)
            >>> P.is_anticlockwise()
            False
        """
        pointset: List[Vector2[int, int]] = [Vector2(0, 0)] + self._vecs

        if len(pointset) < 2:
            raise ValueError("RPolygon must have at least 2 points")

        # Find the point with minimum coordinates (bottom-left point)
        min_index, min_point = min(
            enumerate(pointset), key=lambda it: (it[1].x, it[1].y)
        )

        # Get the previous and next points in the polygon (with wrap-around)
        n = len(pointset)
        prev_point = pointset[(min_index - 1) % n]
        current_point = min_point

        # Calculate vectors and cross product
        return prev_point.y > current_point.y

    def to_polygon(self) -> Polygon:
        """
        The `to_polygon` function converts a rectilinear polygon to a standard polygon.

        :return: A `Polygon` object representing the converted polygon.

        Examples:
            >>> from .point import Point
            >>> from .rpolygon import RPolygon
            >>> coords = [
            ...     (0, 0),
            ...     (0, 1),
            ...     (1, 1),
            ...     (1, 0),
            ... ]
            >>> S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
            >>> P = RPolygon.from_pointset(S)
            >>> polygon = P.to_polygon()
            >>> polygon.signed_area_x2
            -2
        """
        new_vecs: List[Vector2[int, int]] = []
        current_pt: Vector2[int, int] = Vector2(0, 0)

        for next_pt in self._vecs:
            if current_pt.x != next_pt.x and current_pt.y != next_pt.y:
                # Add intermediate point for non-rectilinear segment
                new_vecs.append(Vector2(next_pt.x, current_pt.y))
            new_vecs.append(next_pt)
            current_pt = next_pt

        # Closing segment
        first_pt: Vector2[int, int] = Vector2(0, 0)
        if current_pt.x != first_pt.x and current_pt.y != first_pt.y:
            new_vecs.append(Vector2(first_pt.x, current_pt.y))

        return Polygon(self._origin, new_vecs)


def partition(pred, iterable):
    "Use a predicate to partition entries into true entries and false entries"
    # partition(is_odd, range(10)) --> 1 9 3 7 5 and 4 0 8 2 6
    t1, t2 = tee(iterable)
    return filter(pred, t1), filterfalse(pred, t2)


def create_mono_rpolygon(
    lst: PointSet, dir: Callable, cmp: Callable
) -> Tuple[PointSet, bool]:
    """
    The `create_mono_rpolygon` function creates a monotone rectilinear polygon for a given point set,
    where the direction of the polygon depends on the provided direction function.

    .. svgbob::
       :align: center

                                       ┌────0
                ┌──────────4           │    │
                │   lst2   │           │    │
           ┌────5          │ ┌────2    │    │
           │               │ │    │    │    │
           │               └─3    └────1    │
           │                                │
      ─ ─ ─0───────┬─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┼ ─ ─ leftmost.ycoord
                   │                        │
                   1────┐                   │
                        │   3────┐  lst1    │
                        2───┘    │          │
                                 │   5──────┘
                                 │   │
                                 4───┘

    :param lst: A list of points representing a point set
    :type lst: PointSet
    :param dir: The `dir` parameter is a callable function that determines the direction in which the
        points are sorted. It can be either an x-first or y-first function
    :type dir: Callable
    :return: The function `create_mono_rpolygon` returns a tuple containing two elements:
        1. `PointSet`: This is the list of points that make up the monotone rectilinear polygon.
        2. `bool`: This boolean value indicates whether the polygon is clockwise or anticlockwise, depending
        on the `dir` parameter passed to the function.

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
        >>> _, is_anticlockwise = create_mono_rpolygon(S, lambda pt: (pt.xcoord, pt.ycoord), lambda a, b: a < b)
        >>> is_anticlockwise
        True
    """
    assert len(lst) >= 2
    _logger.debug("creating_mono_rpolygon begin")

    # Use x-monotone as notation
    leftmost = min(lst, key=dir)
    rightmost = max(lst, key=dir)
    is_anticlockwise = cmp(dir(leftmost)[1], dir(rightmost)[1])

    def r2l(pt) -> bool:
        return dir(pt)[1] <= dir(leftmost)[1]

    def l2r(pt) -> bool:
        return dir(pt)[1] >= dir(leftmost)[1]

    [lst1, lst2] = partition(r2l if is_anticlockwise else l2r, lst)
    lst1 = sorted(lst1, key=dir)
    lst2 = sorted(lst2, key=dir, reverse=True)
    return lst1 + lst2, is_anticlockwise  # is_clockwise if y-monotone


def create_xmono_rpolygon(lst: PointSet) -> Tuple[PointSet, bool]:
    """
    The function creates an x-monotone rectilinear polygon for a given point set.

    :param lst: A point set represented as a list of points. Each point has x and y coordinates
    :type lst: PointSet
    :return: The function `create_xmono_rpolygon` returns a tuple containing two elements: a `PointSet`
        and a boolean value is_anticlockwise <-- Note!!!

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
        >>> _, is_anticlockwise = create_xmono_rpolygon(S)
        >>> is_anticlockwise
        True
    """
    return create_mono_rpolygon(
        lst, lambda pt: (pt.xcoord, pt.ycoord), lambda a, b: a < b
    )


def create_ymono_rpolygon(lst: PointSet) -> Tuple[PointSet, bool]:
    """
    The function creates a y-monotone rectilinear polygon for a given point set.

    :param lst: A point set represented as a list of points. Each point has x and y coordinates
    :type lst: PointSet
    :return: The function `create_ymono_rpolygon` returns a tuple containing two elements: a `PointSet`
        and a boolean value is_clockwise <-- Note!!!

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
        >>> _, is_clockwise = create_ymono_rpolygon(S)
        >>> is_clockwise
        False
    """
    return create_mono_rpolygon(
        lst, lambda pt: (pt.ycoord, pt.xcoord), lambda a, b: a > b
    )


def create_test_rpolygon(lst: PointSet) -> PointSet:
    def dir_x(pt):
        return (pt.xcoord, pt.ycoord)

    def dir_y(pt):
        return (pt.ycoord, pt.xcoord)

    max_pt = max(lst, key=dir_y)
    min_pt = min(lst, key=dir_y)
    vec = max_pt.displace(min_pt)

    lst1, lst2 = partition(lambda pt: vec.cross(pt.displace(min_pt)) < 0, lst)
    lst1 = list(lst1)  # note!!!!
    lst2 = list(lst2)  # note!!!!
    max_pt1 = max(lst1, key=dir_x)
    lst3, lst4 = partition(lambda pt: pt.ycoord < max_pt1.ycoord, lst1)
    min_pt2 = min(lst2, key=dir_x)
    lst5, lst6 = partition(lambda pt: pt.ycoord > min_pt2.ycoord, lst2)

    if vec.x < 0:
        lsta = sorted(lst6, key=dir_x, reverse=True)
        lstb = sorted(lst5, key=dir_y)
        lstc = sorted(lst4, key=dir_x)
        lstd = sorted(lst3, key=dir_y, reverse=True)
    else:
        lsta = sorted(lst3, key=dir_x)
        lstb = sorted(lst4, key=dir_y)
        lstc = sorted(lst5, key=dir_x, reverse=True)
        lstd = sorted(lst6, key=dir_y, reverse=True)
    return lsta + lstb + lstc + lstd


def rpolygon_is_monotone(lst: PointSet, dir: Callable) -> bool:
    """
    Check if a rectilinear polygon is monotone in a given direction.

    :param lst: A list of points representing the vertices of the polygon.
    :param dir: A function that extracts the coordinates for the desired direction.
    :return: True if the polygon is monotone, False otherwise.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
        >>> rpolygon_is_monotone(lst, lambda p: (p.xcoord, p.ycoord))
        True
        >>> lst = [Point(0, 0), Point(1, 1), Point(0, 1), Point(1, 0)]
        >>> rpolygon_is_monotone(lst, lambda p: (p.xcoord, p.ycoord))
        False
    """
    if len(lst) <= 3:
        return True

    min_index, _ = min(enumerate(lst), key=lambda it: dir(it[1]))
    max_index, _ = max(enumerate(lst), key=lambda it: dir(it[1]))
    rdll = RDllist(len(lst))
    v_min = rdll[min_index]
    v_max = rdll[max_index]

    def voilate(vi: Dllink[int], v_stop: Dllink[int], cmp: Callable) -> bool:
        while id(vi) != id(v_stop):
            vnext = vi.next
            if cmp(dir(lst[vi.data])[0], dir(lst[vnext.data])[0]):
                return True
            vi = vnext
        return False

    # Chain from min to max
    if voilate(v_min, v_max, lambda a, b: a > b):
        return False

    # Chain from max to min
    return not voilate(v_max, v_min, lambda a, b: a < b)


def rpolygon_is_xmonotone(lst: PointSet) -> bool:
    """
    Check if a rectilinear polygon is x-monotone.

    :param lst: A list of points representing the vertices of the polygon.
    :return: True if the polygon is x-monotone, False otherwise.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
        >>> rpolygon_is_xmonotone(lst)
        True
        >>> lst = [Point(0, 0), Point(1, 1), Point(0, 1), Point(1, 0)]
        >>> rpolygon_is_xmonotone(lst)
        False
    """
    return rpolygon_is_monotone(lst, lambda pt: (pt.xcoord, pt.ycoord))


def rpolygon_is_ymonotone(lst: PointSet) -> bool:
    """
    Check if a rectilinear polygon is y-monotone.

    :param lst: A list of points representing the vertices of the polygon.
    :return: True if the polygon is y-monotone, False otherwise.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
        >>> rpolygon_is_ymonotone(lst)
        True
        >>> lst = [Point(0, 0), Point(1, 1), Point(0, 1), Point(1, 0)]
        >>> rpolygon_is_ymonotone(lst)
        True
    """
    return rpolygon_is_monotone(lst, lambda pt: (pt.ycoord, pt.xcoord))


def rpolygon_is_convex(lst: PointSet) -> bool:
    """
    Check if a rectilinear polygon is convex.

    :param lst: A list of points representing the vertices of the polygon.
    :return: True if the polygon is convex, False otherwise.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0)]
        >>> rpolygon_is_convex(lst)
        True
        >>> lst = [Point(0, 0), Point(0, 2), Point(1, 2), Point(1, 1), Point(2, 1), Point(2, 0)]
        >>> rpolygon_is_convex(lst)
        True
    """
    return rpolygon_is_xmonotone(lst) and rpolygon_is_ymonotone(lst)


def point_in_rpolygon(pointset: PointSet, ptq: Point[int, int]) -> bool:
    """
    The function `point_in_rpolygon` determines if a given point is within a given RPolygon.

    The code below is from Wm. Randolph Franklin <wrf@ecse.rpi.edu>
    (see URL below) with some minor modifications for rectilinear. It returns
    true for strictly interior points, false for strictly exterior, and ub
    for points on the boundary.  The boundary behavior is complex but
    determined; in particular, for a partition of a region into polygons,
    each Point is "in" exactly one Polygon.
    (See p.243 of [O'Rourke (C)] for a discussion of boundary behavior.)

    See http://www.faqs.org/faqs/graphics/algorithms-faq/ Subject 2.03

    .. svgbob::
       :align: center

       │     │                │    │    │       │
       │     │  o────────┐    │    │    │       │
       │     │  │        │    │    │    │       │
       │     │  │    q───T────F────T────F───────T──────►
       │     │  └──o     │    │    │    │       │
       │     │     │     │    │    │    │       │
       │     │     │     o────┘    │    │       │
       │     │     │               │    │       │

    :param pointset: The `pointset` parameter is a list of points that define the vertices of the
        RPolygon. Each point in the list is represented as a `Point` object, which has `xcoord` and `ycoord`
        attributes representing the x and y coordinates of the point, respectively

    :type pointset: PointSet

    :param ptq: ptq is a Point object representing the query point. It has two attributes: xcoord and
        ycoord, which represent the x and y coordinates of the point, respectively

    :type ptq: Point[int, int]

    :return: a boolean value indicating whether the given point `ptq` is within the given RPolygon
        defined by the `pointset`.

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
        False
        >>> point_in_rpolygon(S, Point(0, -4))
        True
        >>> point_in_rpolygon(S, Point(-6, -2))
        False
        >>> point_in_rpolygon(S, Point(0, 0))
        False
        >>> point_in_rpolygon(S, Point(10, 10))
        False
    """
    res = False
    pt0 = pointset[-1]
    for pt1 in pointset:
        if (
            (pt1.ycoord <= ptq.ycoord < pt0.ycoord)
            or (pt0.ycoord <= ptq.ycoord < pt1.ycoord)
            and pt1.xcoord > ptq.xcoord
        ):
            res = not res
        pt0 = pt1
    return res


def rpolygon_make_monotone_hull(
    lst: PointSet, is_anticlockwise: bool, dir: Callable
) -> PointSet:
    """
    Create the x-monotone hull of a rectilinear polygon.

    :param lst: A list of points representing the vertices of the polygon.
    :param is_anticlockwise: True if the polygon is anticlockwise, False otherwise.
    :return: A list of points representing the x-monotone hull.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(1, 2), Point(2, 1)]
        >>> hull = rpolygon_make_xmonotone_hull(lst, False)
        >>> len(hull)
        3
    """
    if len(lst) <= 3:
        return lst

    min_index, min_point = min(enumerate(lst), key=lambda it: dir(it[1]))
    max_index, _ = max(enumerate(lst), key=lambda it: dir(it[1]))

    # Get the previous and next points in the polygon (with wrap-around)
    rdll = RDllist(len(lst))
    v_min = rdll[min_index]
    v_max = rdll[max_index]

    def process(
        vcurr: Dllink[int],
        vstop: Dllink[int],
        cmp: Callable,
        cmp2: Callable,
        dir: Callable,
    ) -> None:
        while id(vcurr) != id(vstop):
            vnext = vcurr.next
            vprev = vcurr.prev
            p0 = lst[vprev.data]
            p1 = lst[vcurr.data]
            p2 = lst[vnext.data]
            if cmp(dir(p1)[0], dir(p2)[0]) or cmp(dir(p0)[0], dir(p1)[0]):
                area_diff = (p1.ycoord - p0.ycoord) * (p2.xcoord - p1.xcoord)
                if cmp2(area_diff):
                    vcurr.detach()
                    vcurr = vprev
                else:
                    vcurr = vnext
            else:
                vcurr = vnext

    if is_anticlockwise:
        # Chain from min to max
        process(v_min, v_max, lambda x, y: x >= y, lambda a: a >= 0, dir)
        # Chain from max to min
        process(v_max, v_min, lambda x, y: x <= y, lambda a: a >= 0, dir)
    else:
        # Chain from min to max
        process(v_min, v_max, lambda x, y: x >= y, lambda a: a <= 0, dir)
        # Chain from max to min
        process(v_max, v_min, lambda x, y: x <= y, lambda a: a <= 0, dir)

    return [min_point] + [lst[v.data] for v in rdll.from_node(min_index)]


def rpolygon_make_xmonotone_hull(lst: PointSet, is_anticlockwise: bool) -> PointSet:
    """
    Create the x-monotone hull of a rectilinear polygon.

    :param lst: A list of points representing the vertices of the polygon.
    :param is_anticlockwise: True if the polygon is anticlockwise, False otherwise.
    :return: A list of points representing the x-monotone hull.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(1, 2), Point(2, 1)]
        >>> hull = rpolygon_make_xmonotone_hull(lst, False)
        >>> len(hull)
        3
    """
    return rpolygon_make_monotone_hull(
        lst, is_anticlockwise, lambda p: (p.xcoord, p.ycoord)
    )


def rpolygon_make_ymonotone_hull(lst: PointSet, is_anticlockwise: bool) -> PointSet:
    """
    Create the y-monotone hull of a rectilinear polygon.

    :param lst: A list of points representing the vertices of the polygon.
    :param is_anticlockwise: True if the polygon is anticlockwise, False otherwise.
    :return: A list of points representing the y-monotone hull.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(1, 2), Point(2, 1)]
        >>> hull = rpolygon_make_ymonotone_hull(lst, False)
        >>> len(hull)
        3
    """
    return rpolygon_make_monotone_hull(
        lst, is_anticlockwise, lambda p: (p.ycoord, p.xcoord)
    )


def rpolygon_make_convex_hull(pointset: PointSet, is_anticlockwise: bool) -> PointSet:
    """
    Create the convex hull of a rectilinear polygon.

    :param pointset: A list of points representing the vertices of the polygon.
    :param is_anticlockwise: True if the polygon is anticlockwise, False otherwise.
    :return: A list of points representing the convex hull.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(1, 2), Point(2, 1)]
        >>> hull = rpolygon_make_convex_hull(lst, False)
        >>> len(hull)
        3
    """
    S = rpolygon_make_xmonotone_hull(pointset, is_anticlockwise)
    return rpolygon_make_ymonotone_hull(S, is_anticlockwise)
