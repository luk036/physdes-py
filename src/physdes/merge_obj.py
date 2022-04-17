from .generic import intersection, min_dist
from .interval import enlarge
from .point import Point
from .vector2 import Vector2


class MergeObj(Point):
    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> print(a)
            /9, -1/
        """
        Point.__init__(self, x, y)

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> print(a)
            /9, -1/
        """
        return "/{self.x}, {self.y}/".format(self=self)

    def __iadd__(self, rhs: Vector2):
        """Translate by displacement

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> a += Vector2(1, 2)
            >>> print(a)
            /12, -2/
        """
        self.x += rhs.x + rhs.y
        self.y += rhs.x - rhs.y
        return self

    def __isub__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> a -= Vector2(1, 2)
            >>> print(a)
            /6, 0/
        """
        self.x -= rhs.x + rhs.y
        self.y -= rhs.x - rhs.y
        return self

    def min_dist_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> r1 = MergeObj(4 + 5, 4 - 5)
            >>> r2 = MergeObj(7 + 9, 7 - 9)
            >>> v = Vector2(5, 6)
            >>> r1.min_dist_with(r2)
            7
        """
        return max(min_dist(self.x, other.x), min_dist(self.y, other.y))

    def enlarge_with(self, alpha):
        """[summary]

        Args:
            alpha ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> r = a.enlarge_with(1)
            >>> print(r)
            /[8, 10], [-2, 0]/
        """
        x = enlarge(self.x, alpha)
        y = enlarge(self.y, alpha)
        return MergeObj(x, y)  # ???

    def intersection_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> r = a.intersection_with(a)
            >>> print(r)
            /9, -1/
        """
        p = super().intersection_with(other)  # ???
        return MergeObj(p.x, p.y)

    def merge_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> s1 = MergeObj(200 + 600, 200 - 600)
            >>> s2 = MergeObj(500 + 900, 500 - 900)
            >>> m1 = s1.merge_with(s2)
            >>> print(m1)
            /[1100.0, 1100.0], [-700.0, -100.0]/
        """
        alpha = self.min_dist_with(other)
        half = alpha / 2
        trr1 = enlarge(self, half)
        trr2 = enlarge(other, alpha - half)
        return intersection(trr1, trr2)
