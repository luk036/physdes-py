from numpy import isscalar

from .generic import min_dist, min_dist_change


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
        """[summary]

        Args:
            a ([type]): [description]

        Returns:
            bool: [description]
        """
        # `a` can be an interval or int
        if isscalar(a):
            return self.lower <= a <= self.upper
        return self.lower <= a.lower and a.upper <= self.upper

    def intersection_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        # `a` can be an interval or int
        if isscalar(other):
            return other
        return interval(max(self.lower, other.lower), min(self.upper, other.upper))

    def min_dist_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self < other:
            return min_dist(self.upper, other)
        if other < self:
            return min_dist(self.lower, other)
        return 0

    def min_dist_change_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        if self < other:
            self._lower = self._upper
            return min_dist_change(self._upper, other)
        if other < self:
            self._upper = self._lower
            return min_dist_change(self._lower, other)
        if isscalar(other):
            self._upper = self._lower = other
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
        return interval(self._lower - alpha, self._upper + alpha)

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "[{self.lower}, {self.upper}]".format(self=self)


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
        return interval(lhs - rhs, lhs + rhs)
