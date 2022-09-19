from .generic import contain, intersection, min_dist, overlap
from .interval import hull
from .vector2 import Vector2
from typing import NamedTuple, Any


class Point(NamedTuple):
    x: Any
    y: Any

    # __slots__ = ("x", "y")

    # def __init__(self, x, y):
    #     """[summary]
    #
    #     Args:
    #         x ([type]): [description]
    #         y ([type]): [description]
    #
    #     Examples:
    #         >>> a = Point(3, 4)
    #         >>> print(a)
    #         (3, 4)
    #         >>> a3d = Point(a, 5)  # Point in 3d
    #         >>> print(a3d)
    #         ((3, 4), 5)
    #     """
    #     self.x = x
    #     self.y = y

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> print(a)
            (3, 4)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> print(a3d)
            ((3, 4), 5)
        """
        return "({self.x}, {self.y})".format(self=self)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> b = a.copy()
            >>> print(b)
            (3, 4)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = a3d.copy()
            >>> print(b3d)
            ((3, 4), 5)
        """
        return Point(self.x, self.y)

    def __lt__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]

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
        return (self.x, self.y) < (rhs.x, rhs.y)

    def __le__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]

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
        return (self.x, self.y) <= (rhs.x, rhs.y)

    def __eq__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]

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
        return (self.x, self.y) == (rhs.x, rhs.y)

    def __iadd__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]

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
        self.x += rhs.x
        self.y += rhs.y
        return self

    def __add__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> print(a + v)
            (8, 10)
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> print(a3d + Vector2(v, 1))
            ((8, 10), 6)
        """
        if isinstance(rhs, Vector2):
            return Point(self.x + rhs.x, self.y + rhs.y)
        else:
            return Point(self.x + rhs, self.y + rhs)

    def __isub__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]

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
        self.x -= rhs.x
        self.y -= rhs.y
        return self

    def __sub__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> v = Vector2(5, 6)
            >>> b = a - v
            >>> print(b)
            (-2, -2)
            >>> print(a - b)
            <5, 6>
            >>> a3d = Point(a, 5)  # Point in 3d
            >>> b3d = a3d - Vector2(v, 1)
            >>> print(b3d)
            ((-2, -2), 4)
            >>> print(a3d - b3d)
            <<5, 6>, 1>
        """
        if isinstance(rhs, Vector2):
            return Point(self.x - rhs.x, self.y - rhs.y)
        elif isinstance(rhs, Point):
            return Vector2(self.x - rhs.x, self.y - rhs.y)
        else:
            return Point(self.x - rhs, self.y - rhs)

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Point(3, 4)
            >>> print(a.flip())
            (4, 3)
            >>> r = Point([3, 4], [5, 6])  # Rect
            >>> print(r.flip())
            ([5, 6], [3, 4])
        """
        return Point(self.y, self.x)

    def overlaps(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return overlap(self.x, other.x) and overlap(self.y, other.y)

    def contains(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return contain(self.x, other.x) and contain(self.y, other.y)

    def hull_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        Self = type(self)
        return Self(hull(self.x, other.x), hull(self.y, other.y))

    def intersection_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        Self = type(self)
        return Self(intersection(self.x, other.x),
                    intersection(self.y, other.y))

    def min_dist_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return min_dist(self.x, other.x) + min_dist(self.y, other.y)
