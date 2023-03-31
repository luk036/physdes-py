"""
Rectilinear Point Class
"""
from .generic import contain, intersection, min_dist, overlap
from .interval import Interval, enlarge, hull
from .vector2 import Vector2

from typing import TypeVar, Generic, Union
TPoint = TypeVar("TPoint", bound="Point")
# T1 = TypeVar("T1", int, float, Interval[int], Interval[float], "Point")
# T2 = TypeVar("T2", int, float, Interval[int], Interval[float], "Point")
T1 = TypeVar("T1", int, float, "Point")
T2 = TypeVar("T2", int, float, "Point")
# TPoint = TypeVar("TPoint", bound="Point")


class Point(Generic[T1, T2]):
    """
    Generic Rectilinear Point class (▪️, ──, │, or 🫱)
    """

    xcoord: T1
    ycoord: T2

    def __init__(self, xcoord: T1, ycoord: T2) -> None:
        """[summary]

        Args:
            xcoord ([type]): [description]
            ycoord ([type]): [description]
        """
        self.xcoord = xcoord
        self.ycoord = ycoord

    def __str__(self) -> str:
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> print(a)
            (3, 4)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> print(a3d)
            ((3, 4), 5)
        """
        return "({self.xcoord}, {self.ycoord})".format(self=self)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> b = a.copy()
            >>> print(b)
            (3, 4)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = a3d.copy()
            >>> print(b3d)
            ((3, 4), 5)
        """
        T = type(self)  # Type could be Point or Rectangle or others
        return T(self.xcoord, self.ycoord)

    def __lt__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> a < b
            True
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = Point(b, 1)  # Point in 3d
            >>> a3d > b3d
            False
        """
        return (self.xcoord, self.ycoord) < (other.xcoord, other.ycoord)

    def __le__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> a <= b
            True
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = Point(b, 1)  # Point in 3d
            >>> a3d >= b3d
            False
        """
        return (self.xcoord, self.ycoord) <= (other.xcoord, other.ycoord)

    def __eq__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> a == b
            False
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = Point(b, 1)  # Point in 3d
            >>> a3d != b3d
            True
        """
        return (self.xcoord, self.ycoord) == (other.xcoord, other.ycoord)

    def __iadd__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> a += v
            >>> print(a)
            (8, 10)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> a3d += Vector2(v, 1)
            >>> print(a3d)
            ((13, 16), 6)
        """
        self.xcoord += rhs.x
        self.ycoord += rhs.y
        return self

    def __add__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> print(a + v)
            (8, 10)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> print(a3d + Vector2(v, 1))
            ((8, 10), 6)
        """
        T = type(self)  # Type could be Point or Rectangle or others
        return T(self.xcoord + rhs.x, self.ycoord + rhs.y)

    def __isub__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> a -= v
            >>> print(a)
            (-2, -2)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> a3d -= Vector2(v, 1)
            >>> print(a3d)
            ((-7, -8), 4)
        """
        self.xcoord -= rhs.x
        self.ycoord -= rhs.y
        return self

    def __sub__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector or Point): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> b = a - v
            >>> print(b)
            (-2, -2)
        """
        T = type(self)  # Type could be Point or Rectangle or others
        return T(self.xcoord - rhs.x, self.ycoord - rhs.y)

    def displace(self, rhs): # TODO: what is the type?
        """[summary]

        Args:
            rhs (Vector or Point): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> b = a - v
            >>> print(b)
            (-2, -2)
            >>> print(a.displace(b))
            <5, 6>
        """
        return Vector2(self.xcoord - rhs.xcoord, self.ycoord - rhs.ycoord)

    def flip(self):
        """[summary]

        Returns:
            TPoint[T2, T1]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> print(a.flip())
            (4, 3)
            >>> r = Point([3, 4], [5, 6])  # Rectangle
            >>> print(r.flip())
            ([5, 6], [3, 4])
        """
        return Point(self.ycoord, self.xcoord)

    def overlaps(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return overlap(self.xcoord, other.xcoord) and overlap(self.ycoord, other.ycoord)

    def contains(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return contain(self.xcoord, other.xcoord) and contain(self.ycoord, other.ycoord)

    def hull_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        T = type(self)
        return T(hull(self.xcoord, other.xcoord), hull(self.ycoord, other.ycoord))

    def intersection_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        T = type(self)
        return T(
            intersection(self.xcoord, other.xcoord),
            intersection(self.ycoord, other.ycoord),
        )

    def min_dist_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return min_dist(self.xcoord, other.xcoord) + min_dist(self.ycoord, other.ycoord)

    def enlarge_with(self, alpha): # TODO: what is the type?
        """[summary]

        Args:
            alpha ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(9, -1)
            >>> r = a.enlarge_with(1)
            >>> print(r)
            ([8, 10], [-2, 0])
        """
        xcoord = enlarge(self.xcoord, alpha)
        ycoord = enlarge(self.ycoord, alpha)
        T = type(self)
        return T(xcoord, ycoord)
