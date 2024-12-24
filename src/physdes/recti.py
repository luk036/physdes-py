r"""
Rectangle and Segment Classes (src\physdes\recti.py)

This code defines classes for working with rectangles and line segments in a 2D coordinate system. The main purpose is to provide a way to represent and manipulate these geometric shapes in a program.

The code introduces three main classes: Rectangle, VSegment (vertical segment), and HSegment (horizontal segment). These classes are built on top of more basic classes like Point and Interval, which are imported at the beginning of the file.

The Rectangle class represents a rectangular shape. It takes two inputs when created: an x-coordinate interval and a y-coordinate interval. These intervals define the boundaries of the rectangle. For example, you could create a rectangle from x-coordinates 3 to 4 and y-coordinates 5 to 6.

The Rectangle class provides several useful methods. You can get the lower-left and upper-right corners of the rectangle, check if a point or another rectangle is inside it, calculate its width, height, and area, and even flip it (swap its x and y coordinates).

The VSegment and HSegment classes represent vertical and horizontal line segments, respectively. A VSegment is defined by a single x-coordinate and a y-coordinate interval, while an HSegment is defined by an x-coordinate interval and a single y-coordinate.

These segment classes also have methods to check if they contain a point or another segment, and to flip themselves (turning a vertical segment into a horizontal one, or vice versa).

The code achieves its purpose by using object-oriented programming principles. Each class encapsulates the data and behavior related to its specific geometric shape. The classes inherit from a Point class, which allows them to reuse some common functionality.

An important aspect of the logic is how the classes use the Interval class to represent ranges of coordinates. This allows for easy checking of whether one range contains another, which is crucial for the "contains" methods in each class.

The code doesn't produce any output on its own. Instead, it provides a set of tools (the classes and their methods) that a programmer can use to work with rectangles and line segments in their own programs. For example, you could use these classes to implement a simple drawing program or to solve geometric problems.

Overall, this code provides a foundation for working with basic 2D geometric shapes in a structured and object-oriented way, making it easier to perform common operations on these shapes in more complex programs.
"""

from .interval import Interval
from .point import Point


class Rectangle(Point[Interval[int], Interval[int]]):
    """Axis-parallel Rectangle"""

    def __init__(self, xcoord: Interval, ycoord: Interval):
        """
        The `__init__` function initializes a Rectangle object with x and y coordinates.

        :param xcoord: The x-coordinate interval of the rectangle. It represents the range of x-values that
            the rectangle spans

        :type xcoord: Interval

        :param ycoord: The `ycoord` parameter represents the interval of values for the y-coordinate of a
            rectangle. It is an instance of the `Interval` class, which represents a range of values. The
            `Interval` class typically has two attributes, `start` and `end`, which define the lower and upper

        :type ycoord: Interval

        Examples:
            >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
            >>> print(a)
            ([3, 4], [5, 6])
            >>> a3d = Rectangle(a, Interval(7, 8))  # Rectangle in 3d
            >>> print(a3d)
            (([3, 4], [5, 6]), [7, 8])
        """
        Point.__init__(self, xcoord, ycoord)

    @property
    def ll(self) -> Point[int, int]:
        """
        The `ll` function returns the lower left point of a rectangle.

        :return: The `ll` method is returning a `Point` object with the lower left coordinates of the rectangle.

        Examples:
            >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
            >>> print(a.ll)
            (3, 5)
        """
        return Point(self.xcoord.lb, self.ycoord.lb)

    @property
    def ur(self) -> Point[int, int]:
        """
        The `ur` function returns the upper right coordinates of a rectangle.

        :return: The `ur` method is returning a `Point` object with the upper right coordinates of a rectangle.

        Examples:
            >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
            >>> print(a.ur)
            (4, 6)
        """
        return Point(self.xcoord.ub, self.ycoord.ub)

    # def copy(self):
    #     """[summary]
    #
    #     Returns:
    #         [type]: [description]
    #
    #     Examples:
    #         >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
    #         >>> print(a.copy())
    #         ([3, 4], [5, 6])
    #         >>> a3d = Rectangle(a, Interval(7, 8))  # Rectangle in 3d
    #         >>> print(a3d.copy())
    #         (([3, 4], [5, 6]), [7, 8])
    #     """
    #     return Rectangle(self.xcoord, self.ycoord)
    #
    # def __eq__(self, rhs) -> bool:
    #     return self.xcoord == rhs.xcoord and self.ycoord == rhs.ycoord

    def flip(self) -> "Rectangle":
        """
        The `flip` function returns a new `Rectangle` object with the x and y coordinates swapped.

        :return: The `flip` method is returning a new `Rectangle` object with the x and y coordinates swapped.

        Note:
            Overriding the `flip` function of the `Point` class. The `flip` function of the `Point`
            class is used to flip the x and y coordinates of a `Point` object. The `flip` function of the
            `Rectangle` class is used to flip the x and y coordinates of a `Rectangle` object.

        Examples:
            >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
            >>> print(a.flip())
            ([5, 6], [3, 4])
            >>> a3d = Rectangle(a, Interval(7, 8))  # Rectangle in 3d
            >>> print(a3d.flip())
            ([7, 8], ([3, 4], [5, 6]))
        """
        return Rectangle(self.ycoord, self.xcoord)

    def contains(self, other: Point) -> bool:
        """
        The `contains` function checks if a given point is contained within a rectangle.

        :param other: The `other` parameter can be an instance of the `Point`, `VSegment`, `HSegment`, or
            `Rectangle` class

        :type other: Point

        :return: The `contains` method is returning a boolean value, indicating whether the given `other`
            object is contained within the current object.

        Examples:
            >>> a = Rectangle(Interval(30, 40), Interval(50, 60))
            >>> a.contains(Point(36, 53))
            True
            >>> a.contains(Rectangle(Interval(32, 38), Interval(51, 57)))
            True
            >>> a.contains(Rectangle(Interval(32, 38), Interval(51, 67)))
            False
        """
        return self.xcoord.contains(other.xcoord) and self.ycoord.contains(other.ycoord)

    def width(self) -> int:
        """
        The `width` function returns the length of the x-coordinate interval of a rectangle.

        :return: The `width` method is returning the length of the x-coordinate interval of the rectangle.

        Examples:
            >>> a = Rectangle(Interval(30, 40), Interval(50, 62))
            >>> a.width()
            10
        """
        return self.xcoord.length()

    def height(self) -> int:
        """
        The `height` function returns the length of the y-coordinate interval of a rectangle.

        :return: The height of the rectangle, which is the length of the y-coordinate interval.

        Examples:
            >>> a = Rectangle(Interval(30, 40), Interval(50, 62))
            >>> a.height()
            12
        """
        return self.ycoord.length()

    def area(self) -> int:
        """
        The `area` function calculates the area of a rectangle using the lengths of its x and y coordinates.

        :return: The area of the rectangle, which is an integer.

        Examples:
            >>> a = Rectangle(Interval(30, 40), Interval(50, 62))
            >>> a.area()
            120
        """
        return self.xcoord.length() * self.ycoord.length()


