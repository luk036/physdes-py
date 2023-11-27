from typing import Generic, TypeVar, Union

from typing_extensions import Self

T = TypeVar("T", int, float)


def overlap(lhs, rhs) -> bool:
    """
    The `overlap` function checks if two objects have an overlapping property or are equal.

    :param lhs: The `lhs` parameter represents the left-hand side object that we want to check for
    overlap with the `rhs` parameter

    :param rhs: The parameter `rhs` is the right-hand side of the comparison. It can be any object that
    supports the `overlaps` method or a scalar value

    :return: a boolean value.

    Examples:
        >>> overlap(1, 1)
        True
        >>> overlap(1, 3)
        False
        >>> overlap(Interval(1, 2), Interval(2, 3))
        True
        >>> overlap(Interval(1, 2), Interval(3, 4))
        False
        >>> overlap(Interval(1, 2), 2)
        True
        >>> overlap(Interval(1, 2), 4)
        False
        >>> overlap(2, Interval(2, 3))
        True
        >>> overlap(1, Interval(3, 4))
        False
        >>> overlap(1, Interval(1, 2))
        True
    """
    if hasattr(lhs, "overlaps"):
        return lhs.overlaps(rhs)
    elif hasattr(rhs, "overlaps"):
        return rhs.overlaps(lhs)
    else:  # assume scalar
        return lhs == rhs


def contain(lhs, rhs) -> bool:
    """
    The `contain` function checks if one object contains another object.

    :param lhs: The `lhs` parameter represents the left-hand side of the comparison, while the `rhs`
    parameter represents the right-hand side of the comparison

    :param rhs: The `rhs` parameter represents the right-hand side of the comparison. It can be any
    value or object that you want to check if it is contained within the `lhs` object

    :return: a boolean value.

    Examples:
        >>> contain(1, 1)
        True
        >>> contain(1, 3)
        False
        >>> contain(Interval(1, 4), Interval(2, 3))
        True
        >>> contain(Interval(1, 2), Interval(3, 4))
        False
        >>> contain(Interval(1, 2), 2)
        True
        >>> contain(Interval(1, 2), 4)
        False
        >>> contain(2, Interval(2, 3))
        False
        >>> contain(1, Interval(3, 4))
        False
    """
    if hasattr(lhs, "contains"):
        return lhs.contains(rhs)
    elif hasattr(rhs, "contains"):
        return False
    else:  # assume scalar
        return lhs == rhs


def intersection(lhs, rhs):
    """
    The `intersection` function returns the intersection of two objects if they have an
    `intersection_with` method, otherwise it returns the objects themselves if they are equal.

    :param lhs: The `lhs` parameter represents the left-hand side of the intersection operation, while
    the `rhs` parameter represents the right-hand side of the intersection operation

    :param rhs: The `rhs` parameter is the second input to the `intersection` function. It represents
    the right-hand side of the intersection operation

    :return: the intersection of `lhs` and `rhs`.

    Examples:
        >>> print(intersection(1, 1))
        1
        >>> print(intersection(Interval(1, 2), Interval(2, 3)))
        [2, 2]
        >>> print(intersection(Interval(1, 2), 2))
        [2, 2]
        >>> print(intersection(2, Interval(2, 3)))
        [2, 2]
        >>> print(intersection(1, Interval(1, 2)))
        [1, 1]
        >>> print(intersection(Interval(1, 2), Interval(1, 2)))
        [1, 2]
        >>> print(intersection(Interval(1, 2), Interval(2, 3)))
        [2, 2]
        >>> print(intersection(Interval(1, 2), 2))
        [2, 2]
    """
    if hasattr(lhs, "intersection_with"):
        return lhs.intersection_with(rhs)
    elif hasattr(rhs, "intersection_with"):
        return rhs.intersection_with(lhs)
    else:  # assume scalar
        assert lhs == rhs
        return lhs


