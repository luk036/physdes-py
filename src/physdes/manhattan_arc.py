"""
ManhattanArc Class

This code defines a class called ManhattanArc, which represents a geometric object in a 2D space.
The purpose of this class is to handle operations on points, segments, or regions that are
rotated 45 degrees. It's designed to work with different types of coordinates, such as
integers, floats, or intervals.

The ManhattanArc class takes two inputs when creating an object: xcoord and ycoord. These
represent the coordinates of the object in the rotated space. The class doesn't produce a
specific output on its own, but it provides various methods to manipulate and interact
with these objects.

The class achieves its purpose by storing the coordinates in a Point object and providing
methods to perform operations like translation, enlargement, intersection, and merging
with other ManhattanArc instances. It uses a 45-degree rotated coordinate system, which allows
for easier calculations in certain geometric operations.

Some important logic flows in this code include:

1. The constructor (init) creates a Point object with the given coordinates.
2. The construct method creates a ManhattanArc from regular x and y coordinates by rotating
   them 45 degrees.
3. The translation methods (iadd and isub) move the object by adding or subtracting
   vector components.
4. The min_dist_with method calculates the minimum rectilinear distance between two
   ManhattanArc instances.
5. The enlarge_with method creates a new ManhattanArc with enlarged coordinates.
6. The intersect_with method finds the intersection point between two ManhattanArc instances.
7. The merge_with method combines two ManhattanArc instances by enlarging them based on their
   distance and finding their intersection.

These operations allow for complex geometric manipulations, which can be useful in various
applications such as computer graphics, game development, or computational geometry. The
class provides a high-level interface for working with these rotated geometric objects,
abstracting away some of the more complex mathematical calculations.
"""

from typing import TYPE_CHECKING, Any, Generic, TypeVar, overload

from icecream import ic  # type: ignore

from .generic import min_dist
from .interval import enlarge
from .point import Point

if TYPE_CHECKING:
    from .interval import Interval

T1 = TypeVar("T1", int, float, "Interval[int]", "Interval[float]")
T2 = TypeVar("T2", int, float, "Interval[int]", "Interval[float]")


