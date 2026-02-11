"""
ManhattanArc3D Class

This code defines a class called ManhattanArc3D, which represents a geometric object in a 2D space.
The purpose of this class is to handle operations on points, segments, or regions that are
rotated 45 degrees. It's designed to work with different types of coordinates, such as
integers, floats, or intervals.

The ManhattanArc3D class takes two inputs when creating an object: xcoord and ycoord. These
represent the coordinates of the object in the rotated space. The class doesn't produce a
specific output on its own, but it provides various methods to manipulate and interact
with these objects.

The class achieves its purpose by storing the coordinates in a Point object and providing
methods to perform operations like translation, enlargement, intersection, and merging
with other ManhattanArc3D instances. It uses a 45-degree rotated coordinate system, which allows
for easier calculations in certain geometric operations.

Some important logic flows in this code include:

1. The constructor (init) creates a Point object with the given coordinates.
2. The construct method creates a ManhattanArc3D from regular x and y coordinates by rotating
   them 45 degrees.
3. The translation methods (iadd and isub) move the object by adding or subtracting
   vector components.
4. The min_dist_with method calculates the minimum rectilinear distance between two
   ManhattanArc3D instances.
5. The enlarge_with method creates a new ManhattanArc3D with enlarged coordinates.
6. The intersect_with method finds the intersection point between two ManhattanArc3D instances.
7. The merge_with method combines two ManhattanArc3D instances by enlarging them based on their
   distance and finding their intersection.

These operations allow for complex geometric manipulations, which can be useful in various
applications such as computer graphics, game development, or computational geometry. The
class provides a high-level interface for working with these rotated geometric objects,
abstracting away some of the more complex mathematical calculations.
"""

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from icecream import ic  # type: ignore

from .manhattan_arc import ManhattanArc

# from .generic import min_dist
# from .interval import enlarge
from .point import Point

if TYPE_CHECKING:
    from .interval import Interval

T1 = TypeVar("T1", int, float, "Interval[int]", "Interval[float]")
T2 = TypeVar("T2", int, float, "Interval[int]", "Interval[float]")
T3 = TypeVar("T3", int, float, "Interval[int]", "Interval[float]")