def min_dist(lhs, rhs):
    """
    The `min_dist` function calculates the minimum distance between two objects, using their
    `min_dist_with` method if available, or by subtracting them if they are scalars.

    :param lhs: The `lhs` parameter represents the left-hand side value or object that we want to
    calculate the minimum distance with

    :param rhs: The parameter `rhs` represents the right-hand side value or object that we want to
    compare with the left-hand side value or object `lhs`

    :return: the minimum distance between `lhs` and `rhs`.

    Examples:
        >>> min_dist(1, 1)
        0
        >>> min_dist(1, 3)
        2
        >>> min_dist(Interval(1, 2), Interval(2, 3))
        0
        >>> min_dist(Interval(1, 2), Interval(3, 4))
        1
        >>> min_dist(Interval(1, 2), 2)
        0
        >>> min_dist(Interval(1, 2), 4)
        2
        >>> min_dist(2, Interval(2, 3))
        0
        >>> min_dist(1, Interval(3, 4))
        2
        >>> min_dist(1, Interval(1, 2))
        0
        >>> min_dist(Interval(1, 2), Interval(1, 2))
        0
        >>> min_dist(Interval(1, 2), Interval(2, 3))
        0
        >>> min_dist(Interval(1, 2), 2)
        0
        >>> min_dist(2, Interval(2, 3))
        0
    """
    if hasattr(lhs, "min_dist_with"):
        return lhs.min_dist_with(rhs)
    elif hasattr(rhs, "min_dist_with"):
        return rhs.min_dist_with(lhs)
    else:  # assume scalar
        return abs(lhs - rhs)


# def min_dist_change(lhs, rhs):
#     """
#     The `min_dist_change` function calculates the minimum distance change between two objects.
#
#     :param lhs: The `lhs` parameter represents the left-hand side value or object that you want to
#     compare
#     :param rhs: The `rhs` parameter represents the right-hand side value or object that we want to
#     compare with the `lhs` parameter
#     :return: The function `min_dist_change` returns the minimum distance change between `lhs` and `rhs`.
#
#     Examples:
#         >>> min_dist_change(1, 1)
#         0
#         >>> min_dist_change(1, 3)
#         2
#         >>> min_dist_change(Interval(1, 2), Interval(2, 3))
#         0
#         >>> min_dist_change(Interval(1, 2), Interval(3, 4))
#         1
#         >>> min_dist_change(Interval(1, 2), 2)
#         0
#         >>> min_dist_change(Interval(1, 2), 4)
#         2
#         >>> min_dist_change(2, Interval(2, 3))
#         0
#         >>> min_dist_change(1, Interval(3, 4))
#         2
#         >>> min_dist_change(1, Interval(1, 2))
#         0
#         >>> min_dist_change(Interval(1, 2), Interval(1, 2))
#         0
#         >>> min_dist_change(Interval(1, 2), Interval(2, 3))
#         0
#         >>> min_dist_change(Interval(1, 2), 2)
#         0
#     """
#     if hasattr(lhs, "min_dist_change_with"):
#         return lhs.min_dist_change_with(rhs)
#     elif hasattr(rhs, "min_dist_change_with"):
#         return rhs.min_dist_change_with(lhs)
#     else:  # assume scalar
#         return abs(lhs - rhs)


def displacement(lhs, rhs):
    """
    The `displacement` function calculates the displacement between two objects or scalars.

    :param lhs: The `lhs` parameter represents the left-hand side of the displacement operation. It can
    be either an object that has a `displace` method or a scalar value

    :param rhs: The `rhs` parameter represents the displacement value that needs to be subtracted from
    the `lhs` parameter

    :return: the displacement between `lhs` and `rhs`. If `lhs` has a `displace` method, it calls that
    method passing `rhs` as an argument. Otherwise, it assumes `lhs` is a scalar and returns the
    difference between `lhs` and `rhs`.

    Examples:
        >>> displacement(1, 1)
        0
        >>> displacement(1, 3)
        -2
        >>> print(displacement(Interval(1, 2), Interval(2, 3)))
        [-1, -1]
        >>> print(displacement(Interval(1, 2), Interval(3, 4)))
        [-2, -2]
    """
    if hasattr(lhs, "displace"):
        return lhs.displace(rhs)
    else:  # assume scalar
        return lhs - rhs


