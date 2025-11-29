"""
Point Class

This code defines a Point class, which represents a point in a 2D coordinate system. The
purpose of this class is to provide a way to work with points, perform operations on them,
and compare them with other points or geometric shapes.

The Point class takes two inputs when creating a new point: xcoord and ycoord. These
represent the x and y coordinates of the point, respectively. The class is designed to be
flexible, allowing these coordinates to be integers, floats, intervals, or even other
Point objects (for higher-dimensional points).

The class doesn't produce a specific output on its own, but it provides many methods that
can be used to manipulate points or get information about them. For example, you can add
or subtract vectors from points, check if points overlap or contain each other, find the
distance between points, and more.

The Point class achieves its purpose by storing the x and y coordinates and providing a
set of methods to work with these coordinates. It uses operator overloading to make it
easy to perform arithmetic operations with points, such as addition and subtraction. It
also includes comparison methods to determine the relative positions of points.

Some important operations in the class include:

1. Adding and subtracting vectors from points
2. Checking if points overlap or contain each other
3. Finding the minimum Manhattan distance between points
4. Creating a hull (bounding box) that contains two points
5. Finding the intersection of two points or shapes
6. Enlarging a point to create a rectangle around it

The class uses type hints and generics to make it flexible and usable with different
types of coordinates. It also includes many helper methods that use functions from other
modules (like generic, interval, and vector2) to perform calculations and comparisons.

Overall, this Point class provides a comprehensive set of tools for working with points
in a 2D space, making it easier for programmers to handle geometric calculations and
manipulations in their code.
"""

from typing import Any, Generic, TypeVar, Union

from .generic import (
    center,
    contain,
    displacement,
    intersection,
    lower,
    measure_of,
    min_dist,
    nearest,
    overlap,
    upper,
)
from .interval import enlarge, hull
from .vector2 import Vector2

T1 = TypeVar("T1")
T2 = TypeVar("T2")


