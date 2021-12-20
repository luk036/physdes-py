from .generic import intersection, min_dist
from .interval import enlarge
from .point import point
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
        """[summary]

        Args:
            rhs (vector2): [description]

        Returns:
            [type]: [description]
        """
        self.x += rhs.x + rhs.y
        self.y += rhs.x - rhs.y
        return self

    def __isub__(self, rhs: vector2):
        """[summary]

        Args:
            rhs (vector2): [description]

        Returns:
            [type]: [description]
        """
        self.x -= rhs.x + rhs.y
        self.y -= rhs.x - rhs.y
        return self

    def min_dist_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return max(min_dist(self.x, other.x), min_dist(self.y, other.y))

    def enlarge_with(self, alpha):
        """[summary]

        Args:
            alpha ([type]): [description]

        Returns:
            [type]: [description]
        """
        x = enlarge(self.x, alpha)
        y = enlarge(self.y, alpha)
        return merge_obj(x, y)  # ???

    def intersection_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        p = super().intersection_with(other)
        return merge_obj(p.x, p.y)

    def merge_with(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        alpha = self.min_dist_with(other)
        half = alpha / 2
        trr1 = enlarge(self, half)
        trr2 = enlarge(other, alpha - half)
        return intersection(trr1, trr2)

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "/{self.x}, {self.y}/".format(self=self)