class Interval(Generic[T]):
    __slots__ = ("_lb", "_ub")

    def __init__(self, lb: T, ub: T) -> None:
        """
        The function initializes an Interval object with lower bound `lb` and upper bound `ub`.

        :param lb: The `lb` parameter represents the lower bound of the interval. It is of type `T`,
        which means it can be any data type

        :type lb: T

        :param ub: The `ub` parameter represents the upper bound of the interval. It is the maximum
        value that the interval can take

        :type ub: T

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a)
            [3, 4]
            >>> print(a.lb)
            3
            >>> print(a.ub)
            4
        """
        self._lb: T = lb
        self._ub: T = ub

    def __str__(self) -> str:
        """
        The `__str__` function returns a string representation of an Interval object in the format "[lb, ub]".

        :return: The method `__str__` returns a string representation of the object. In this case, it
        returns a string in the format "[lb, ub]", where lb is the lower bound and ub is the upper bound
        of the interval.

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a)
            [3, 4]
        """
        return f"[{self.lb}, {self.ub}]"

    @property
    def lb(self) -> T:
        """
        The function `lb` returns the lower bound of an interval.

        :return: The method is returning the lower bound of the interval.

        Examples:
            >>> a = Interval(3, 4)
            >>> a.lb
            3
        """
        return self._lb

    @property
    def ub(self) -> T:
        """
        The function `ub` returns the upper bound of an interval.

        :return: The method is returning the upper bound of the interval.

        Examples:
            >>> a = Interval(3, 4)
            >>> a.ub
            4
        """
        return self._ub

    # def copy(self) -> Self:
    #     """
    #     The `copy` function returns a new instance of the same class with the same lower and upper
    #     bounds.
    #     :return: The `copy` method is returning a new instance of the same class as `self`, with the
    #     same lower bound (`_lb`) and upper bound (`_ub`) values.
    #
    #     Examples:
    #         >>> a = Interval(3, 4)
    #         >>> print(a.copy())
    #         [3, 4]
    #     """
    #     S = type(self)
    #     return S(self._lb, self._ub)

    def length(self) -> T:
        """
        The function returns the length of a range defined by the upper bound (ub) and lower bound (lb)
        attributes.

        :return: The length of the object, which is calculated by subtracting the upper bound (ub) from
        the lower bound (lb).

        Examples:
            >>> a = Interval(3, 4)
            >>> a.length()
            1
        """
        return self.ub - self.lb

    def __eq__(self, other) -> bool:
        """
        The function checks if two Interval objects have the same lower and upper bounds.

        :param other: The "other" parameter represents another object that we are comparing with the
        current object. In this case, it is used to compare two Interval objects and check if they are
        equal

        :return: The `__eq__` method is returning a boolean value.

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(3, 5)
            >>> a == b
            False
        """
        return (self.lb, self.ub) == (other.lb, other.ub)

    def __lt__(self, other) -> bool:
        """
        The function compares the upper bound of the current object with the other object and returns
        True if the upper bound of the current object is less than the other object.

        :param other: The "other" parameter represents the value that the current object is being
        compared to. In this case, it is being compared to the upper bound (ub) of the current object

        :return: The code is returning a boolean value indicating whether the upper bound of the current
        interval object is less than the other object.

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
        """
        The function compares the upper bound of the current object with the other object and returns
        True if the lower bound of the current object is greater than the other object.

        :param other: The "other" parameter represents the value that the current object is being
        compared to. In this case, it is being compared to the lower bound (lb) of the current object

        :return: The code is returning a boolean value indicating whether the lower bound of the current
        interval object is greater than the other object.

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
        """
        The function returns True if the current interval is less than or equal to the the other interval.

        :param other: The `other` parameter represents another instance of the `Interval` class that we
        are comparing to the current instance

        :return: The code is returning a boolean value.

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
        """
        The function returns True if the current interval is greater than or equal to the the other interval.

        :param other: The `other` parameter represents another instance of the `Interval` class that we
        are comparing to the current instance

        :return: The code is returning a boolean value.

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(3, 5)
            >>> a >= b
            True
            >>> b >= a
            True
        """
        return not (self.ub < other)

    def __neg__(self) -> Self:
        """
        The `__neg__` function returns a new instance of the class with the lower and upper bounds negated.

        :return: The `__neg__` method returns a new instance of the same class (`S`) with the lower
        bound (`lb`) and upper bound (`ub`) negated.

        Examples:
            >>> a = Interval(3, 4)
            >>> print(-a)
            [-4, -3]
        """
        S = type(self)
        return S(-self.ub, -self.lb)

    def __iadd__(self, rhs: T) -> Self:
        """
        The `__iadd__` method allows for in-place addition of an `Interval` object.

        :param rhs: The parameter `rhs` represents the right-hand side value that is being added to the
        current object. In this case, it is expected to be of type `T`, which is a generic type

        :type rhs: T

        :return: The method `__iadd__` returns `self`, which is an instance of the class `Self`.

        Examples:
            >>> a = Interval(3, 4)
            >>> a += 10
            >>> print(a)
            [13, 14]
        """
        self._lb += rhs
        self._ub += rhs
        return self

    def __add__(self, rhs: T) -> Self:
        """
        The function overloads the "+" operator to add a constant value to the lower and upper bounds of
        an Interval object.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the value that is
        being added to the current object

        :type rhs: T

        :return: The method is returning a new instance of the class `S` (which is the same type as
        `self`) with the lower bound (`lb`) and upper bound (`ub`) incremented by `rhs`.

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a + 10)
            [13, 14]
        """
        S = type(self)
        return S(self.lb + rhs, self.ub + rhs)

    def __isub__(self, rhs: T) -> Self:
        """
        The function subtracts a value from both the lower and upper bounds of an Interval object and
        returns the modified object.

        :param rhs: The parameter `rhs` represents the right-hand side value that will be subtracted
        from the current object. In this case, it is expected to be of type `T`, which is a generic type

        :type rhs: T

        :return: The method is returning `self`, which is an instance of the class that the method
        belongs to.

        Examples:
            >>> a = Interval(3, 4)
            >>> a -= 1
            >>> print(a)
            [2, 3]
        """
        self._lb -= rhs
        self._ub -= rhs
        return self

    def __sub__(self, rhs: T) -> Self:
        """
        The function subtracts a value from the lower and upper bounds of an interval and returns a new
        interval.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the value that is
        being subtracted from the interval

        :type rhs: T

        :return: The method is returning a new instance of the class `S` (which is the same type as
        `self`) with the lower bound (`lb`) and upper bound (`ub`) subtracted by `rhs`.

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a - 1)
            [2, 3]
        """
        S = type(self)
        return S(self.lb - rhs, self.ub - rhs)

    def __imul__(self, rhs: T) -> Self:
        """
        The `__imul__` method allows for in-place multiplication of an `Interval` object.

        :param rhs: The parameter `rhs` represents the right-hand side value that is being multiplied to the
        current object. In this case, it is expected to be of type `T`, which is a generic type

        :type rhs: T

        :return: The method `__imul__` returns `self`, which is an instance of the class `Self`.

        Examples:
            >>> a = Interval(3, 4)
            >>> a *= 10
            >>> print(a)
            [30, 40]
        """
        self._lb *= rhs
        self._ub *= rhs
        return self

    def __mul__(self, rhs: T) -> Self:
        """
        The function overloads the "*" operator to multiply a constant value to the lower and upper bounds of
        an Interval object.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the value that is
        being multiplied to the current object

        :type rhs: T

        :return: The method is returning a new instance of the class `S` (which is the same type as
        `self`) with the lower bound (`lb`) and upper bound (`ub`) incremented by `rhs`.

        Examples:
            >>> a = Interval(3, 4)
            >>> print(a * 10)
            [30, 40]
        """
        S = type(self)
        return S(self.lb * rhs, self.ub * rhs)

    def overlaps(self, other: Union[Self, T]) -> bool:
        """
        The `overlaps` function checks if two intervals overlap with each other.

        :param other: The parameter "other" is of type Union[Self, T], which means it can accept either
        an object of the same class as "self" or an object of type "T"

        :type other: Union[Self, T]

        :return: a boolean value, either True or False.

        Examples:
            >>> a = Interval(3, 5)
            >>> a.overlaps(Interval(4, 9))
            True
            >>> a.overlaps(Interval(6, 9))
            False
        """
        return not (self < other or other < self)

    def contains(self, obj: Union[Self, T]) -> bool:
        """
        The `contains` function checks if an object is contained within a given interval.

        :param obj: The `obj` parameter can be either an instance of the `Interval` class or an integer
        :type obj: Union[Self, T]
        :return: The `contains` method returns a boolean value indicating whether the given object is
        contained within the interval.

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

    def hull_with(self, obj: Union[Self, T]):
        """
        The `hull_with` function takes an object (either an `Interval` or a scalar) and returns a new
        `Interval` object that represents the hull (smallest interval that contains both intervals) of
        the current `Interval` object and the input object.

        :param obj: The `obj` parameter can be either an instance of the same class (`Self`) or a scalar value (`T`)
        :type obj: Union[Self, T]
        :return: The method `hull_with` returns an `Interval` object.

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

    def intersection_with(self, obj: Union[Self, T]):
        """
        The `intersection_with` function takes in an object and returns the intersection between the
        object and the current interval.

        :param obj: The `obj` parameter can be either an instance of the `Self` class (which is the same
        class as `self`), or it can be of type `T`, which is a generic type

        :type obj: Union[Self, T]

        :return: The `intersection_with` method returns an `Interval` object that represents the
        intersection between the current `Interval` object (`self`) and the input object (`obj`).

        Examples:
            >>> a = Interval(3, 8)
            >>> print(a.intersection_with(4))
            [4, 4]
            >>> print(a.intersection_with(Interval(4, 7)))
            [4, 7]
            >>> print(a.intersection_with(Interval(6, 9)))
            [6, 8]
            >>> print(a.intersection_with(Interval(3, 5)))
            [3, 5]
            >>> print(a.intersection_with(Interval(5, 7)))
            [5, 7]
            >>> print(a.intersection_with(Interval(3, 6)))
            [3, 6]
            >>> print(a.intersection_with(Interval(5, 8)))
            [5, 8]
            >>> print(a.intersection_with(Interval(3, 7)))
            [3, 7]
        """
        # `a` can be an Interval or int
        assert self.overlaps(obj)
        if isinstance(obj, Interval):
            return Interval(max(self.lb, obj.lb), min(self.ub, obj.ub))
        else:  # assume scalar
            return Interval(obj, obj)

    def min_dist_with(self, obj: Union[Self, T]):
        """
        The function calculates the minimum distance between two objects.

        :param obj: The parameter `obj` can be of type `Self` or `T`
        :type obj: Union[Self, T]
        :return: The function `min_dist_with` returns the minimum distance between the given object
        `obj` and the current object `self`.

        Examples:
            >>> a = Interval(3, 5)
            >>> print(a.min_dist_with(2))
            1
            >>> print(a.min_dist_with(Interval(4, 7)))
            0
            >>> print(a.min_dist_with(Interval(6, 9)))
            1
            >>> print(a.min_dist_with(Interval(3, 5)))
            0
            >>> print(a.min_dist_with(Interval(5, 7)))
            0
        """
        if self < obj:
            return min_dist(self.ub, obj)
        if obj < self:
            return min_dist(self.lb, obj)
        return 0

    def displace(self, obj: Self):
        """
        The `displace` function takes an object as an argument and returns a new Interval object with
        the lower and upper bounds displaced by the corresponding bounds of the input object.

        :param obj: The `obj` parameter is an object of the same class as the `self` object. It
        represents another interval that will be used to displace the current interval

        :type obj: Self

        :return: The `displace` method returns an `Interval` object.

        Examples:
            >>> a = Interval(3, 5)
            >>> print(a.displace(Interval(4, 7)))
            [-1, -2]
            >>> print(a.displace(Interval(6, 9)))
            [-3, -4]
        """
        lb = displacement(self.lb, obj.lb)
        ub = displacement(self.ub, obj.ub)
        return Interval(lb, ub)

    # def min_dist_change_with(self, obj: Union[Self, T]):
    #     """[summary]
    #
    #     Args:
    #         other ([type]): [description]
    #
    #     Returns:
    #         [type]: [description]
    #     """
    #     if self < obj:
    #         self._lb = self._ub
    #         return min_dist_change(self._ub, obj)
    #     if obj < self:
    #         self._ub = self._lb
    #         return min_dist_change(self._lb, obj)
    #     S = type(self)
    #     if isinstance(obj, S):
    #         self = obj = self.intersection_with(obj)  # what???
    #     else:  # assume scalar
    #         self._ub = self._lb = obj
    #     return 0

    def enlarge_with(self, alpha: T) -> Self:
        """
        The `enlarge_with` function takes a value `alpha` and returns a new instance of the same type
        with the lower bound decreased by `alpha` and the upper bound increased by `alpha`.

        :param alpha: The parameter "alpha" represents the amount by which the interval should be enlarged

        :type alpha: T

        :return: The method `enlarge_with` returns a new instance of the same class (`Self`) with the
        lower bound decreased by `alpha` and the upper bound increased by `alpha`.

        Examples:
            >>> a = Interval(3, 5)
            >>> print(a.enlarge_with(2))
            [1, 7]
        """
        S = type(self)
        return S(self._lb - alpha, self._ub + alpha)