class Point(Generic[T1, T2]):
    """
    Generic Rectilinear Point class (▪️, ──, │, or 🔲)
    """

    xcoord: T1
    ycoord: T2

    def __init__(self, xcoord: T1, ycoord: T2) -> None:
        """
        The function initializes an object with x and y coordinates.

        :param xcoord: The parameter `xcoord` is of type `T1` and represents the x-coordinate of a point

        :type xcoord: T1

        :param ycoord: The `ycoord` parameter is a variable that represents the y-coordinate of a point.
            It can be of any type (`T2`)

        :type ycoord: T2

        Examples:
            >>> a = Point(3, 4)
            >>> print(a)
            (3, 4)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> print(a3d)
            ((3, 4), 5)
        """
        self.xcoord: T1 = xcoord
        self.ycoord: T2 = ycoord

    def __repr__(self) -> str:
        """
        The `__repr__` function returns a string representation of a Point object, including the class
        name and its coordinates.

        :return: The `__repr__` method is returning a string representation of the `Point` object. The
            string includes the class name, and the x and y coordinates of the point

        Examples:
            >>> a = Point(3, 4)
            >>> repr(a)
            'Point(3, 4)'
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> repr(a3d)
            'Point(Point(3, 4), 5)'
        """
        return f"{self.__class__.__name__}({repr(self.xcoord)}, {repr(self.ycoord)})"

    def __str__(self) -> str:
        """
        The __str__ function returns a string representation of a Point object in the format (xcoord, ycoord).

        :return: The `__str__` method is returning a string representation of the object, which is the
            coordinates of the point in the format "(x, y)".

        Examples:
            >>> a = Point(3, 4)
            >>> print(a)
            (3, 4)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> print(a3d)
            ((3, 4), 5)
        """
        return "({self.xcoord}, {self.ycoord})".format(self=self)

    def width(self) -> Any:
        """
        Calculates the width of the point.

        :return: The width of the point.

        Examples:
            >>> a = Point(3, 4)
            >>> a.width()
            1
            >>> b = Point(3, 8)
            >>> b.width()
            1
        """
        return measure_of(self.xcoord)

    def height(self) -> Any:
        """
        Calculates the height of the point.

        :return: The height of the point.

        Examples:
            >>> a = Point(3, 4)
            >>> a.height()
            1
            >>> b = Point(3, 8)
            >>> b.height()
            1
        """
        return measure_of(self.ycoord)

    def measure(self) -> Any:
        """
        Calculates the measure (area, volume etc.) of the point.

        :return: The measure (area, volume etc.) of the point.

        Examples:
            >>> a = Point(3, 4)
            >>> a.measure()
            1
            >>> b = Point(3, 8)
            >>> b.measure()
            1
        """
        return measure_of(self.xcoord) * measure_of(self.ycoord)

    # def copy(self) -> "Point[T1, T2]":
    #     """
    #     The `copy` function returns a new instance of the same type as the current object, with the same
    #     x and y coordinates.
    #     :return: The `copy` method is returning a new instance of the same type as the current object.
    #
    #     Examples:
    #         >>> a = Point(3, 4)
    #         >>> b = a.copy()
    #         >>> print(b)
    #         (3, 4)
    #         >>> a3d = Point(a, 5)  # Point in 3d
    #         >>> b3d = a3d.copy()
    #         >>> print(b3d)
    #         ((3, 4), 5)
    #     """
    #     T = type(self)  # Type could be Point or Rectangle or others
    #     return T(self.xcoord, self.ycoord)

    def __lt__(self, other: "Point[T1, T2]") -> bool:
        """
        The `__lt__` function compares two points based on their x and y coordinates and returns True if
        the first point is less than the second point.

        :param other: The `other` parameter represents another instance of the `Point` class that we are
            comparing to the current instance

        :return: The `__lt__` method is returning a boolean value indicating whether the current
            instance is less than the `other` instance.

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> a < b
            True
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = Point(b, 1)  # Point in 3d
            >>> a3d > b3d
            False
            >>> b > a
            True
        """
        return (self.xcoord, self.ycoord) < (other.xcoord, other.ycoord)

    def __le__(self, other: "Point[T1, T2]") -> bool:
        """
        The `__le__` function compares two points and returns True if the first point is less than or
        equal to the second point based on their x and y coordinates.

        :param other: The `other` parameter represents another instance of the `Point` class that we are
            comparing to the current instance

        :return: The method `__le__` is returning a boolean value.

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> a <= b
            True
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = Point(b, 1)  # Point in 3d
            >>> a3d >= b3d
            False
            >>> b >= a
            True
        """
        return (self.xcoord, self.ycoord) <= (other.xcoord, other.ycoord)

    def __eq__(self, other: object) -> bool:
        """
        The `__eq__` function checks if two points have the same x and y coordinates.

        :param other: The `other` parameter represents the other object that we are comparing with the
            current object. In this case, it is used to compare the x and y coordinates of two `Point`
            objects to determine if they are equal

        :return: The `__eq__` method is returning a boolean value indicating whether the coordinates of
            the current point object (`self`) are equal to the coordinates of the other point object (`other`).

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> a == b
            False
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = Point(b, 1)  # Point in 3d
            >>> a3d != b3d
            True
            >>> a != b
            True
        """
        if not isinstance(other, Point):
            return NotImplemented
        return (self.xcoord, self.ycoord) == (other.xcoord, other.ycoord)

    def __iadd__(self, rhs: Vector2) -> "Point[T1, T2]":
        """
        The `__iadd__` method allows for in-place addition of a `Vector2` object to a `Point` object.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the vector that is
            being added to the current vector

        :type rhs: Vector2

        :return: The `self` object is being returned.

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

    def __add__(self, rhs: Vector2) -> "Point[T1, T2]":
        """
        The `__add__` method allows for addition of a `Vector2` object to a `Point` object, resulting in a
        new `Point` object with updated coordinates.

        :param rhs: rhs is the right-hand side operand of the addition operation. In this case, it is a
            Vector2 object that is being added to the current Point object

        :type rhs: Vector2

        :return: The `__add__` method is returning a new instance of the same type as `self` (which could be
            `Point`, `Rectangle`, or any other type). The new instance is created by adding the `x` and `y`
            coordinates of `self` with the `x` and `y` coordinates of `rhs` (the right-hand side operand).

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

    def __isub__(self, rhs: Vector2) -> "Point[T1, T2]":
        """
        The `__isub__` method subtracts the x and y coordinates of a `Vector2` object from the x and y
        coordinates of a `Point` object and returns the updated `Point` object.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the vector that is being
            subtracted from the current vector. In this case, `rhs` is an instance of the `Vector2` class

        :type rhs: Vector2

        :return: The method `__isub__` returns `self`.

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

    def __sub__(self, rhs: Vector2) -> "Point[T1, T2]":
        """
        The `__sub__` method subtracts the x and y coordinates of a given vector or point from the x and y
        coordinates of the current object and returns a new object of the same type.

        :param rhs: The parameter `rhs` represents the right-hand side operand of the subtraction operation.
            It can be either a `Vector2` or a `Point` object

        :type rhs: Vector2

        :return: The `__sub__` method returns a new instance of the same type as `self` (which could be
            `Point`, `Rectangle`, or any other type) with the x and y coordinates subtracted by the
            corresponding coordinates of `rhs` (another `Vector2` or `Point`).

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> b = a - v
            >>> print(b)
            (-2, -2)
        """
        T = type(self)  # Type could be Point or Rectangle or others
        return T(self.xcoord - rhs.x, self.ycoord - rhs.y)

    def displace(self, rhs: "Point[T1, T2]") -> Vector2:
        """
        Calculates the displacement vector from another point to this point.

        This method takes another `Point` object (`rhs`) as input and returns a `Vector2`
        object representing the displacement from `rhs` to the current point (`self`).

        :param rhs: The other point from which to calculate the displacement.
        :type rhs: Point[T1, T2]
        :return: A `Vector2` object representing the displacement.

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(1, 1)
            >>> print(a.displace(b))
            <2, 3>
            >>> c = Point(5, 6)
            >>> print(b.displace(c))
            <-4, -5>
        """
        return Vector2(
            displacement(self.xcoord, rhs.xcoord), displacement(self.ycoord, rhs.ycoord)
        )

    def flip(self) -> "Point[T2, T1]":
        """
        The `flip` function returns a new `Point` object with the x and y coordinates swapped.

        :return: The flip() method returns a new Point object with the x and y coordinates swapped.

        Examples:
            >>> a = Point(3, 4)
            >>> print(a.flip())
            (4, 3)
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6))  # Rectangle
            >>> print(r.flip())
            ([5, 6], [3, 4])
        """
        return Point(self.ycoord, self.xcoord)

    def rotates(self) -> "Point[T1, T2]":
        xcoord = self.xcoord - self.ycoord  # type: ignore
        ycoord = self.xcoord + self.ycoord  # type: ignore
        return Point(xcoord, ycoord)

    def inv_rotates(self) -> "Point[T1, T2]":
        xcoord = self.ycoord + (self.xcoord - self.ycoord) // 2  # type: ignore
        ycoord = (-self.xcoord + self.ycoord) // 2  # type: ignore
        return Point(xcoord, ycoord)

    def overlaps(self, other: "Point[T1, T2]") -> bool:
        """
        The `overlaps` function checks if two objects overlap by comparing their x and y coordinates.

        :param other: The `other` parameter represents another object that we want to check for overlap with
            the current object

        :return: a boolean value, indicating whether there is an overlap between the coordinates of the two objects.

        .. svgbob::
           :align: center

                 .----------.
                 | other    |
                 | .--------+---.
                 | |        |   |
                 '-+--------'   |
                   | self       |
                   '------------'

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> print(a.overlaps(b))
            False
            >>> c = Point(3, 4)
            >>> d = Point(3, 4)
            >>> print(c.overlaps(d))
            True
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6))  # Rectangle
            >>> print(r.overlaps(a))
            False
        """
        return overlap(self.xcoord, other.xcoord) and overlap(self.ycoord, other.ycoord)

    def contains(self, other: "Point[T1, T2]") -> bool:
        """
        The function checks if the x and y coordinates of one object are contained within the x and y
        coordinates of another object.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the class that we want to check if it is contained within the current
            instance

        :return: The `contains` method is returning a boolean value.

        .. svgbob::
           :align: center

            .-----------------.
            | self            |
            |   .---------.   |
            |   | other   |   |
            |   '---------'   |
            |                 |
            '-----------------'

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> print(a.contains(b))
            False
            >>> c = Point(3, 4)
            >>> d = Point(3, 4)
            >>> print(c.contains(d))
            True
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.contains(a))
            False
        """
        return contain(self.xcoord, other.xcoord) and contain(self.ycoord, other.ycoord)

    def blocks(self, other: "Point[T1, T2]") -> bool:
        """
        :param other: The `other` parameter is an object of the same type as `self`. It represents another
            instance of the class that the `blocks` method belongs to

        .. svgbob::
           :align: center

                    .------.
                    | self |
            .-------+------+---.
            | other |      |   |
            '-------+------+---'
                    |      |
                    '------'

        """
        return (
            contain(self.xcoord, other.xcoord)
            and contain(other.ycoord, self.ycoord)
            or contain(self.ycoord, other.ycoord)
            and contain(other.xcoord, self.xcoord)
        )

    def hull_with(self, other: "Point[T1, T2]") -> "Point[Any, Any]":
        """
        The `hull_with` function takes another object and returns a new object with the hull of the x and y
        coordinates of both objects.

        :param other: The `other` parameter is an object of the same type as `self`. It represents another
            instance of the class that the `hull_with` method belongs to

        :return: an instance of the same class as `self` (type `T`). The instance is created using the
            `hull` function, which takes the x-coordinates and y-coordinates of `self` and `other` as arguments.

        .. svgbob::
           :align: center

            .-----------.------.
            | self      |      |
            '-----------'      |
            | hull             |
            |                  |
            |      .-----------.
            |      | other     |
            '------'-----------'

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> print(a.hull_with(b))
            ([3, 5], [4, 6])
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.hull_with(r))
            ([3, 4], [5, 6])
        """
        return Point(hull(self.xcoord, other.xcoord), hull(self.ycoord, other.ycoord))

    def intersect_with(self, other: "Point[T1, T2]") -> "Point[Any, Any]":
        """
        The function `intersect_with` takes another object as input and returns a new object that
        represents the intersection of the x and y coordinates of the two objects.

        :param other: The "other" parameter is an object of the same type as the current object. It
            represents another instance of the class that has the same attributes and methods

        :return: The method `intersect_with` returns an instance of the same class as `self` (i.e.,
            `type(self)`). The instance is created using the `T` constructor and takes the intersection of
            the `xcoord` and `ycoord` attributes of `self` and `other`.

        .. svgbob::
           :align: center

                 .----------.
                 | other    |
                 | .--------+---.
                 | | inter  |   |
                 '-+--------'   |
                   | self       |
                   '------------'

        Examples:
            >>> a = Point(3, 5)
            >>> b = Point(4, 6)
            >>> print(a.intersect_with(a))
            (3, 5)
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.intersect_with(a))
            ([3, 3], [5, 5])
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.intersect_with(b))
            ([4, 4], [6, 6])
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.intersect_with(r))
            ([3, 4], [5, 6])
        """
        return Point(
            intersection(self.xcoord, other.xcoord),
            intersection(self.ycoord, other.ycoord),
        )

    def min_dist_with(self, other: "Point[T1, T2]") -> Any:
        """
        The function calculates the minimum Manhattan distance between two points using their x and y coordinates.

        :param other: The "other" parameter represents another object or point with which you want to
            calculate the minimum Manhattan distance. It is assumed that both the current object (self) and the other
            object have attributes xcoord and ycoord, which represent their respective x and y coordinates. The
            function calculates the minimum Manhattan distance between the

        :return: the sum of the minimum distances between the x-coordinates and the y-coordinates of two objects.

        .. svgbob::
           :align: center

            .-----------.
            | self      |
            '-----------'
                   |
                  dy
                   |
            .-----------.
            | other     |
            '-----------'

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> print(a.min_dist_with(b))
            4
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.min_dist_with(a))
            1
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.min_dist_with(b))
            1
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.min_dist_with(r))
            0
        """
        return min_dist(self.xcoord, other.xcoord) + min_dist(self.ycoord, other.ycoord)

    def nearest_to(self, other: "Point") -> "Point":
        """
        Calculates the point on this object that is nearest to another point.

        This method takes another `Point` object (`other`) and returns a new `Point`
        representing the location on the boundary or inside of `self` that is closest to
        `other`. This is particularly useful when `self` represents a geometric shape
        (like a rectangle, represented by a Point of Intervals) and `other` is a point.

        :param other: The other point to find the nearest location to.
        :type other: Point
        :return: A new `Point` object representing the nearest point on `self`.

        .. svgbob::
           :align: center

            .-----------.
            | self      |
            '-----------o nearest point
                        :
                        '~~~~~~~~o
                                other

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> print(a.nearest_to(b))
            (3, 4)
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.nearest_to(a))
            (3, 5)
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.nearest_to(b))
            (4, 6)
        """
        return Point(
            nearest(self.xcoord, other.xcoord), nearest(self.ycoord, other.ycoord)
        )

    def enlarge_with(self, alpha: int | float) -> "Point[Any, Any]":
        """
        Enlarges the point by a given amount in each dimension.

        This method takes a numerical value `alpha` and enlarges the point by that
        amount in both the x and y dimensions. If the point's coordinates are single
        values, they are converted into intervals. The result is a new object of the
        same type as `self` (e.g., a `Point` with `Interval` coordinates, representing
        a rectangle).

        :param alpha: The amount to enlarge the point by. This can be an integer or a float.
        :type alpha: float
        :return: A new object of the same type as `self` with enlarged coordinates.

        .. svgbob::
           :align: center

            .-------------------.
            |                   |
            |    .---------.    |
            |    | self    |    |
            |    '---------'    |
            |                   |
            '-------------------'
                           <----> alpha

        Examples:
            >>> a = Point(9, -1)
            >>> r = a.enlarge_with(1)
            >>> print(r)
            ([8, 10], [-2, 0])
            >>> r = a.enlarge_with(2)
            >>> print(r)
            ([7, 11], [-3, 1])
            >>> r = a.enlarge_with(0)
            >>> print(r)
            ([9, 9], [-1, -1])
        """
        xcoord = enlarge(self.xcoord, alpha)
        ycoord = enlarge(self.ycoord, alpha)
        return Point(xcoord, ycoord)

    def get_center(self) -> "Point[Any, Any]":
        """
        Calculates the center of the point.

        :return: The center of the point.

        Examples:
            >>> a = Point(3, 4)
            >>> a.get_center()
            Point(3, 4)
            >>> from physdes.interval import Interval
            >>> a = Point(Interval(3, 7), 4)
            >>> a.get_center()
            Point(5, 4)
        """
        return Point(center(self.xcoord), center(self.ycoord))

    def lower_corner(self) -> "Point[Any, Any]":
        """
        Calculates the lower corner of the point.

        :return: The lower corner of the point.

        Examples:
            >>> a = Point(3, 4)
            >>> a.lower_corner()
            Point(3, 4)
            >>> from physdes.interval import Interval
            >>> a = Point(Interval(3, 7), 4)
            >>> a.lower_corner()
            Point(3, 4)
        """
        return Point(lower(self.xcoord), lower(self.ycoord))

    def upper_corner(self) -> "Point[Any, Any]":
        """
        Calculates the upper corner of the point.

        :return: The upper corner of the point.

        Examples:
            >>> a = Point(3, 4)
            >>> a.upper_corner()
            Point(3, 4)
            >>> from physdes.interval import Interval
            >>> a = Point(Interval(3, 7), 4)
            >>> a.upper_corner()
            Point(7, 4)
        """
        return Point(upper(self.xcoord), upper(self.ycoord))