class VSegment(Point[int, Interval[int]]):
    """
    Represents a VSegment.
    """

    def contains(self, other: Point) -> bool:
        """
        The `contains` function checks if a given point is contained within a vertical segment.

        :param other: The "other" parameter is of type Point. It represents another point that we want to
            check if it is contained within the current point

        :type other: Point

        :return: a boolean value, indicating whether the given point `other` is contained within the current point object.

        Examples:
            >>> a = VSegment(5, Interval(30, 40))
            >>> a.contains(Point(5, 33))
            True
            >>> a.contains(VSegment(5, Interval(33, 38)))
            True
            >>> a.contains(VSegment(6, Interval(33, 38)))
            False
        """
        return self.xcoord == other.xcoord and self.ycoord.contains(other.ycoord)

    def flip(self) -> "HSegment":
        """
        The `flip` function returns a new `HSegment` object with the x and y coordinates swapped.

        :return: The flip() method is returning an instance of the HSegment class.

        Note:
            Overriding the `flip` method of the `Point` class.

        Examples:
            >>> a = VSegment(5, Interval(30, 40))
            >>> print(a.flip())
            ([30, 40], 5)
        """
        return HSegment(self.ycoord, self.xcoord)


class HSegment(Point[Interval[int], int]):
    """
    Represents a HSegment.
    """

    def contains(self, other) -> bool:
        """
        The `contains` function checks if a given object is contained within another object based on their
        coordinates.

        :param other: The `other` parameter represents another object that we want to check if it is
            contained within the current object. It can be either a `Point` or a `HSegment` object

        :return: The function `contains` returns a boolean value indicating whether `other` is contained
            within `self`.

        Examples:
            >>> a = HSegment(Interval(30, 40), 5)
            >>> a.contains(Point(33, 5))
            True
            >>> a.contains(HSegment(Interval(33, 38), 5))
            True
            >>> a.contains(HSegment(Interval(33, 38), 6))
            False
        """
        return self.ycoord == other.ycoord and self.xcoord.contains(other.xcoord)

    def flip(self) -> VSegment:
        """
        The `flip` function returns a `VSegment` object with the y-coordinate and x-coordinate swapped.

        :return: The flip() method is returning a VSegment object.

        Note:
            Overriding the `flip` method of the `Point` class.

        Examples:
            >>> a = HSegment(Interval(30, 40), 5)
            >>> print(a.flip())
            (5, [30, 40])
        """
        return VSegment(self.ycoord, self.xcoord)
