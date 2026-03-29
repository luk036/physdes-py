"""
ManhattanArc3D Class

This code defines a class called ManhattanArc3D, which represents a geometric object in a 3D space.
The purpose of this class is to handle operations on points, segments, or regions that are
rotated 45 degrees. It's designed to work with different types of coordinates, such as
integers, floats, or intervals.

The ManhattanArc3D class takes four inputs when creating an object: xcoord, ycoord, zcoord, and wcoord. These
represent the coordinates of the object in the rotated space. The class doesn't produce a
specific output on its own, but it provides various methods to manipulate and interact
with these objects.

The class achieves its purpose by storing the coordinates in a Point object and providing
methods to perform operations like translation, enlargement, intersection, and merging
with other ManhattanArc3D instances. It uses a 45-degree rotated coordinate system, which allows
for easier calculations in certain geometric operations.
"""

from .generic import intersection, min_dist
from .interval import enlarge
from .point import Point


class ManhattanArc3D:
    """
    Merging point, segment, or region ⛝
    """

    def __init__(self, x, y, z, w) -> None:
        """
        Initialize a ManhattanArc3D object with 4-interval coordinates.

        :param x: The x-interval coordinate in the 4-interval space.
        :param y: The y-interval coordinate in the 4-interval space.
        :param z: The z-interval coordinate in the 4-interval space.
        :param w: The w-interval coordinate in the 4-interval space.

        Examples:
            >>> a = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
            >>> print(a)
            /-4, 2, 6, 12/
        """
        self.x_i = x
        self.y_i = y
        self.z_i = z
        self.w_i = w

    @classmethod
    def from_point(cls, pt) -> "ManhattanArc3D":
        """
        Create a ManhattanArc3D object from a 3D point.

        :param pt: A 3D point.
        :type pt: Point
        :return: A new ManhattanArc3D object.
        :rtype: ManhattanArc3D
        """
        xcoord = pt.xcoord.xcoord
        ycoord = pt.ycoord
        zcoord = pt.xcoord.ycoord
        x = xcoord - ycoord - zcoord
        y = xcoord - ycoord + zcoord
        z = xcoord + ycoord - zcoord
        w = xcoord + ycoord + zcoord
        return cls(x, y, z, w)

    @staticmethod
    def construct(xcoord, ycoord, zcoord) -> "ManhattanArc3D":
        """
        Constructs a ManhattanArc3D object from standard x and y coordinates.

        :param xcoord: The x-coordinate.
        :param ycoord: The y-coordinate.
        :param zcoord: The z-coordinate.
        :return: A new ManhattanArc3D object.
        Examples:
            >>> a = ManhattanArc3D.construct(4, 5, 3)
            >>> print(a)
            /-4, 2, 6, 12/
        """
        x = xcoord - ycoord - zcoord
        y = xcoord - ycoord + zcoord
        z = xcoord + ycoord - zcoord
        w = xcoord + ycoord + zcoord
        return ManhattanArc3D(x, y, z, w)

    def __repr__(self) -> str:
        """
        The `__repr__` function returns a string representation of an `ManhattanArc3D` object, including the class
        name and its x and y coordinates, which is useful for debugging.

        :return: The `__repr__` method is returning a string representation of the `ManhattanArc3D` object.

        Examples:
            >>> a = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
            >>> repr(a)
            'ManhattanArc3D(-4, 2, 6, 12)'
        """
        return f"{self.__class__.__name__}({self.x_i}, {self.y_i}, {self.z_i}, {self.w_i})"

    def __str__(self) -> str:
        """
        The `__str__` function returns a string representation of an object, specifically in the format
        "/xcoord, ycoord/".

        :return: The method `__str__` returns a string representation of the object. In this case, it
            returns a string in the format "/xcoord, ycoord/" where xcoord and ycoord are the x and y
            coordinates of the object.

        Examples:
            >>> a = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
            >>> print(a)
            /-4, 2, 6, 12/
        """
        return f"/{self.x_i}, {self.y_i}, {self.z_i}, {self.w_i}/"

    def __eq__(self, other: object) -> bool:
        """
        The `__eq__` function checks if two `ManhattanArc3D` instances have the same `impl` attribute.

        :param other: The `other` parameter represents the object that we are comparing with the current object
        :return: The `__eq__` method is returning a boolean value.

        Examples:
            >>> a = ManhattanArc3D(4 - 5 - 3 , 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
            >>> b = ManhattanArc3D(7 - 9 - 2, 7 - 9 + 2, 7 + 9 - 2, 7 + 9 + 2)
            >>> a == b
            False
            >>> c = ManhattanArc3D.construct(4, 5, 3)
            >>> a == c
            True
        """
        if not isinstance(other, ManhattanArc3D):
            return NotImplemented
        return (self.x_i, self.y_i, self.z_i, self.w_i) == (other.x_i, other.y_i, other.z_i, other.w_i)

    def min_dist_with(self, other) -> int:
        """
        The `min_dist_with` function calculates the minimum rectilinear distance between two objects.

        :param other: The `other` parameter represents another object with which you want to calculate
            the minimum rectilinear distance

        :return: the minimum rectilinear distance between the two objects.

        Examples:
            >>> r1 = ManhattanArc3D(4 - 5 - 3 , 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
            >>> r2 = ManhattanArc3D(7 - 9 - 2, 7 - 9 + 2, 7 + 9 - 2, 7 + 9 + 2)
            >>> r1.min_dist_with(r2)
            8
        """
        x_dist = min_dist(self.x_i, other.x_i)
        y_dist = min_dist(self.y_i, other.y_i)
        z_dist = min_dist(self.z_i, other.z_i)
        w_dist = min_dist(self.w_i, other.w_i)
        return int(max([x_dist, y_dist, z_dist, w_dist]))

    def enlarge_with(self, alpha: int) -> "ManhattanArc3D":
        """
        Enlarge the ManhattanArc3D intervals by a given factor.

        Expands each coordinate interval by the specified alpha value using the
        enlarge function from the interval module.

        :param alpha: The expansion factor to enlarge each coordinate interval.
        :return: A new ManhattanArc3D object with enlarged coordinates.

        Examples:
            >>> a = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
            >>> r = a.enlarge_with(1)
            >>> print(r)
            /[-5, -3], [1, 3], [5, 7], [11, 13]/
        """
        xcoord = enlarge(self.x_i, alpha)
        ycoord = enlarge(self.y_i, alpha)
        zcoord = enlarge(self.z_i, alpha)
        wcoord = enlarge(self.w_i, alpha)
        return ManhattanArc3D(xcoord, ycoord, zcoord, wcoord)

    def intersect_with(self, other: "ManhattanArc3D") -> "ManhattanArc3D":
        """
        Calculate the intersection between two ManhattanArc3D objects.

        Computes the coordinate-wise intersection of the intervals stored in both
        ManhattanArc3D objects, returning a new ManhattanArc3D with the intersected
        coordinates.

        :param other: Another ManhattanArc3D object to intersect with.
        :return: A new ManhattanArc3D object containing the intersection coordinates.
        """
        x_inter = intersection(self.x_i, other.x_i)
        y_inter = intersection(self.y_i, other.y_i)
        z_inter = intersection(self.z_i, other.z_i)
        w_inter = intersection(self.w_i, other.w_i)
        return ManhattanArc3D(x_inter, y_inter, z_inter, w_inter)

    def merge_with(self, other, alpha: int):
        """
        The `merge_with` function takes another object as input, calculates the minimum Manhattan distance between
        the two objects, enlarges the objects based on the calculated distance, finds the intersection
        of the enlarged objects, and returns a new object with the coordinates of the intersection.

        :param other: The "other" parameter is an object of the same class as the current object. It
            represents another instance of the class that we want to merge with the current instance

        :return: The `merge_with` method returns a new `ManhattanArc3D` object with the x-coordinate and
            y-coordinate of the intersection of the two objects being merged.

        Examples:
            >>> r1 = ManhattanArc3D(4 - 5 - 3, 4 - 5 + 3, 4 + 5 - 3, 4 + 5 + 3)
            >>> r2 = ManhattanArc3D(7 - 9 - 2, 7 - 9 + 2, 7 + 9 - 2, 7 + 9 + 2)
            >>> r1.merge_with(r2, 4)
            ManhattanArc3D([-8, 0], [-2, 4], [10, 10], [14, 16])
        """
        distance = self.min_dist_with(other)
        trr1 = self.enlarge_with(alpha)
        trr2 = other.enlarge_with(distance - alpha)
        return trr1.intersect_with(trr2)

    def get_point(self):
        """
        Converts the ManhattanArc3D object back to a Point object.

        :return: A Point object representing the coordinates of the ManhattanArc3D object.

        Examples:
            >>> a = ManhattanArc3D(-4, 2, 6, 12)
            >>> print(a.get_point())
            ((4, 3), 5)
        """
        xcoord = (self.x_i + self.y_i + self.z_i + self.w_i) // 4
        ycoord = (-self.x_i - self.y_i + self.z_i + self.w_i) // 4
        zcoord = (-self.x_i + self.y_i - self.z_i + self.w_i) // 4
        return Point(Point(xcoord, zcoord), ycoord)

    # def get_center(self):
    #     """
    #     Calculates the center of the merging segment

    #     :return: The center of the merging segment.

    #     Examples:
    #         >>> a = ManhattanArc3D(4 - 5, 4 + 5)
    #         >>> print(a.get_center())
    #         (4, 5)
    #     """
    #     center_point = self.impl.get_center()
    #     return center_point.inv_rotates()

    # def get_lower_corner(self) -> Point[Any, Any]:
    #     """
    #     Calculates the lower corner of the merging segment

    #     :return: The lower corner of the merging segment.

    #     Examples:
    #         >>> a = ManhattanArc3D(4 - 5, 4 + 5)
    #         >>> print(a.get_lower_corner())
    #         (4, 5)
    #     """
    #     lower_point = self.impl.lower_corner()
    #     return lower_point.inv_rotates()

    # def get_upper_corner(self) -> Point[Any, Any]:
    #     """
    #     Calculates the upper corner of the merging segment

    #     :return: The upper corner of the merging segment.

    #     Examples:
    #         >>> a = ManhattanArc3D(4 - 5, 4 + 5)
    #         >>> print(a.get_upper_corner())
    #         (4, 5)
    #     """
    #     upper_point = self.impl.upper_corner()
    #     return upper_point.inv_rotates()

    # def _nearest_point_to(self, manhattan_arc: "ManhattanArc3D[Any, Any]") -> Point[Any, Any]:
    #     """
    #     Calculates the center of the merging segment

    #     :return: The center of the merging segment.

    #     Examples:
    #         >>> a = ManhattanArc3D(4 - 5, 4 + 5)
    #         >>> print(a.nearest_point_to(Point(0, 0)))
    #         (4, 5)
    #     """
    #     nearest_pt = self.impl.nearest_to(manhattan_arc.impl)
    #     ic(nearest_pt)
    #     return nearest_pt.inv_rotates()

    # def nearest_point_to(self, other: Point[int, int]) -> Point[Any, Any]:
    #     """
    #     Calculates the center of the merging segment

    #     :return: The center of the merging segment.

    #     Examples:
    #         >>> a = ManhattanArc3D(4 - 5, 4 + 5)
    #         >>> print(a.nearest_point_to(Point(0, 0)))
    #         (4, 5)
    #     """
    #     ms = ManhattanArc3D.from_point(other)
    #     ic(self)
    #     ic(ms)
    #     return self._nearest_point_to(ms)

    #     # distance = self.min_dist_with(ms)
    #     # trr = ms.enlarge_with(distance)
    #     # lb = self.impl.lower_corner()
    #     # ub = self.impl.upper_corner()
    #     # m = self.impl.get_center()
    #     # if trr.impl.contains(lb):
    #     #     m = lb
    #     # elif trr.impl.contains(ub):
    #     #     m = ub
    #     # else:
    #     #     ic(self)
    #     # return m.inv_rotates()
