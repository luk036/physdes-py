"""
Point Class

This code defines a Point class, which represents a point in a 2D coordinate system. The purpose of this class is to provide a way to work with points, perform operations on them, and compare them with other points or geometric shapes.

The Point class takes two inputs when creating a new point: xcoord and ycoord. These represent the x and y coordinates of the point, respectively. The class is designed to be flexible, allowing these coordinates to be integers, floats, intervals, or even other Point objects (for higher-dimensional points).

The class doesn't produce a specific output on its own, but it provides many methods that can be used to manipulate points or get information about them. For example, you can add or subtract vectors from points, check if points overlap or contain each other, find the distance between points, and more.

The Point class achieves its purpose by storing the x and y coordinates and providing a set of methods to work with these coordinates. It uses operator overloading to make it easy to perform arithmetic operations with points, such as addition and subtraction. It also includes comparison methods to determine the relative positions of points.

Some important operations in the class include:

1. Adding and subtracting vectors from points
2. Checking if points overlap or contain each other
3. Finding the minimum Manhattan distance between points
4. Creating a hull (bounding box) that contains two points
5. Finding the intersection of two points or shapes
6. Enlarging a point to create a rectangle around it

The class uses type hints and generics to make it flexible and usable with different types of coordinates. It also includes many helper methods that use functions from other modules (like generic, interval, and vector2) to perform calculations and comparisons.

Overall, this Point class provides a comprehensive set of tools for working with points in a 2D space, making it easier for programmers to handle geometric calculations and manipulations in their code.
"""

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from .generic import contain, displacement, intersection, min_dist, overlap
from .interval import enlarge, hull
from .vector2 import Vector2

if TYPE_CHECKING:
    from .interval import Interval

T1 = TypeVar("T1", int, float, "Interval[int]", "Interval[float]", "Point[Any, Any]")
T2 = TypeVar("T2", int, float, "Interval[int]", "Interval[float]", "Point[Any, Any]")


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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.xcoord}, {self.ycoord})"

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

    def __lt__(self, other) -> bool:
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
        """
        return (self.xcoord, self.ycoord) < (other.xcoord, other.ycoord)

    def __le__(self, other) -> bool:
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
        """
        return (self.xcoord, self.ycoord) <= (other.xcoord, other.ycoord)

    def __eq__(self, other) -> bool:
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
        """
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

    def displace(self, rhs: "Point[T1, T2]"):  # TODO: what is the type?
        """
        The `displace` function takes a `Vector` or `Point` object as an argument and returns a new
        `Vector2` object representing the displacement between the two points.

        :param rhs: The parameter `rhs` is of type `"Point[T1, T2]"`, which means it can be either a `Vector2` or a `Point` object
        :type rhs: "Point[T1, T2]"
        :return: The `displace` method is returning a `Vector2` object.

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> b = a - v
            >>> print(b)
            (-2, -2)
            >>> print(a.displace(b))
            <5, 6>
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

    def overlaps(self, other) -> bool:
        """
        The `overlaps` function checks if two objects overlap by comparing their x and y coordinates.

        :param other: The `other` parameter represents another object that we want to check for overlap with
            the current object

        :return: a boolean value, indicating whether there is an overlap between the coordinates of the two objects.

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> print(a.overlaps(b))
            False
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6))  # Rectangle
            >>> print(r.overlaps(a))
            False
        """
        return overlap(self.xcoord, other.xcoord) and overlap(self.ycoord, other.ycoord)

    def contains(self, other) -> bool:
        """
        The function checks if the x and y coordinates of one object are contained within the x and y
        coordinates of another object.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the class that we want to check if it is contained within the current
            instance

        :return: The `contains` method is returning a boolean value.

        Examples:
            >>> a = Point(3, 4)
            >>> b = Point(5, 6)
            >>> print(a.contains(b))
            False
            >>> from physdes.interval import Interval
            >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
            >>> print(r.contains(a))
            False
        """
        return contain(self.xcoord, other.xcoord) and contain(self.ycoord, other.ycoord)

    def hull_with(self, other):
        """
        The `hull_with` function takes another object and returns a new object with the hull of the x and y
        coordinates of both objects.

        :param other: The `other` parameter is an object of the same type as `self`. It represents another
            instance of the class that the `hull_with` method belongs to

        :return: an instance of the same class as `self` (type `T`). The instance is created using the
            `hull` function, which takes the x-coordinates and y-coordinates of `self` and `other` as arguments.

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
        T = type(self)
        return T(hull(self.xcoord, other.xcoord), hull(self.ycoord, other.ycoord))

    # >>> a = Point(3, 4)
    # >>> r = Point(Interval(3, 4), Interval(5, 6)) # Rectangle
    # >>> print(r.intersect_with(a))
    def intersect_with(self, other):
        """
        The function `intersect_with` takes another object as input and returns a new object that
        represents the intersection of the x and y coordinates of the two objects.

        :param other: The "other" parameter is an object of the same type as the current object. It
            represents another instance of the class that has the same attributes and methods

        :return: The method `intersect_with` returns an instance of the same class as `self` (i.e.,
            `type(self)`). The instance is created using the `T` constructor and takes the intersection of
            the `xcoord` and `ycoord` attributes of `self` and `other`.

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
        T = type(self)
        return T(
            intersection(self.xcoord, other.xcoord),
            intersection(self.ycoord, other.ycoord),
        )

    def min_dist_with(self, other):
        """
        The function calculates the minimum Manhattan distance between two points using their x and y coordinates.

        :param other: The "other" parameter represents another object or point with which you want to
            calculate the minimum Manhattan distance. It is assumed that both the current object (self) and the other
            object have attributes xcoord and ycoord, which represent their respective x and y coordinates. The
            function calculates the minimum Manhattan distance between the

        :return: the sum of the minimum distances between the x-coordinates and the y-coordinates of two objects.

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

    def enlarge_with(self, alpha):  # TODO: what is the type?
        """
        The `enlarge_with` function takes a parameter `alpha` and returns a new instance of the same type
        with the x and y coordinates enlarged by `alpha`.

        :param alpha: The `alpha` parameter is a value that determines the amount by which the coordinates
            of the point should be enlarged

        :return: The `enlarge_with` method returns an instance of the same type as `self` with the enlarged
            coordinates.

        Examples:
            >>> a = Point(9, -1)
            >>> r = a.enlarge_with(1)
            >>> print(r)
            ([8, 10], [-2, 0])
            >>> r = a.enlarge_with(2)
            >>> print(r)
            ([7, 11], [-3, 1])
            >>> r = a.enlarge_with(3)
            >>> print(r)
            ([6, 12], [-4, 2])
            >>> r = a.enlarge_with(4)
            >>> print(r)
            ([5, 13], [-5, 3])
        """
        xcoord = enlarge(self.xcoord, alpha)
        ycoord = enlarge(self.ycoord, alpha)
        T = type(self)
        return T(xcoord, ycoord)
