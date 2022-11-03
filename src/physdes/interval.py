from .generic import min_dist, min_dist_change


class Interval:
    __slots__ = ("_lb", "_ub")

    def __init__(self, lb, ub):
        """[summary]

        Args:
            lb ([type]): [description]
            ub ([type]): [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a)
            [3, 4]
        """
        self._lb = lb
        self._ub = ub

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a)
            [3, 4]
        """
        return "[{self.lb}, {self.ub}]".format(self=self)

    @property
    def lb(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> a.lb
            3
        """
        return self._lb

    @property
    def ub(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> a.ub
            4
        """
        return self._ub

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a.copy())
            [3, 4]
        """
        return Interval(self._lb, self._ub)

    def length(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.ub - self.lb

    def __eq__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(3, 5)
            >>> a == b
            False
        """
        return (self.lb, self.ub) == (other.lb, other.ub)

    def __lt__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(3, 5)
            >>> a < b
            False
            >>> b < a
            False
        """
        return self.ub < other

    def __gt__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(3, 5)
            >>> a > b
            False
            >>> b > a
            False
        """
        return self.lb > other

    def __le__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(3, 5)
            >>> a <= b
            True
            >>> b <= a
            True
        """
        return not (other < self.lb)

    def __ge__(self, other) -> bool:
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(3, 5)
            >>> a >= b
            True
            >>> b >= a
            True
        """
        return not (self.ub < other)

    def __neg__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> print(-a)
            [-4, -3]
        """
        return Interval(-self.ub, -self.lb)

    def __iadd__(self, rhs):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> a += 10
            >>> print(a)
            [13, 14]
        """
        self._lb += rhs
        self._ub += rhs
        return self

    def __add__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a + 10)
            [13, 14]
        """
        return Interval(self.lb + rhs, self.ub + rhs)

    def __isub__(self, rhs):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> a -= 1
            >>> print(a)
            [2, 3]
        """
        self._lb -= rhs
        self._ub -= rhs
        return self

    def __sub__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a - 1)
            [2, 3]
        """
        return Interval(self.lb - rhs, self.ub - rhs)

    def overlaps(self, obj) -> bool:
        """[summary]

        Args:
            obj ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Interval(3, 5)
            >>> a.overlaps(Interval(4, 9))
            True
            >>> a.overlaps(Interval(6, 9))
            False
        """
        return not (self < obj or obj < self)

    def contains(self, obj) -> bool:
        """[summary]

        Args:
            obj ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Interval(3, 8)
            >>> a.contains(4)
            True
            >>> a.contains(Interval(4, 7))
            True
            >>> a.contains(Interval(6, 9))
            False
        """
        # `obj` can be an Interval or int
        if isinstance(obj, Interval):
            return self.lb <= obj.lb and obj.ub <= self.ub
        else:  # assume scalar
            return self.lb <= obj <= self.ub

    def hull_with(self, obj):
        """[summary]

        Args:
            obj ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 8)
            >>> print(a.hull_with(Interval(4, 7)))
            [3, 8]
            >>> print(a.hull_with(Interval(6, 9)))
            [3, 9]
        """
        if isinstance(obj, Interval):
            return Interval(min(self.lb, obj.lb), max(self.ub, obj.ub))
        else:  # assume scalar
            return Interval(min(self.lb, obj), max(self.ub, obj))

    def intersection_with(self, obj):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 8)
            >>> print(a.intersection_with(4))
            4
            >>> print(a.intersection_with(Interval(4, 7)))
            [4, 7]
            >>> print(a.intersection_with(Interval(6, 9)))
            [6, 8]
        """
        # `a` can be an Interval or int
        assert self.overlaps(obj)
        if isinstance(obj, Interval):
            return Interval(max(self.lb, obj.lb), min(self.ub, obj.ub))
        else:  # assume scalar
            return obj

    def min_dist_with(self, obj):
        """[summary]

        Args:
            obj ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 5)
            >>> print(a.min_dist_with(2))
            1
            >>> print(a.min_dist_with(Interval(4, 7)))
            0
            >>> print(a.min_dist_with(Interval(6, 9)))
            1
        """
        if self < obj:
            return min_dist(self.ub, obj)
        if obj < self:
            return min_dist(self.lb, obj)
        return 0

    def min_dist_change_with(self, obj):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self < obj:
            self._lb = self._ub
            return min_dist_change(self._ub, obj)
        if obj < self:
            self._ub = self._lb
            return min_dist_change(self._lb, obj)
        if isinstance(obj, Interval):
            self = obj = self.intersection_with(obj)
        else:  # assume scalar
            self._ub = self._lb = obj
        return 0

    def enlarge_with(self, alpha):
        """[summary]

        Args:
            alpha: [description]

        Returns:
            [type]: [description]

        Examples:
            >>> a = Interval(3, 5)
            >>> print(a.enlarge_with(2))
            [1, 7]
        """
        return Interval(self._lb - alpha, self._ub + alpha)


def hull(lhs, rhs):
    """[summary]

    Args:
        lhs ([type]): [description]
        rhs ([type]): [description]

    Returns:
        [type]: [description]
    """
    if hasattr(lhs, 'hull_with'):
        return lhs.hull_with(rhs)
    elif hasattr(rhs, 'hull_with'):
        return rhs.hull_with(lhs)
    else:  # assume scalar
        return Interval(min(lhs, rhs), max(lhs, rhs))


def enlarge(lhs, rhs):
    """[summary]

    Args:
        lhs ([type]): [description]
        rhs ([type]): [description]

    Returns:
        [type]: [description]

        Examples:
            >>> a = Interval(3, 5)
            >>> print(enlarge(a, 2))
            [1, 7]
    """
    if hasattr(lhs, 'enlarge_with'):
        return lhs.enlarge_with(rhs)
    else:  # assume scalar
        return Interval(lhs - rhs, lhs + rhs)