def hull(lhs, rhs):
    """
    The `hull` function calculates the convex hull of two objects.

    :param lhs: The `lhs` parameter represents the left-hand side of the operation, while the `rhs`
    parameter represents the right-hand side of the operation

    :param rhs: The `rhs` parameter is the right-hand side of the operation. It can be any value or
    object that supports the `hull_with` method

    :return: the hull of the input arguments.

    Examples:
        >>> a = Interval(3, 5)
        >>> print(hull(a, 4))
        [3, 5]
        >>> print(hull(a, Interval(4, 7)))
        [3, 7]
        >>> print(hull(a, Interval(6, 9)))
        [3, 9]
    """
    if hasattr(lhs, "hull_with"):
        return lhs.hull_with(rhs)
    elif hasattr(rhs, "hull_with"):
        return rhs.hull_with(lhs)
    else:  # assume scalar
        return Interval(min(lhs, rhs), max(lhs, rhs))


def enlarge(lhs, rhs: T):
    """
    The `enlarge` function takes two arguments, `lhs` and `rhs`, and returns the result of enlarging
    `lhs` by `rhs`.

    :param lhs: The `lhs` parameter represents the left-hand side of the operation. It can be either an
    object that has a method `enlarge_with`, or a scalar value

    :param rhs: The parameter `rhs` is the value by which the `lhs` object will be enlarged

    :type rhs: T

    :return: an enlarged interval or scalar value.

    Examples:
        >>> a = Interval(3, 5)
        >>> print(enlarge(a, 2))
        [1, 7]
        >>> print(enlarge(a, -1))
        [4, 4]
    """
    if hasattr(lhs, "enlarge_with"):
        return lhs.enlarge_with(rhs)
    else:  # assume scalar
        return Interval(lhs - rhs, lhs + rhs)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
