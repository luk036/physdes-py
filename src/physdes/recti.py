from .interval import Interval
from .point import Point


class Rectangle(Point):
    def __init__(self, xcoord: Interval, ycoord: Interval):
        """[summary]

        Args:
            xcoord (Interval): [description]
            ycoord (Interval): [description]

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
    def ll(self) -> Point:
        """Lower left

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
            >>> print(a.ll)
            (3, 5)
        """
        return Point(self.xcoord.lb, self.ycoord.lb)

    @property
    def ur(self) -> Point:
        """Upper right

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
            >>> print(a.ur)
            (4, 6)
        """
        return Point(self.xcoord.ub, self.ycoord.ub)

    # def copy(self):
    #     """[summary]

    #     Returns:
    #         [type]: [description]

    #     Examples:
    #         >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
    #         >>> print(a.copy())
    #         ([3, 4], [5, 6])
    #         >>> a3d = Rectangle(a, Interval(7, 8))  # Rectangle in 3d
    #         >>> print(a3d.copy())
    #         (([3, 4], [5, 6]), [7, 8])
    #     """
    #     return Rectangle(self.xcoord, self.ycoord)

    # def __eq__(self, rhs) -> bool:
    #     return self.xcoord == rhs.xcoord and self.ycoord == rhs.ycoord

    # def flip(self):
    #     """[summary]

    #     Returns:
    #         [type]: [description]

    #     Examples:
    #         >>> a = Rectangle(Interval(3, 4), Interval(5, 6))
    #         >>> print(a.flip())
    #         ([5, 6], [3, 4])
    #         >>> a3d = Rectangle(a, Interval(7, 8))  # Rectangle in 3d
    #         >>> print(a3d.flip())
    #         ([7, 8], ([3, 4], [5, 6]))
    #     """
    #     return Rectangle(self.ycoord, self.xcoord)

    # `a` can be Point, VSegment, HSegment, or Rectangle
    def contains(self, obj: Point) -> bool:
        """[summary]

        Args:
            obj (Point): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Rectangle(Interval(30, 40), Interval(50, 60))
            >>> a.contains(Point(36, 53))
            True
            >>> a.contains(Rectangle(Interval(32, 38), Interval(51, 57)))
            True
            >>> a.contains(Rectangle(Interval(32, 38), Interval(51, 67)))
            False
        """
        return self.xcoord.contains(obj.xcoord) and \
            self.ycoord.contains(obj.ycoord)

    def width(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rectangle(Interval(30, 40), Interval(50, 62))
            >>> a.width()
            10
        """
        return self.xcoord.length()

    def height(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rectangle(Interval(30, 40), Interval(50, 62))
            >>> a.height()
            12
        """
        return self.ycoord.length()

    def area(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rectangle(Interval(30, 40), Interval(50, 62))
            >>> a.area()
            120
        """
        return self.xcoord.length() * self.ycoord.length()


class VSegment(Point):
    # def __init__(self, xcoord, ycoord):
    #     """[summary]
    #
    #     Args:
    #         xcoord ([type]): [description]
    #         ycoord ([type]): [description]
    #
    #     Examples:
    #         >>> a = VSegment(5, Interval(3, 4))
    #         >>> print(a)
    #         (5, [3, 4])
    #         >>> a3d = VSegment(6, a)  # VSegment in 3d
    #         >>> print(a3d)
    #         (6, (5, [3, 4]))
    #     """
    #     Point.__init__(self, xcoord, ycoord)

    # def copy(self):
    #     """[summary]

    #     Returns:
    #         [type]: [description]

    #     Examples:
    #         >>> a = VSegment(5, Interval(3, 4))
    #         >>> print(a.copy())
    #         (5, [3, 4])
    #         >>> a3d = VSegment(6, a)  # VSegment in 3d
    #         >>> print(a3d.copy())
    #         (6, (5, [3, 4]))
    #     """
    #     return VSegment(self.xcoord, self.ycoord)

    # `a` can be Point or VSegment
    def contains(self, a: Point) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = VSegment(5, Interval(30, 40))
            >>> a.contains(Point(5, 33))
            True
            >>> a.contains(VSegment(5, Interval(33, 38)))
            True
            >>> a.contains(VSegment(6, Interval(33, 38)))
            False
        """
        return self.xcoord == a.xcoord and self.ycoord.contains(a.ycoord)

    # def flip(self):
    #     """[summary]

    #     Returns:
    #         [type]: [description]

    #     Examples:
    #         >>> a = VSegment(5, Interval(30, 40))
    #         >>> print(a.flip())
    #         ([30, 40], 5)
    #     """
    #     return HSegment(self.ycoord, self.xcoord)


class HSegment(Point):
    # def __init__(self, xcoord, ycoord):
    #     """[summary]
    #
    #     Args:
    #         xcoord ([type]): [description]
    #         ycoord ([type]): [description]
    #
    #     Examples:
    #         >>> a = HSegment(Interval(3, 4), 5)
    #         >>> print(a)
    #         ([3, 4], 5)
    #         >>> a3d = HSegment(a, 7)  # HSegment in 3d
    #         >>> print(a3d)
    #         (([3, 4], 5), 7)
    #     """
    #     Point.__init__(self, xcoord, ycoord)

    # def copy(self):
    #     """[summary]

    #     Returns:
    #         [type]: [description]

    #     Examples:
    #         >>> a = HSegment(Interval(3, 4), 5)
    #         >>> print(a.copy())
    #         ([3, 4], 5)
    #         >>> a3d = HSegment(a, 7)  # HSegment in 3d
    #         >>> print(a3d.copy())
    #         (([3, 4], 5), 7)
    #     """
    #     return HSegment(self.xcoord, self.ycoord)

    # `a` can be Point or HSegment
    def contains(self, a) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = HSegment(Interval(30, 40), 5)
            >>> a.contains(Point(33, 5))
            True
            >>> a.contains(HSegment(Interval(33, 38), 5))
            True
            >>> a.contains(HSegment(Interval(33, 38), 6))
            False
        """
        return self.ycoord == a.ycoord and self.xcoord.contains(a.xcoord)

    # def flip(self):
    #     """[summary]

    #     Returns:
    #         [type]: [description]

    #     Examples:
    #         >>> a = HSegment(Interval(30, 40), 5)
    #         >>> print(a.flip())
    #         (5, [30, 40])
    #     """
    #     return VSegment(self.ycoord, self.xcoord)