class ManhattanArc3D(Generic[T1, T2, T3]):
    """
    Merging point, segment, or region ⛝

    A 45 degree rotated point, vertical or horizontal segment, or rectangle

    .. code-block:: text

                              +
                             /|           b
                            * +----<------o
                           /|
                          + +---------->--------o c
              a           |
              o-----<-----+

    """

    def __init__(self, ma1: ManhattanArc, ma2: ManhattanArc, ma3: ManhattanArc) -> None:
        """
        The function initializes an object with x and y coordinates and stores them in a Point object.

        :param xcoord: The parameter `xcoord` represents the x-coordinate of a point in a 2D space. It
            can be of any type `T1`

        :type xcoord: T1

        :param ycoord: The `ycoord` parameter represents the y-coordinate of a point in a
            two-dimensional space. It is used to initialize the `y` attribute of the `Point` object

        :type ycoord: T2
        """
        self.ma1 = ma1
        self.ma2 = ma2
        self.ma3 = ma3

    @classmethod
    def from_point(cls, pt: Point) -> "ManhattanArc3D[T1, T2, T3]":
        ma1 = ManhattanArc.from_point(Point(pt.xcoord.xcoord, pt.ycoord))  # x-y
        ma2 = ManhattanArc.from_point(Point(pt.ycoord, pt.xcoord.ycoord))  # y-z
        ma3 = ManhattanArc.from_point(pt.xcoord)  # x-z
        # assert pt.xcoord.ycoord == 0
        return cls(ma1, ma2, ma3)

    def __repr__(self) -> str:
        """
        The `__repr__` function returns a string representation of an `ManhattanArc3D` object, including the class
        name and its x and y coordinates, which is useful for debugging.

        :return: The `__repr__` method is returning a string representation of the `ManhattanArc3D` object.
        """
        return f"{self.__class__.__name__}({self.ma1}, {self.ma2}, {self.ma3})"

    def __str__(self) -> str:
        """
        The `__str__` function returns a string representation of an object, specifically in the format
        "/xcoord, ycoord/".

        :return: The method `__str__` returns a string representation of the object. In this case, it
            returns a string in the format "/xcoord, ycoord/" where xcoord and ycoord are the x and y
            coordinates of the object.
        """
        return f"/{self.ma1}, {self.ma2}, {self.ma3}/"

    def __eq__(self, other: object) -> bool:
        """
        The `__eq__` function checks if two `ManhattanArc3D` instances have the same `impl` attribute.

        :param other: The `other` parameter represents the object that we are comparing with the current object
        :return: The `__eq__` method is returning a boolean value.
        """
        if not isinstance(other, ManhattanArc3D):
            return NotImplemented
        return self.ma1 == other.ma1 and self.ma2 == other.ma2 and self.ma3 == other.ma3

    def min_dist_with(self, other: "ManhattanArc3D[Any, Any, Any]") -> int:
        """
        The `min_dist_with` function calculates the minimum rectilinear distance between two objects.

        :param other: The `other` parameter represents another object with which you want to calculate
            the minimum rectilinear distance

        :return: the minimum rectilinear distance between the two objects.
        """
        # Note: take max of xcoord and ycoord
        return (self.ma1.min_dist_with(other.ma1) + self.ma2.min_dist_with(other.ma2) + self.ma3.min_dist_with(other.ma3)) // 2

    def enlarge_with(self, alpha: int) -> "ManhattanArc3D[Any, Any, Any]":
        """
        The `enlarge_with` function takes an integer `alpha` and returns a new `ManhattanArc3D` object with
        enlarged coordinates.

        :param alpha: The parameter `alpha` is an integer that represents the factor by which the
            coordinates of the `ManhattanArc3D` object should be enlarged

        :type alpha: int

        :return: The `enlarge_with` method is returning a new `ManhattanArc3D` object with the enlarged coordinates.
        """
        ma1 = self.ma1.enlarge_with(alpha)
        ma2 = self.ma2.enlarge_with(alpha)
        ma3 = self.ma3.enlarge_with(alpha)
        return ManhattanArc3D(ma1, ma2, ma3)

    def intersect_with(self, other: "ManhattanArc3D[T1, T2, T3]") -> "ManhattanArc3D[T1, T2, T3]":
        """
        The function calculates the intersection point between two ManhattanArc3D objects and returns a new
        ManhattanArc3D object with the coordinates of the intersection point.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the ManhattanArc3D class that we want to find the intersection with

        :return: a ManhattanArc3D object with the x-coordinate and y-coordinate of the intersection point
            between the self object and the other object.
        """
        ma1 = self.ma1.intersect_with(other.ma1)
        ma2 = self.ma2.intersect_with(other.ma2)
        ma3 = self.ma3.intersect_with(other.ma3)
        return ManhattanArc3D(ma1, ma2, ma3)

    def get_center(self) -> Point[Any, Any]:
        """
        Calculates the center of the merging segment.

        :return: The center of the merging segment.
        """
        xy_point = self.ma1.get_center()  # x-y
        xz_point = self.ma3.get_center()  # x-z
        # assert xz_point.ycoord == 0
        return Point(xz_point, xy_point.ycoord)

    def get_lower_corner(self) -> Point[Any, Any]:
        """
        Calculates the lower corner of the merging segment

        :return: The lower corner of the merging segment.
        """
        xy_point = self.ma1.get_lower_corner()  # x-y
        xz_point = self.ma3.get_lower_corner()  # TODO: check
        # assert xz_point.ycoord == 0
        return Point(xz_point, xy_point.ycoord)

    def get_upper_corner(self) -> Point[Any, Any]:
        """
        Calculates the upper corner of the merging segment

        :return: The upper corner of the merging segment.
        """
        xy_point = self.ma1.get_upper_corner()  # TODO: check
        xz_point = self.ma3.get_upper_corner()  # TODO: check
        # assert xz_point.ycoord == 0
        return Point(xz_point, xy_point.ycoord)

    def nearest_point_to(self, other: Point) -> Point[Any, Any]:
        """
        Calculates the center of the merging segment

        :return: The center of the merging segment.
        """
        ms_arc = ManhattanArc3D.from_point(other)
        xy_point = self.ma1._nearest_point_to(ms_arc.ma1)
        yz_point = self.ma2._nearest_point_to(ms_arc.ma2)
        xz_point = self.ma3._nearest_point_to(ms_arc.ma3)
        ic(self)
        ic(other)
        ic(ms_arc)
        ic(xy_point)
        ic(yz_point)
        ic(xz_point)
        assert xy_point.ycoord == yz_point.xcoord
        assert yz_point.ycoord == xz_point.ycoord
        assert xy_point.xcoord == xz_point.xcoord
        return Point(xz_point, xy_point.ycoord)

        # distance = self.min_dist_with(ms)
        # trr1 = ms.ma1.enlarge_with(distance)  # TODO: check
        # trr2 = ms.ma2.enlarge_with(distance)  # TODO: check

        # pl1 = self.ma1.impl.lower_corner()  # TODO: check
        # pl2 = self.ma2.impl.lower_corner()  # TODO: check

        # pu1 = self.ma1.impl.upper_corner()  # TODO: check
        # pu2 = self.ma2.impl.upper_corner()  # TODO: check

        # pli1 = pl1.inv_rotates()
        # pli2 = pl2.inv_rotates()
        # pui1 = pu1.inv_rotates()
        # pui2 = pu2.inv_rotates()

        # nearest_point = self.get_center()
        # if trr1.impl.contains(pl1):
        #     if trr2.impl.contains(pl2):
        #         nearest_point = Point(Point(pli1.xcoord, pli2.ycoord), pli1.ycoord)
        #     elif trr2.impl.contains(pu2):
        #         nearest_point = Point(Point(pli1.xcoord, pui2.ycoord), pli1.ycoord)
        # elif trr1.impl.contains(pu1):
        #     if trr2.impl.contains(pl2):
        #         nearest_point = Point(Point(pui1.xcoord, pli2.ycoord), pui1.ycoord)
        #     elif trr2.impl.contains(pu2):
        #         nearest_point = Point(Point(pui1.xcoord, pui2.ycoord), pui1.ycoord)
        # else:
        #     ic()
        # return nearest_point

    def merge_with(self, other: "ManhattanArc3D", alpha: int) -> "ManhattanArc3D":
        """
        The `merge_with` function takes another object as input, calculates the minimum Manhattan distance between
        the two objects, enlarges the objects based on the calculated distance, finds the intersection
        of the enlarged objects, and returns a new object with the coordinates of the intersection.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the class that we want to merge with the current instance

        :return: The `merge_with` method returns a new `ManhattanArc3D` object with the x-coordinate and
            y-coordinate of the intersection of the two objects being merged.
        """
        distance = self.min_dist_with(other)
        trr1 = self.enlarge_with(alpha)
        trr2 = other.enlarge_with(distance - alpha)
        return trr1.intersect_with(trr2)
