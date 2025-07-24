"""
MergeObj Class

This code defines a class called MergeObj, which represents a geometric object in a 2D space. The purpose of this class is to handle operations on points, segments, or regions that are rotated 45 degrees. It's designed to work with different types of coordinates, such as integers, floats, or intervals.

The MergeObj class takes two inputs when creating an object: xcoord and ycoord. These represent the coordinates of the object in the rotated space. The class doesn't produce a specific output on its own, but it provides various methods to manipulate and interact with these objects.

The class achieves its purpose by storing the coordinates in a Point object and providing methods to perform operations like translation, enlargement, intersection, and merging with other MergeObj instances. It uses a 45-degree rotated coordinate system, which allows for easier calculations in certain geometric operations.

Some important logic flows in this code include:

1. The constructor (init) creates a Point object with the given coordinates.
2. The construct method creates a MergeObj from regular x and y coordinates by rotating them 45 degrees.
3. The translation methods (iadd and isub) move the object by adding or subtracting vector components.
4. The min_dist_with method calculates the minimum rectilinear distance between two MergeObj instances.
5. The enlarge_with method creates a new MergeObj with enlarged coordinates.
6. The intersect_with method finds the intersection point between two MergeObj instances.
7. The merge_with method combines two MergeObj instances by enlarging them based on their distance and finding their intersection.

These operations allow for complex geometric manipulations, which can be useful in various applications such as computer graphics, game development, or computational geometry. The class provides a high-level interface for working with these rotated geometric objects, abstracting away some of the more complex mathematical calculations.
"""

from typing import TYPE_CHECKING, Generic, TypeVar

from .generic import intersection, min_dist
from .interval import enlarge
from .point import Point
from .vector2 import Vector2

if TYPE_CHECKING:
    from .interval import Interval

T1 = TypeVar("T1", int, float, "Interval[int]", "Interval[float]")
T2 = TypeVar("T2", int, float, "Interval[int]", "Interval[float]")