class ManhattanArc(Generic[T1, T2]):
    """
    Merging point, segment, or region ⛝

    A 45 degree rotated point, vertical or horizontal segment, or rectangle

    .. svgbob::
       :align: center

              .
            .' `.
          .'     `.
        .'    .    `.
         `.       .'
           `.   .'
             `.'

              .
            .' `.
          .'     `.
        .'    .    `.
         `.    `.    `.
           `.    `.    `.
             `.       .'
               `.   .'
                 `.'

    """

    impl: Point[T1, T2]

    def __init__(self, xcoord: T1, ycoord: T2) -> None:
        """
        Initializes a ManhattanArc object with the given x and y coordinates.

        :param xcoord: The x-coordinate in the 45-degree rotated space.
        :type xcoord: T1
        :param ycoord: The y-coordinate in the 45-degree rotated space.
        :type ycoord: T2

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> print(a)
            /-1, 9/
        """
        self.impl: Point[T1, T2] = Point(xcoord, ycoord)

    @classmethod
    def from_point(cls, pt: Point[T1, T2]) -> "ManhattanArc[T1, T2]":
        """
        Create a ManhattanArc object from a 2D point.

        :param pt: A 2D point.
        :type pt: Point
        :return: A new ManhattanArc object.
        :rtype: ManhattanArc
        """
        pt_xformed = pt.rotates()
        return cls(pt_xformed.xcoord, pt_xformed.ycoord)

    @overload
    @staticmethod
    def construct(xcoord: int, ycoord: int) -> "ManhattanArc[int, int]": ...

    @overload
    @staticmethod
    def construct(xcoord: float, ycoord: float) -> "ManhattanArc[float, float]": ...

    @staticmethod
    def construct(xcoord: int, ycoord: int) -> "ManhattanArc[int, int]":
        """
        Constructs a ManhattanArc object from standard x and y coordinates.

        :param xcoord: The x-coordinate.
        :type xcoord: int
        :param ycoord: The y-coordinate.
        :type ycoord: int
        :return: A new ManhattanArc object.
        :rtype: ManhattanArc[int, int]
        """
        impl = Point(xcoord - ycoord, xcoord + ycoord)
        return ManhattanArc(impl.xcoord, impl.ycoord)

    def __repr__(self) -> str:
        """
        The `__repr__` function returns a string representation of an `ManhattanArc` object, including the class
        name and its x and y coordinates, which is useful for debugging.

        :return: The `__repr__` method is returning a string representation of the `ManhattanArc` object.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> repr(a)
            'ManhattanArc(-1, 9)'
        """
        return f"{self.__class__.__name__}({self.impl.xcoord}, {self.impl.ycoord})"

    def __str__(self) -> str:
        """
        The `__str__` function returns a string representation of an object, specifically in the format
        "/xcoord, ycoord/".

        :return: The method `__str__` returns a string representation of the object. In this case, it
            returns a string in the format "/xcoord, ycoord/" where xcoord and ycoord are the x and y
            coordinates of the object.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> print(a)
            /-1, 9/
        """
        return f"/{self.impl.xcoord}, {self.impl.ycoord}/"

    def __eq__(self, other: object) -> bool:
        """
        The `__eq__` function checks if two `ManhattanArc` instances have the same `impl` attribute.

        :param other: The `other` parameter represents the object that we are comparing with the current object
        :return: The `__eq__` method is returning a boolean value.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> b = ManhattanArc(7 - 9, 7 + 9)
            >>> a == b
            False
            >>> c = ManhattanArc(-1, 9)
            >>> a == c
            True
        """
        if not isinstance(other, ManhattanArc):
            return NotImplemented
        return self.impl == other.impl

    def min_dist_with(self, other: "ManhattanArc[Any, Any]") -> int:
        """
        The `min_dist_with` function calculates the minimum rectilinear distance between two objects.

        :param other: The `other` parameter represents another object with which you want to calculate
            the minimum rectilinear distance

        :return: the minimum rectilinear distance between the two objects.

        Examples:
            >>> r1 = ManhattanArc(4 - 5, 4 + 5)
            >>> r2 = ManhattanArc(7 - 9, 7 + 9)
            >>> r1.min_dist_with(r2)
            7
        """
        # Note: take max of xcoord and ycoord
        x_dist = min_dist(self.impl.xcoord, other.impl.xcoord)
        y_dist = min_dist(self.impl.ycoord, other.impl.ycoord)
        return int(max(x_dist, y_dist))

    def enlarge_with(self, alpha: int) -> "ManhattanArc[T1, T2]":
        """
        The `enlarge_with` function takes an integer `alpha` and returns a new `ManhattanArc` object with
        enlarged coordinates.

        :param alpha: The parameter `alpha` is an integer that represents the factor by which the
            coordinates of the `ManhattanArc` object should be enlarged

        :type alpha: int

        :return: The `enlarge_with` method is returning a new `ManhattanArc` object with the enlarged coordinates.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> r = a.enlarge_with(1)
            >>> print(r)
            /[-2, 0], [8, 10]/
        """
        xcoord = enlarge(self.impl.xcoord, alpha)
        ycoord = enlarge(self.impl.ycoord, alpha)
        return ManhattanArc(xcoord, ycoord)

    def intersect_with(self, other: "ManhattanArc[T1, T2]") -> "ManhattanArc[T1, T2]":
        """
        The function calculates the intersection point between two ManhattanArc objects and returns a new
        ManhattanArc object with the coordinates of the intersection point.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the ManhattanArc class that we want to find the intersection with

        :return: a ManhattanArc object with the x-coordinate and y-coordinate of the intersection point
            between the self object and the other object.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> r = a.intersect_with(a)
            >>> print(r)
            /-1, 9/
        """
        point = self.impl.intersect_with(other.impl)
        return ManhattanArc(point.xcoord, point.ycoord)

    def get_center(self) -> Point[Any, Any]:
        """
        Calculates the center of the merging segment

        :return: The center of the merging segment.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> print(a.get_center())
            (4, 5)
        """
        center_point = self.impl.get_center()
        return center_point.inv_rotates()

    def get_lower_corner(self) -> Point[Any, Any]:
        """
        Calculates the lower corner of the merging segment

        :return: The lower corner of the merging segment.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> print(a.get_lower_corner())
            (4, 5)
        """
        lower_point = self.impl.lower_corner()
        return lower_point.inv_rotates()

    def get_upper_corner(self) -> Point[Any, Any]:
        """
        Calculates the upper corner of the merging segment

        :return: The upper corner of the merging segment.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> print(a.get_upper_corner())
            (4, 5)
        """
        upper_point = self.impl.upper_corner()
        return upper_point.inv_rotates()

    def _nearest_point_to(self, manhattan_arc: "ManhattanArc[Any, Any]") -> Point[Any, Any]:
        """
        Calculates the center of the merging segment

        :return: The center of the merging segment.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> print(a.nearest_point_to(Point(0, 0)))
            (4, 5)
        """
        nearest_pt = self.impl.nearest_to(manhattan_arc.impl)
        ic(nearest_pt)
        return nearest_pt.inv_rotates()

    def nearest_point_to(self, other: Point[int, int]) -> Point[Any, Any]:
        """
        Calculates the center of the merging segment

        :return: The center of the merging segment.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> print(a.nearest_point_to(Point(0, 0)))
            (4, 5)
        """
        ms = ManhattanArc.from_point(other)
        ic(self)
        ic(ms)
        return self._nearest_point_to(ms)

        # distance = self.min_dist_with(ms)
        # trr = ms.enlarge_with(distance)
        # lb = self.impl.lower_corner()
        # ub = self.impl.upper_corner()
        # m = self.impl.get_center()
        # if trr.impl.contains(lb):
        #     m = lb
        # elif trr.impl.contains(ub):
        #     m = ub
        # else:
        #     ic(self)
        # return m.inv_rotates()

    def merge_with(self, other: "ManhattanArc[T1, T2]", alpha: int) -> "ManhattanArc[T1, T2]":
        """
        The `merge_with` function takes another object as input, calculates the minimum Manhattan distance between
        the two objects, enlarges the objects based on the calculated distance, finds the intersection
        of the enlarged objects, and returns a new object with the coordinates of the intersection.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the class that we want to merge with the current instance

        :return: The `merge_with` method returns a new `ManhattanArc` object with the x-coordinate and
            y-coordinate of the intersection of the two objects being merged.

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> b = ManhattanArc(7 - 9, 7 + 9)
            >>> print(a.merge_with(b, 3))
            /[-4, 2], [12, 12]/
        """
        distance = self.min_dist_with(other)
        trr1 = self.enlarge_with(alpha)
        trr2 = other.enlarge_with(distance - alpha)
        return trr1.intersect_with(trr2)
