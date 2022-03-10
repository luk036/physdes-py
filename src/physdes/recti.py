from .interval import Interval
from .point import Point


class Rect(Point):
    def __init__(self, x: Interval, y: Interval):
        """[summary]

        Args:
            x (Interval): [description]
            y (Interval): [description]
        """
        Point.__init__(self, x, y)

    @property
    def lb(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return Point(self.x.lb, self.y.lb)

    @property
    def ub(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return Point(self.x.ub, self.y.ub)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return Rect(self.x, self.y)

    # def __eq__(self, rhs) -> bool:
    #     return self.x == rhs.x and self.y == rhs.y

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return Rect(self.y, self.x)

    # `a` can be Point, VSegment, HSegment, or Rect
    def contains(self, a) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]
        """
        return self.x.contains(a.x) and self.y.contains(a.y)

    def area(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.x.len() * self.y.len()


class VSegment(Point):
    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        Point.__init__(self, x, y)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return VSegment(self.x, self.y)

    # `a` can be Point or VSegment
    def contains(self, a) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]
        """
        return self.x == a.x and self.y.contains(a.y)

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return HSegment(self.y, self.x)


class HSegment(Point):
    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        Point.__init__(self, x, y)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return HSegment(self.x, self.y)

    # `a` can be Point or HSegment
    def contains(self, a) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]
        """
        return self.y == a.y and self.x.contains(a.x)

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return VSegment(self.y, self.x)
