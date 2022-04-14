from numpy import isscalar

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
        assert not (ub < lb)
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

    def len(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.ub - self.lb

    def __eq__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(3, 5)
            >>> a == b
            False
        """
        return (self.lb, self.ub) == (rhs.lb, rhs.ub)

    def __lt__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

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
        return self.ub < rhs

    def __gt__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

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
        return self.lb > rhs

    def __le__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

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
        return not (rhs < self.lb)

    def __ge__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

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
        return not (self.ub < rhs)

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
        """
        return Interval(self.lb + rhs, self.ub + rhs)

    def __isub__(self, rhs):
        """[summary]

        Args:
            rhs (Vector2): [description]

        Returns:
            [type]: [description]
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
        """
        return Interval(self.lb - rhs, self.ub - rhs)

    def overlaps(self, a) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]
        """
        return not (self < a or a < self)

    def contains(self, a) -> bool:
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]
        """
        # `a` can be an Interval or int
        if isscalar(a):
            return self.lb <= a <= self.ub
        return self.lb <= a.lb and a.ub <= self.ub

    def intersection_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        # `a` can be an Interval or int
        if isscalar(other):
            return other
        return Interval(max(self.lb, other.lb), min(self.ub, other.ub))

    def min_dist_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self < other:
            return min_dist(self.ub, other)
        if other < self:
            return min_dist(self.lb, other)
        return 0

    def min_dist_change_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self < other:
            self._lb = self._ub
            return min_dist_change(self._ub, other)
        if other < self:
            self._ub = self._lb
            return min_dist_change(self._lb, other)
        if isscalar(other):
            self._ub = self._lb = other
        else:
            self = other = self.intersection_with(other)
        return 0

    def enlarge_with(self, alpha):
        """[summary]

        Args:
            alpha: [description]

        Returns:
            [type]: [description]
        """
        return Interval(self._lb - alpha, self._ub + alpha)


def enlarge(lhs, rhs):
    """[summary]

    Args:
        lhs ([type]): [description]
        rhs ([type]): [description]

    Returns:
        [type]: [description]
    """
    if not isscalar(lhs):
        return lhs.enlarge_with(rhs)
    else:
        return Interval(lhs - rhs, lhs + rhs)
