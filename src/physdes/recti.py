from .generic import contain, intersection, min_dist, min_dist_change, overlap
from .vector2 import vector2
from numpy import isscalar

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

    def overlaps(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return overlap(self.x, other.x) and overlap(self.y, other.y)

    def contains(self, other):
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


class interval:
    __slots__ = ("_lower", "_upper")

    def __init__(self, lower, upper):
        """[summary]

        Args:
            lower ([type]): [description]
            upper ([type]): [description]
        """
        assert not (upper < lower)
        self._lower = lower
        self._upper = upper

    @property
    def lower(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._lower

    @property
    def upper(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._upper

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return interval(self._lower, self._upper)

    def len(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.upper - self.lower

    def __eq__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]
        """
        return (self.lower, self.upper) == (rhs.lower, rhs.upper)

    def __lt__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]
        """
        return self.upper < rhs

    def __gt__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]
        """
        return self.lower > rhs

    def __le__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]
        """
        return not (rhs < self.lower)

    def __ge__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]
        """
        return not (self.upper < rhs)

    def __neg__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return interval(-self.upper, -self.lower)

    def __iadd__(self, rhs):
        """[summary]

        Args:
            rhs (vector2): [description]

        Returns:
            [type]: [description]
        """
        self._lower += rhs
        self._upper += rhs
        return self

    def __add__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]
        """
        return interval(self.lower + rhs, self.upper + rhs)

    def __isub__(self, rhs):
        """[summary]

        Args:
            rhs (vector2): [description]

        Returns:
            [type]: [description]
        """
        self._lower -= rhs
        self._upper -= rhs
        return self

    def __sub__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]
        """
        return interval(self.lower - rhs, self.upper - rhs)

    def overlaps(self, a) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]
        """
        return not (self < a or a < self)

    def contains(self, a) -> bool:
        # `a` can be an interval or int
        if isscalar(a):
            return self.lower <= a and a <= self.upper
        return self.lower <= a.lower and a.upper <= self.upper

    def intersection_with(self, other):
        # `a` can be an interval or int
        if isscalar(other):
            return other
        return interval(max(self.lower, other.lower),
                        min(self.upper, other.upper))

    def min_dist_with(self, other):
        if self < other:
            return min_dist(self.upper, other);
        if other < self:
            return min_dist(self.lower, other);
        return 0;

    def min_dist_change_with(self, other):
        if self < other:
            self._lower = self._upper
            return min_dist_change(self._upper, other);
        if other < self:
            self._upper = self._lower
            return min_dist_change(self._lower, other);
        if isscalar(other):
            self._upper = self._lower = other;
        else:
            self = other = self.intersection_with(other);
        return 0;

    def __str__(self):
        return "[{self.lower}, {self.upper}]".format(self=self)


class rectangle(point):
    def __init__(self, x: interval, y: interval):
        point.__init__(self, x, y)

    @property
    def lower(self):
        return point(self.x.lower, self.y.lower)

    @property
    def upper(self):
        return point(self.x.upper, self.y.upper)

    def copy(self):
        return rectangle(self._x, self._y)

    # def __eq__(self, rhs) -> bool:
    #     return self.x == rhs.x and self.y == rhs.y

    def flip(self):
        return rectangle(self.y, self.x)

    # `a` can be point, vsegment, hsegment, or rectangle
    def contains(self, a) -> bool:
        return self.x.contains(a.x) and self.y.contains(a.y)

    def area(self):
        return self.x.len() * self.y.len()


class vsegment(point):
    def __init__(self, x, y):
        point.__init__(self, x, y)

    def copy(self):
        return vsegment(self._x, self._y)

    # `a` can be point or vsegment
    def contains(self, a) -> bool:
        return self.x == a.x and self.y.contains(a.y)

    def flip(self):
        return hsegment(self.y, self.x)


class hsegment(point):
    def __init__(self, x, y):
        point.__init__(self, x, y)

    def copy(self):
        return hsegment(self._x, self._y)

    # `a` can be point or hsegment
    def contains(self, a) -> bool:
        return self.y == a.y and self.x.contains(a.x)

    def flip(self):
        return vsegment(self.y, self.x)


def test_recti(obj):
    print(obj)
    obj2 = obj.copy()
    assert obj2 == obj
    obj3 = obj2.flip().flip()
    assert obj3 == obj


if __name__ == "__main__":
    v = vector2(1, 2)
    p = point(3, 4)
    q = point(5, 6)
    intv1 = interval(2, 8)
    intv3 = interval(1, 10)
    R = rectangle(intv1, intv3)
    vseg = vsegment(4, intv1)
    hseg = hsegment(intv3, 11)

    print(v)
    print(q)
    print(intv1)
    print(intv3)

    v2 = v.copy()
    assert v2 == v

    intv2 = intv1.copy()
    assert intv2 == intv1
    assert intv2.contains(5)
    assert intv3.contains(intv2)

    test_recti(p)
    test_recti(vseg)
    test_recti(hseg)
    test_recti(R)

    assert R.contains(p)
    assert R.contains(vseg)
    assert not R.contains(hseg)
