from .interval import Interval
from .point import Point

class Rect(Point):
    def __init__(self, x: Interval, y: Interval):
        """[summary]
    
        Args:
            x (Interval): [description]
            y (Interval): [description]
    
        Examples:
            >>> a = Rect(Interval(3, 4), Interval(5, 6))
            >>> print(a)
            ([3, 4], [5, 6])
            >>> a3d = Rect(a, Interval(7, 8))  # Rect in 3d
            >>> print(a3d)
            (([3, 4], [5, 6]), [7, 8])
        """
        Point.__init__(self, x, y)

    @property
    def lb(self) -> Point:
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rect(Interval(3, 4), Interval(5, 6))
            >>> print(a.lb)
            (3, 5)
        """
        return Point(self.x.lb, self.y.lb)

    @property
    def ub(self) -> Point:
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rect(Interval(3, 4), Interval(5, 6))
            >>> print(a.ub)
            (4, 6)
        """
        return Point(self.x.ub, self.y.ub)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rect(Interval(3, 4), Interval(5, 6))
            >>> print(a.copy())
            ([3, 4], [5, 6])
            >>> a3d = Rect(a, Interval(7, 8))  # Rect in 3d
            >>> print(a3d.copy())
            (([3, 4], [5, 6]), [7, 8])
        """
        return Rect(self.x, self.y)

    # def __eq__(self, rhs) -> bool:
    #     return self.x == rhs.x and self.y == rhs.y

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rect(Interval(3, 4), Interval(5, 6))
            >>> print(a.flip())
            ([5, 6], [3, 4])
            >>> a3d = Rect(a, Interval(7, 8))  # Rect in 3d
            >>> print(a3d.flip())
            ([7, 8], ([3, 4], [5, 6]))
        """
        return Rect(self.y, self.x)

    # `a` can be Point, VSegment, HSegment, or Rect
    def contains(self, a) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Rect(Interval(30, 40), Interval(50, 60))
            >>> a.contains(Point(36, 53))
            True
            >>> a.contains(Rect(Interval(32, 38), Interval(51, 57)))
            True
            >>> a.contains(Rect(Interval(32, 38), Interval(51, 67)))
            False
        """
        return self.x.contains(a.x) and self.y.contains(a.y)

    def width(self):
        return self.x.len()

    def height(self):
        return self.y.len()

    def area(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Rect(Interval(30, 40), Interval(50, 60))
            >>> a.area()
            100
        """
        return self.x.len() * self.y.len()


class VSegment(Point):
    # def __init__(self, x, y):
    #     """[summary]
    #
    #     Args:
    #         x ([type]): [description]
    #         y ([type]): [description]
    #
    #     Examples:
    #         >>> a = VSegment(5, Interval(3, 4))
    #         >>> print(a)
    #         (5, [3, 4])
    #         >>> a3d = VSegment(6, a)  # VSegment in 3d
    #         >>> print(a3d)
    #         (6, (5, [3, 4]))
    #     """
    #     Point.__init__(self, x, y)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = VSegment(5, Interval(3, 4))
            >>> print(a.copy())
            (5, [3, 4])
            >>> a3d = VSegment(6, a)  # VSegment in 3d
            >>> print(a3d.copy())
            (6, (5, [3, 4]))
        """
        return VSegment(self.x, self.y)

    # `a` can be Point or VSegment
    def contains(self, a) -> bool:
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
        return self.x == a.x and self.y.contains(a.y)

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = VSegment(5, Interval(30, 40))
            >>> print(a.flip())
            ([30, 40], 5)
        """
        return HSegment(self.y, self.x)


class HSegment(Point):
    # def __init__(self, x, y):
    #     """[summary]
    #
    #     Args:
    #         x ([type]): [description]
    #         y ([type]): [description]
    #
    #     Examples:
    #         >>> a = HSegment(Interval(3, 4), 5)
    #         >>> print(a)
    #         ([3, 4], 5)
    #         >>> a3d = HSegment(a, 7)  # HSegment in 3d
    #         >>> print(a3d)
    #         (([3, 4], 5), 7)
    #     """
    #     Point.__init__(self, x, y)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = HSegment(Interval(3, 4), 5)
            >>> print(a.copy())
            ([3, 4], 5)
            >>> a3d = HSegment(a, 7)  # HSegment in 3d
            >>> print(a3d.copy())
            (([3, 4], 5), 7)
        """
        return HSegment(self.x, self.y)

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
        return self.y == a.y and self.x.contains(a.x)

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = HSegment(Interval(30, 40), 5)
            >>> print(a.flip())
            (5, [30, 40])
        """
        return VSegment(self.y, self.x)
