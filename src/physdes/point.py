from .generic import contain, intersection, min_dist, overlap
from .vector2 import Vector2


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        self.x = x
        self.y = y

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return Point(self.x, self.y)

    def __lt__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]
        """
        return (self.x, self.y) < (rhs.x, rhs.y)

    def __le__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]
        """
        return (self.x, self.y) <= (rhs.x, rhs.y)

    def __eq__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]
        """
        return (self.x, self.y) == (rhs.x, rhs.y)

    def __iadd__(self, rhs: Vector2):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]
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

    def intersection_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return Point(intersection(self.x, other.x), intersection(self.y, other.y))

    def min_dist_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return min_dist(self.x, other.x) + min_dist(self.y, other.y)

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "({self.x}, {self.y})".format(self=self)
