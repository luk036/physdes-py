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

from typing import TYPE_CHECKING, Any, Generic, TypeVar

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

    Examples:
        >>> arc = ManhattanArc(-1, 9)
        >>> print(arc)
        /-1, 9/

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
        The function initializes an object with x and y coordinates and stores them in a Point object.

        :param xcoord: The parameter `xcoord` represents the x-coordinate of a point in a 2D space. It
            can be of any type `T1`

        :type xcoord: T1

        :param ycoord: The `ycoord` parameter represents the y-coordinate of a point in a
            two-dimensional space. It is used to initialize the `y` attribute of the `Point` object

        :type ycoord: T2

        Examples:
            >>> a = ManhattanArc(4 - 5, 4 + 5)
            >>> print(a)
            /-1, 9/
        """
        self.impl: Point[T1, T2] = Point(xcoord, ycoord)

    @classmethod
    def from_point(cls, pt: Point) -> "ManhattanArc[Any, Any]":
        """
        Constructs a ManhattanArc from a regular 2D Point by rotating its coordinates by 45 degrees.

        This method effectively transforms a point from the standard Cartesian coordinate system
        to the 45-degree rotated coordinate system used by ManhattanArc.

        Args:
            pt: The input 2D Point object.

        Returns:
            A new ManhattanArc instance representing the rotated point.

        Examples:
            >>> from physdes.point import Point
            >>> p = Point(4, 5)
            >>> arc = ManhattanArc.from_point(p)
            >>> print(arc)
            /-1, 9/
            >>> arc.impl.xcoord
            -1
            >>> arc.impl.ycoord
            9
        """
        pt_xformed = pt.rotates()
        return cls(pt_xformed.xcoord, pt_xformed.ycoord)

    @staticmethod
    def construct(xcoord: int, ycoord: int) -> "ManhattanArc[int, int]":
        """
        The function constructs a ManhattanArc object from the given x and y coordinates.

        :param xcoord: An integer representing the x-coordinate of the point
        :type xcoord: int
        :param ycoord: The `ycoord` parameter represents the y-coordinate of a point in a Cartesian coordinate system
        :type ycoord: int
        :return: an instance of the `ManhattanArc` class with the `xcoord` and `ycoord` values of the `impl` object.

        Examples:
            >>> a = ManhattanArc.construct(4, 5)
            >>> print(a)
            /-1, 9/
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
            >>> r1 = ManhattanArc.construct(4, 5)
            >>> r2 = ManhattanArc.construct(7, 9)
            >>> r1.min_dist_with(r2)
            7
            >>> r3 = ManhattanArc.construct(1, 1)
            >>> r4 = ManhattanArc.construct(1, 1)
            >>> r3.min_dist_with(r4)
            0
        """
        # Calculate the Manhattan distance between the x-coordinates and y-coordinates
        # of the two ManhattanArc instances. The minimum distance between the arcs
        # is the maximum of these two individual coordinate distances.
        return max(
            min_dist(self.impl.xcoord, other.impl.xcoord),
            min_dist(self.impl.ycoord, other.impl.ycoord),
        )

    def enlarge_with(self, alpha: int) -> "ManhattanArc[Any, Any]":
        """
        The `enlarge_with` function takes an integer `alpha` and returns a new `ManhattanArc` object with
        enlarged coordinates.

        :param alpha: The parameter `alpha` is an integer that represents the factor by which the
            coordinates of the `ManhattanArc` object should be enlarged

        :type alpha: int

        :return: The `enlarge_with` method is returning a new `ManhattanArc` object with the enlarged coordinates.

        Examples:
            >>> a = ManhattanArc.construct(4, 5)
            >>> r = a.enlarge_with(1)
            >>> print(r)
            /[-2, 0], [8, 10]/
            >>> r.impl.xcoord
            Interval(-2, 0)
            >>> r.impl.ycoord
            Interval(8, 10)
        """
        # Enlarge both the x and y coordinates of the internal Point object
        # by the given alpha value. This effectively expands the ManhattanArc.
        xcoord = enlarge(self.impl.xcoord, alpha)
        ycoord = enlarge(self.impl.ycoord, alpha)
        # Create and return a new ManhattanArc with the enlarged coordinates.
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
            >>> a = ManhattanArc.construct(4, 5)
            >>> r = a.intersect_with(a)
            >>> print(r)
            /-1, 9/
            >>> r.impl.xcoord
            -1
            >>> r.impl.ycoord
            9
        """
        # Calculate the intersection of the internal Point objects.
        # This operation is handled by the Point class, which can intersect
        # two 2D intervals (or points).
        point = self.impl.intersect_with(other.impl)
        # Return a new ManhattanArc instance from the resulting intersected Point.
        return ManhattanArc(point.xcoord, point.ycoord)

    def get_center(self) -> Point[Any, Any]:
        """
        Calculates the center of the ManhattanArc in the original (unrotated) coordinate system.

        This involves getting the center of the internal Point representation and then
        inverse-rotating it to transform back to the standard Cartesian coordinates.

        :return: A Point object representing the center of the ManhattanArc in the original coordinate system.

        Examples:
            >>> arc = ManhattanArc.construct(4, 5)
            >>> print(arc.get_center())
            (4, 5)
            >>> arc = ManhattanArc.construct(10, 20)
            >>> print(arc.get_center())
            (10, 20)
        """
        # Get the center of the internal Point representation (in rotated coordinates).
        m = self.impl.get_center()
        # Inverse-rotate the center point to get its coordinates in the original system.
        return m.inv_rotates()

    def get_lower_corner(self) -> Point[Any, Any]:
        """
        Calculates the lower corner of the ManhattanArc in the original (unrotated) coordinate system.

        This involves getting the lower corner of the internal Point representation and then
        inverse-rotating it to transform back to the standard Cartesian coordinates.

        :return: A Point object representing the lower corner of the ManhattanArc in the original coordinate system.

        Examples:
            >>> arc = ManhattanArc.construct(4, 5)
            >>> print(arc.get_lower_corner())
            (4, 5)
            >>> arc = ManhattanArc.construct(10, 20)
            >>> print(arc.get_lower_corner())
            (10, 20)
        """
        # Get the lower corner of the internal Point representation (in rotated coordinates).
        m = self.impl.lower_corner()
        # Inverse-rotate the lower corner point to get its coordinates in the original system.
        return m.inv_rotates()

    def get_upper_corner(self) -> Point[Any, Any]:
        """
        Calculates the upper corner of the ManhattanArc in the original (unrotated) coordinate system.

        This involves getting the upper corner of the internal Point representation and then
        inverse-rotating it to transform back to the standard Cartesian coordinates.

        :return: A Point object representing the upper corner of the ManhattanArc in the original coordinate system.

        Examples:
            >>> arc = ManhattanArc.construct(4, 5)
            >>> print(arc.get_upper_corner())
            (4, 5)
            >>> arc = ManhattanArc.construct(10, 20)
            >>> print(arc.get_upper_corner())
            (10, 20)
        """
        # Get the upper corner of the internal Point representation (in rotated coordinates).
        m = self.impl.upper_corner()
        # Inverse-rotate the upper corner point to get its coordinates in the original system.
        return m.inv_rotates()

    def nearest_point_to(self, other: Point[int, int]) -> Point[Any, Any]:
        """
        Finds the point within this ManhattanArc that is nearest to a given target Point.

        This method first converts the target Point into a ManhattanArc, then calculates
        the minimum distance between the two arcs. It then enlarges the target arc by
        this distance and checks if the lower corner, upper corner, or center of the
        current arc's internal representation falls within the enlarged target arc.
        The point that satisfies this condition (or the center if none do) is returned
        after inverse rotation.

        :param other: The target Point to find the nearest point to.
        :type other: Point[int, int]

        :return: A Point object representing the nearest point in this ManhattanArc to the target Point.

        Examples:
            >>> from physdes.point import Point
            >>> arc = ManhattanArc.construct(4, 5)
            >>> target = Point(0, 0)
            >>> print(arc.nearest_point_to(target))
            (4, 5)
            >>> arc2 = ManhattanArc.construct(10, 10)
            >>> target2 = Point(12, 12)
            >>> print(arc2.nearest_point_to(target2))
            (10, 10)
        """
        # Convert the target Point to a ManhattanArc for distance calculation.
        ms = ManhattanArc.from_point(other)
        # Calculate the minimum distance between the current arc and the target arc.
        distance = self.min_dist_with(ms)
        # Enlarge the target arc by the calculated distance.
        trr = ms.enlarge_with(distance)
        # Get the lower and upper corners of the current arc's internal representation.
        lb = self.impl.lower_corner()
        ub = self.impl.upper_corner()
        # Initialize the nearest point to the center of the current arc.
        m = self.impl.get_center()
        # Check if the lower corner of the current arc is contained within the enlarged target arc.
        if trr.impl.contains(lb):
            m = lb
        # Check if the upper corner of the current arc is contained within the enlarged target arc.
        elif trr.impl.contains(ub):
            m = ub
        # If neither corner is contained, the center is considered the nearest point.
        else:
            ic(
                distance
            )  # This line is likely for debugging and can be removed in production.
        # Inverse-rotate the found point to return it in the original coordinate system.
        return m.inv_rotates()

    def merge_with(
        self, other: "ManhattanArc[T1, T2]", alpha: int
    ) -> "ManhattanArc[T1, T2]":
        """
        The `merge_with` function takes another object as input, calculates the minimum Manhattan distance between
        the two objects, enlarges the objects based on the calculated distance, finds the intersection
        of the enlarged objects, and returns a new object with the coordinates of the intersection.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the class that we want to merge with the current instance

        :return: The `merge_with` method returns a new `ManhattanArc` object with the x-coordinate and
            y-coordinate of the intersection of the two objects being merged.

        Examples:
            >>> a = ManhattanArc.construct(4, 5)
            >>> b = ManhattanArc.construct(7, 9)
            >>> print(a.merge_with(b, 3))
            /[-4, 2], [12, 12]/
            >>> c = ManhattanArc.construct(1, 1)
            >>> d = ManhattanArc.construct(1, 1)
            >>> print(c.merge_with(d, 0))
            /[0, 0], [2, 2]/
        """
        # Calculate the minimum distance between the current ManhattanArc and the other ManhattanArc.
        distance = self.min_dist_with(other)
        # Enlarge the current ManhattanArc by 'alpha'.
        trr1 = self.enlarge_with(alpha)
        # Enlarge the other ManhattanArc by the remaining distance (distance - alpha).
        # This ensures that the total enlargement covers the distance between them.
        trr2 = other.enlarge_with(distance - alpha)
        # Find the intersection of the two enlarged ManhattanArcs' internal Point representations.
        localimpl = trr1.impl.intersect_with(trr2.impl)
        # Return a new ManhattanArc constructed from the intersection result.
        return ManhattanArc(localimpl.xcoord, localimpl.ycoord)
