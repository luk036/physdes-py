from .generic import intersection, min_dist
from .interval import enlarge
from .point import Point
from .vector2 import Vector2


class MergeObj:
    """Merging point, segment, or region"""

    impl: Point  # implemented by a 45 degree rotated point, vertical or
    # horizontal segment, and rectangle

    def __init__(self, xcoord, ycoord):
        """[summary]

        Args:
            xcoord ([type]): [description]
            ycoord ([type]): [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> print(a)
            /9, -1/
        """
        self.impl = Point(xcoord, ycoord)

    def construct(xcoord, ycoord):
        """Construct from the real point

        Args:
            xcoord ([type]): [description]
            ycoord ([type]): [description]

        Examples:
            >>> a = MergeObj.construct(4, 5)
            >>> print(a)
            /9, -1/
        """
        impl = Point(xcoord + ycoord, xcoord - ycoord)
        return MergeObj(impl.xcoord, impl.ycoord)

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> print(a)
            /9, -1/
        """
        return "/{self.impl.xcoord}, {self.impl.ycoord}/".format(self=self)

    def __eq__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

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
        self.impl.xcoord += rhs.x + rhs.y
        self.impl.ycoord += rhs.x - rhs.y
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
        self.impl.xcoord -= rhs.x + rhs.y
        self.impl.ycoord -= rhs.x - rhs.y
        return self

    def min_dist_with(self, other) -> int:
        """minimum rectilinear distance

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
        # Note: take max of xcoord and ycoord
        return max(min_dist(self.impl.xcoord, other.impl.xcoord),
                   min_dist(self.impl.ycoord, other.impl.ycoord))

    def enlarge_with(self, alpha: int):
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
        xcoord = enlarge(self.impl.xcoord, alpha)  # TODO: check
        ycoord = enlarge(self.impl.ycoord, alpha)  # TODO: check
        return MergeObj(xcoord, ycoord)  # TODO

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
        point = self.impl.intersection_with(other.impl)  # TODO
        return MergeObj(point.xcoord, point.ycoord)

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
            /[1100, 1100], [-700, -100]/
        """
        alpha = self.min_dist_with(other)
        half = alpha // 2
        trr1 = enlarge(self.impl, half)
        trr2 = enlarge(other.impl, alpha - half)
        impl = intersection(trr1, trr2)
        return MergeObj(impl.xcoord, impl.ycoord)