class MergeObj(Generic[T1, T2]):
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
        The function initializes an object with x and y coordinates and stores them in a Point object.

        :param xcoord: The parameter `xcoord` represents the x-coordinate of a point in a 2D space. It
            can be of any type `T1`

        :type xcoord: T1

        :param ycoord: The `ycoord` parameter represents the y-coordinate of a point in a
            two-dimensional space. It is used to initialize the `y` attribute of the `Point` object

        :type ycoord: T2

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> print(a)
            /9, -1/
        """
        self.impl: Point[T1, T2] = Point(xcoord, ycoord)

    @staticmethod
    def construct(xcoord: int, ycoord: int) -> "MergeObj[int, int]":
        """
        The function constructs a MergeObj object from the given x and y coordinates.

        :param xcoord: An integer representing the x-coordinate of the point
        :type xcoord: int
        :param ycoord: The `ycoord` parameter represents the y-coordinate of a point in a Cartesian coordinate system
        :type ycoord: int
        :return: an instance of the `MergeObj` class with the `xcoord` and `ycoord` values of the `impl` object.

        Examples:
            >>> a = MergeObj.construct(4, 5)
            >>> print(a)
            /9, -1/
        """
        impl = Point(xcoord + ycoord, xcoord - ycoord)
        return MergeObj(impl.xcoord, impl.ycoord)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.impl.xcoord}, {self.impl.ycoord})"

    def __str__(self) -> str:
        """
        The `__str__` function returns a string representation of an object, specifically in the format
        "/xcoord, ycoord/".

        :return: The method `__str__` returns a string representation of the object. In this case, it
            returns a string in the format "/xcoord, ycoord/" where xcoord and ycoord are the x and y
            coordinates of the object.

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> print(a)
            /9, -1/
        """
        return f"/{self.impl.xcoord}, {self.impl.ycoord}/"

    def __eq__(self, other) -> bool:
        """
        The `__eq__` function checks if two `MergeObj` instances have the same `impl` attribute.

        :param other: The `other` parameter represents the object that we are comparing with the current object
        :return: The `__eq__` method is returning a boolean value.

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> b = MergeObj(7 + 9, 7 - 9)
            >>> a == b
            False
            >>> c = MergeObj(9, -1)
            >>> a == c
            True
        """
        return self.impl == other.impl

    def __iadd__(self, rhs: Vector2) -> "MergeObj[T1, T2]":
        """Translate by displacement

        The `__iadd__` method allows a `MergeObj` object to be translated by a given displacement vector.

        :param rhs: The parameter `rhs` is of type `Vector2`, which represents a 2-dimensional vector.
            It is used to specify the displacement that will be added to the current object

        :type rhs: Vector2

        :return: The method `__iadd__` returns an instance of the class `MergeObj[T1, T2]`.

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> a += Vector2(1, 2)
            >>> print(a)
            /12, -2/
        """
        self.impl.xcoord += rhs.x + rhs.y
        self.impl.ycoord += rhs.x - rhs.y
        return self

    def __isub__(self, rhs: Vector2) -> "MergeObj[T1, T2]":
        """
        The function subtracts the x and y coordinates of a Vector2 object from the x and y coordinates
        of a MergeObj object.

        :param rhs: The parameter `rhs` is of type `Vector2`, which represents a 2-dimensional vector
        :type rhs: Vector2
        :return: The method `__isub__` returns an instance of the class `MergeObj[T1, T2]`.

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> a -= Vector2(1, 2)
            >>> print(a)
            /6, 0/
        """
        self.impl.xcoord -= rhs.x + rhs.y
        self.impl.ycoord -= rhs.x - rhs.y
        return self

    def min_dist_with(self, other) -> int:
        """
        The `min_dist_with` function calculates the minimum rectilinear distance between two objects.

        :param other: The `other` parameter represents another object with which you want to calculate
            the minimum rectilinear distance

        :return: the minimum rectilinear distance between the two objects.

        Examples:
            >>> r1 = MergeObj(4 + 5, 4 - 5)
            >>> r2 = MergeObj(7 + 9, 7 - 9)
            >>> v = Vector2(5, 6)
            >>> r1.min_dist_with(r2)
            7
        """
        # Note: take max of xcoord and ycoord
        return max(
            min_dist(self.impl.xcoord, other.impl.xcoord),
            min_dist(self.impl.ycoord, other.impl.ycoord),
        )

    def enlarge_with(self, alpha: int):
        """
        The `enlarge_with` function takes an integer `alpha` and returns a new `MergeObj` object with
        enlarged coordinates.

        :param alpha: The parameter `alpha` is an integer that represents the factor by which the
            coordinates of the `MergeObj` object should be enlarged

        :type alpha: int

        :return: The `enlarge_with` method is returning a new `MergeObj` object with the enlarged coordinates.

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> r = a.enlarge_with(1)
            >>> print(r)
            /[8, 10], [-2, 0]/
        """
        xcoord = enlarge(self.impl.xcoord, alpha)  # TODO: check
        ycoord = enlarge(self.impl.ycoord, alpha)  # TODO: check
        return MergeObj(xcoord, ycoord)  # TODO

    def intersect_with(self, other):
        """
        The function calculates the intersection point between two MergeObj objects and returns a new
        MergeObj object with the coordinates of the intersection point.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the MergeObj class that we want to find the intersection with

        :return: a MergeObj object with the x-coordinate and y-coordinate of the intersection point
            between the self object and the other object.

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> r = a.intersect_with(a)
            >>> print(r)
            /9, -1/
        """
        point = self.impl.intersect_with(other.impl)  # TODO
        return MergeObj(point.xcoord, point.ycoord)

    def merge_with(self, other):
        """
        The `merge_with` function takes another object as input, calculates the minimum Manhattan distance between
        the two objects, enlarges the objects based on the calculated distance, finds the intersection
        of the enlarged objects, and returns a new object with the coordinates of the intersection.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the class that we want to merge with the current instance

        :return: The `merge_with` method returns a new `MergeObj` object with the x-coordinate and
            y-coordinate of the intersection of the two objects being merged.

        Examples:
            >>> s1 = MergeObj(200 + 600, 200 - 600)
            >>> s2 = MergeObj(500 + 900, 500 - 900)
            >>> m1 = s1.merge_with(s2)
            >>> print(m1)
            /[1100, 1100], [-700, -100]/
        """
        alpha = self.min_dist_with(other)
        half = alpha // 2
        trr1 = enlarge(self.impl, half)
        trr2 = enlarge(other.impl, alpha - half)
        impl = intersection(trr1, trr2)
        return MergeObj(impl.xcoord, impl.ycoord)
