from .generic import intersection, min_dist
from .interval import enlarge
from .point import Point
from .vector2 import Vector2


class MergeObj:
    """Merging point, segment, or region"""

    impl: Point # implemented by a 45 degree rotated point, vertical or
                # horizontal segment, and rectangle

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
        self.impl = Point(x, y)

    def construct(x, y):
        """Construct from the real point
    
        Args:
            x ([type]): [description]
            y ([type]): [description]
    
        Examples:
            >>> a = MergeObj.construct(4, 5)
            >>> print(a)
            /9, -1/
        """
        impl = Point(x + y, x - y)
        return MergeObj(impl.x, impl.y)

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = MergeObj(4 + 5, 4 - 5)
            >>> print(a)
            /9, -1/
        """
        return "/{self.impl.x}, {self.impl.y}/".format(self=self)

    def __eq__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

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
        return self.impl == rhs.impl

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
        self.impl.x += rhs.x + rhs.y
        self.impl.y += rhs.x - rhs.y
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
        self.impl.x -= rhs.x + rhs.y
        self.impl.y -= rhs.x - rhs.y
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
        # Note: take max of x and y
        return max(min_dist(self.impl.x, other.impl.x),
                   min_dist(self.impl.y, other.impl.y))

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
        x = enlarge(self.impl.x, alpha) # TODO: check
        y = enlarge(self.impl.y, alpha) # TODO: check
        return MergeObj(x, y)  # TODO

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
        p = self.impl.intersection_with(other.impl)  # TODO
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
            /[1100, 1100], [-700, -100]/
        """
        alpha = self.min_dist_with(other)
        half = alpha // 2
        trr1 = enlarge(self.impl, half)
        trr2 = enlarge(other.impl, alpha - half)
        impl = intersection(trr1, trr2)
        return MergeObj(impl.x, impl.y)
