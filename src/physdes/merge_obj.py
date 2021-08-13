from .generic import intersection, min_dist
from .interval import enlarge
from .recti import point
from .vector2 import vector2


class merge_obj(point):
    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        point.__init__(self, x, y)

    def __iadd__(self, rhs: vector2):
        self._x += rhs.x + rhs.y
        self._y += rhs.x - rhs.y
        return self

    def __isub__(self, rhs: vector2):
        self._x -= rhs.x + rhs.y
        self._y -= rhs.x - rhs.y
        return self

    def min_dist_with(self, other):
        return max(min_dist(self._x, other._x), min_dist(self._y, other._y))

    def enlarge_with(self, alpha):
        x = enlarge(self.x, alpha)
        y = enlarge(self.y, alpha)
        return merge_obj(x, y)  # ???

    def intersection_with(self, other):
        p = super().intersection_with(other)
        return merge_obj(p.x, p.y)

    def merge_with(self, other):
        alpha = self.min_dist_with(other)
        half = alpha / 2
        trr1 = enlarge(self, half)
        trr2 = enlarge(other, alpha - half)
        return intersection(trr1, trr2)

    def __str__(self):
        return "/{self.x}, {self.y}/".format(self=self)
