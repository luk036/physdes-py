from .generic import contain, intersection, min_dist, overlap
from .interval import interval
from .vector2 import vector2


class point:
    __slots__ = ("_x", "_y")

    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        self._x = x
        self._y = y

    @property
    def x(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._x

    @property
    def y(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._y

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return point(self._x, self._y)

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

    def __iadd__(self, rhs: vector2):
        """[summary]

        Args:
            rhs (vector2): [description]

        Returns:
            [type]: [description]
        """
        self._x += rhs.x
        self._y += rhs.y
        return self

    def __add__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]
        """
        if isinstance(rhs, vector2):
            return point(self.x + rhs.x, self.y + rhs.y)
        else:
            return point(self.x + rhs, self.y + rhs)

    def __isub__(self, rhs: vector2):
        """[summary]

        Args:
            rhs (vector2): [description]

        Returns:
            [type]: [description]
        """
        self._x -= rhs.x
        self._y -= rhs.y
        return self

    def __sub__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]
        """
        if isinstance(rhs, vector2):
            return point(self.x - rhs.x, self.y - rhs.y)
        elif isinstance(rhs, point):
            return vector2(self.x - rhs.x, self.y - rhs.y)
        else:
            return point(self.x - rhs, self.y - rhs)

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return point(self.y, self.x)

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
        return point(intersection(self.x, other.x), intersection(self.y, other.y))

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


class dualpoint(point):
    def __init__(self, x, y):
        point.__init__(self, x, y)

    @property
    def x(self):
        return self._y

    @property
    def y(self):
        return self._x


class rectangle(point):
    def __init__(self, x: interval, y: interval):
        """[summary]

        Args:
            x (interval): [description]
            y (interval): [description]
        """
        point.__init__(self, x, y)

    @property
    def lower(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return point(self.x.lower, self.y.lower)

    @property
    def upper(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return point(self.x.upper, self.y.upper)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return rectangle(self._x, self._y)

    # def __eq__(self, rhs) -> bool:
    #     return self.x == rhs.x and self.y == rhs.y

    def flip(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return rectangle(self.y, self.x)

    # `a` can be point, vsegment, hsegment, or rectangle
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


class vsegment(point):
    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        point.__init__(self, x, y)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return vsegment(self._x, self._y)

    # `a` can be point or vsegment
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
        return hsegment(self.y, self.x)


class hsegment(point):
    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        point.__init__(self, x, y)

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return hsegment(self._x, self._y)

    # `a` can be point or hsegment
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
        return vsegment(self.y, self.x)
