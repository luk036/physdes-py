"""
Interval Class

This code defines an Interval class, which represents a range of numbers with a lower bound
and an upper bound. The purpose of this class is to provide a way to work with intervals
of numbers, allowing various operations and comparisons to be performed on them.

The Interval class takes two inputs when creating an instance: a lower bound (lb) and an
upper bound (ub). These can be either integers or floating-point numbers. The class then
stores these values and provides methods to access and manipulate them.

The main outputs of this class are the results of various operations on intervals, such as
checking if two intervals overlap, finding the intersection between intervals, or
calculating the minimum distance between intervals.

The class achieves its purpose by implementing a variety of methods that perform
calculations and comparisons on the lower and upper bounds of the intervals. For example,
the overlaps method checks if two intervals have any numbers in common, while the contains
method determines if a given number or interval is entirely within another interval.

Some important logic flows in this code include:

1. Comparison operations: The class implements methods like __lt__, __gt__, __le__, and
   __ge__ to compare intervals with other intervals or single numbers.
2. Arithmetic operations: Methods like __add__, __sub__, and __mul__ allow intervals to be
   added, subtracted, or multiplied by scalar values.
3. Set-like operations: The hull_with method finds the smallest interval that contains both
   the current interval and another interval or number, while intersect_with finds the
   overlap between two intervals.

The code also includes utility functions outside the class, such as hull and enlarge, which
can work with both Interval objects and scalar values. These functions provide a more
flexible way to perform operations on intervals and numbers.

Overall, this Interval class provides a comprehensive set of tools for working with ranges
of numbers, which can be useful in various applications such as scheduling, resource
allocation, or numerical analysis. It allows programmers to easily manipulate and compare
intervals without having to manually handle the lower and upper bounds separately.
"""

from typing import Any, Generic, TypeVar, Union

from .generic import displacement, min_dist

T = TypeVar("T", int, float)


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

    def __repr__(self) -> str:
        """
        The `__repr__` function returns a string representation of an `Interval` object, including the class
        name and its lower and upper bounds, which is useful for debugging.

        :return: The `__repr__` method is returning a string representation of the `Interval` object.

        Examples:
            >>> a = Interval(3, 4)
            >>> repr(a)
            'Interval(3, 4)'
        """
        return f"{self.__class__.__name__}({self.lb}, {self.ub})"

    def __str__(self) -> str:
        """
        The `__str__` function returns a string representation of an Interval object in the format
        "[lb, ub]".

        :return: The method `__str__` returns a string representation of the object. In this case, it
            returns a string in the format "[lb, ub]", where lb is the lower bound and ub is the upper
            bound of the interval.

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

    def is_invalid(self) -> bool:
        """
        Check if the interval is invalid (lower bound is greater than upper bound).

        :return: True if the interval is invalid, False otherwise.

        Examples:
            >>> a = Interval(3, 4)
            >>> a.is_invalid()
            False
            >>> b = Interval(4, 3)
            >>> b.is_invalid()
            True
        """
        return self.lb > self.ub

    # def copy(self) -> "Interval[T]":
    #     """
    #     The `copy` function returns a new instance of the same class with the same lower and upper
    #     bounds.
    #     :return: The `copy` method is returning a new instance of the same class as `self`, with the
    #         same lower bound (`_lb`) and upper bound (`_ub`) values.
    #
    #     Examples:
    #         >>> a = Interval(3, 4)
    #         >>> print(a.copy())
    #         [3, 4]
    #     """
    #     S = type(self)
    #     return S(self._lb, self._ub)

    def measure(self) -> T:
        """
        Calculates the measure (length) of the interval.

        The measure (length) is the difference between the upper and lower bounds.

        :return: The measure (length) of the interval.

        Examples:
            >>> a = Interval(3, 4)
            >>> a.measure()
            1
            >>> b = Interval(3, 8)
            >>> b.measure()
            5
        """
        return self.ub - self.lb

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Interval):
            return NotImplemented
        return (self.lb, self.ub) == (other.lb, other.ub)

    def __lt__(self, other: Union["Interval[T]", T]) -> bool:
        """
        Checks if this interval is strictly to the left of another value.

        This method returns `True` if the upper bound of this interval is less than
        the given value (or the lower bound of the given interval).

        :param other: The value or interval to compare with.
        :type other: Union[Interval[T], T]
        :return: `True` if this interval is strictly to the left of `other`.

        Examples:
            >>> a = Interval(3, 4)
            >>> b = Interval(5, 6)
            >>> a < b
            True
            >>> a < 5
            True
            >>> b < a
            False
            >>> a < 4
            False
        """
        return self.ub < other

    def __gt__(self, other: Union["Interval[T]", T]) -> bool:
        """
        Checks if this interval is strictly to the right of another value.

        This method returns `True` if the lower bound of this interval is greater than
        the given value (or the upper bound of the given interval).

        :param other: The value or interval to compare with.
        :type other: Union[Interval[T], T]
        :return: `True` if this interval is strictly to the right of `other`.

        Examples:
            >>> a = Interval(5, 6)
            >>> b = Interval(3, 4)
            >>> a > b
            True
            >>> a > 4
            True
            >>> b > a
            False
            >>> a > 5
            False
        """
        return self.lb > other

    def __le__(self, other: Union["Interval[T]", T]) -> bool:
        """
        Checks if this interval is not strictly to the right of another value.

        This method returns `True` if this interval is not strictly greater than the
        given value or interval.

        :param other: The value or interval to compare with.
        :type other: Union[Interval[T], T]
        :return: `True` if this interval is less than or equal to `other`.

        Examples:
            >>> a = Interval(3, 5)
            >>> b = Interval(5, 7)
            >>> a <= b
            True
            >>> a <= 5
            True
            >>> b <= a
            True
            >>> a <= 3
            True
        """
        return not (other < self.lb)

    def __ge__(self, other: Union["Interval[T]", T]) -> bool:
        """
        Checks if this interval is not strictly to the left of another value.

        This method returns `True` if this interval is not strictly less than the
        given value or interval.

        :param other: The value or interval to compare with.
        :type other: Union[Interval[T], T]
        :return: `True` if this interval is greater than or equal to `other`.

        Examples:
            >>> a = Interval(5, 7)
            >>> b = Interval(3, 5)
            >>> a >= b
            True
            >>> a >= 5
            True
            >>> b >= a
            True
            >>> a >= 7
            True
        """
        return not (self.ub < other)

    def __neg__(self) -> "Interval[T]":
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

    def __iadd__(self, rhs: Union["Interval[T]", T]) -> "Interval[T]":
        """
        The `__iadd__` method allows for in-place addition of an `Interval` object.

        :param rhs: The parameter `rhs` represents the right-hand side value that is being added to the
            current object. In this case, it is expected to be of type `T`, which is a generic type

        :type rhs: T

        :return: The method `__iadd__` returns `self`, which is an instance of the class `"Interval[T]"`.

        Examples:
            >>> a = Interval(3, 4)
            >>> a += 10
            >>> print(a)
            [13, 14]
        """
        if isinstance(rhs, Interval):
            self._lb += rhs.lb
            self._ub += rhs.ub
        else:
            self._lb += rhs
            self._ub += rhs
        return self

    def __add__(self, rhs: Union["Interval[T]", T]) -> "Interval[T]":
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
        if isinstance(rhs, Interval):
            return S(self.lb + rhs.lb, self.ub + rhs.ub)
        return S(self.lb + rhs, self.ub + rhs)

    def __radd__(self, lhs: T) -> "Interval[T]":
        """
        The `__radd__` function allows for in-place addition of an `Interval` object.

        :param lhs: The parameter `lhs` represents the left-hand side value that is being added to the
            current object. In this case, it is expected to be of type `T`, which is a generic type

        :type lhs: T

        :return: The method `__radd__` returns `self`, which is an instance of the class `"Interval[T]"`.
        """
        return self + lhs

    def __isub__(self, rhs: Union["Interval[T]", T]) -> "Interval[T]":
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
        if isinstance(rhs, Interval):
            self._lb -= rhs.lb
            self._ub -= rhs.ub
        else:
            self._lb -= rhs
            self._ub -= rhs
        return self

    def __sub__(self, rhs: Union["Interval[T]", T]) -> "Interval[T]":
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
        if isinstance(rhs, Interval):
            return S(self.lb - rhs.lb, self.ub - rhs.ub)
        return S(self.lb - rhs, self.ub - rhs)

    def __rsub__(self, lhs: T) -> "Interval[T]":
        """
        The `__rsub__` function allows for in-place subtraction of an `Interval` object.

        :param lhs: The parameter `lhs` represents the left-hand side value that is being subtracted from the
            current object. In this case, it is expected to be of type `T`, which is a generic type

        :type lhs: T

        :return: The method `__rsub__` returns `self`, which is an instance of the class `"Interval[T]"`.
        """
        S = type(self)
        return S(lhs - self.lb, lhs - self.ub)

    def __imul__(self, rhs: T) -> "Interval[T]":
        """
        The `__imul__` method allows for in-place multiplication of an `Interval` object.

        :param rhs: The parameter `rhs` represents the right-hand side value that is being multiplied to the
            current object. In this case, it is expected to be of type `T`, which is a generic type

        :type rhs: T

        :return: The method `__imul__` returns `self`, which is an instance of the class `"Interval[T]"`.

        Examples:
            >>> a = Interval(3, 4)
            >>> a *= 10
            >>> print(a)
            [30, 40]
        """
        self._lb *= rhs
        self._ub *= rhs
        return self

    def __mul__(self, rhs: T) -> "Interval[T]":
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

    def __truediv__(self, rhs: T) -> "Interval[T]":
        """
        The function overloads the "/" operator to divide a constant value to the lower and upper bounds of
        an Interval object.
        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the value that is
            being divided to the current object
        :type rhs: T
        :return: The method is returning a new instance of the class `S` (which is the same type as
            `self`) with the lower bound (`lb`) and upper bound (`ub`) incremented by `rhs`.
        """
        S = type(self)
        return S(self.lb / rhs, self.ub / rhs)  # type: ignore

    def __floordiv__(self, rhs: T) -> "Interval[T]":
        """
        The function overloads the "//" operator to floor divide a constant value to the lower and upper bounds of
        an Interval object.
        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the value that is
            being divided to the current object
        :type rhs: T
        :return: The method is returning a new instance of the class `S` (which is the same type as
            `self`) with the lower bound (`lb`) and upper bound (`ub`) incremented by `rhs`.
        """
        S = type(self)
        return S(self.lb // rhs, self.ub // rhs)

    def overlaps(self, other: Union["Interval[T]", T]) -> bool:
        """
        The `overlaps` function checks if two intervals overlap with each other.

        :param other: The parameter "other" is of type Union["Interval[T]", T], which means it can accept either
            an object of the same class as "self" or an object of type "T"

        :type other: Union["Interval[T]", T]

        :return: a boolean value, either True or False.

        .. svgbob::
           :align: center

              <-- self -->
                    <-- other -->

        Examples:
            >>> a = Interval(3, 5)
            >>> a.overlaps(Interval(4, 9))
            True
            >>> a.overlaps(Interval(6, 9))
            False
            >>> Interval(1, 5).overlaps(Interval(5, 7))
            True
            >>> Interval(1, 5).overlaps(Interval(0, 1))
            True
        """
        return not (self < other or other < self)

    def contains(self, obj: Union["Interval[T]", T]) -> bool:
        """
        The `contains` function checks if an object is contained within a given interval.

        :param obj: The `obj` parameter can be either an instance of the `Interval` class or an integer
        :type obj: Union["Interval[T]", T]
        :return: The `contains` method returns a boolean value indicating whether the given object is
            contained within the interval.

        .. svgbob::
           :align: center

            <---- self ---->
               <-- obj -->

        Examples:
            >>> a = Interval(3, 8)
            >>> a.contains(4)
            True
            >>> a.contains(Interval(4, 7))
            True
            >>> a.contains(Interval(6, 9))
            False
            >>> a.contains(3)
            True
            >>> a.contains(8)
            True
        """
        # `obj` can be an Interval or int
        if isinstance(obj, Interval):
            return self.lb <= obj.lb and obj.ub <= self.ub
        else:  # assume scalar
            return self.lb <= obj <= self.ub

    def hull_with(self, obj: Union["Interval[T]", T]) -> "Interval[T]":
        """
        The `hull_with` function takes an object (either an `Interval` or a scalar) and returns a new
        `Interval` object that represents the hull (smallest interval that contains both intervals) of
        the current `Interval` object and the input object.

        :param obj: The `obj` parameter can be either an instance of the same class (`"Interval[T]"`) or a scalar value (`T`)
        :type obj: Union["Interval[T]", T]
        :return: The method `hull_with` returns an `Interval` object.

        .. svgbob::
           :align: center

            <---- hull ------>
            <-- self -->
                   <-- obj -->

        Examples:
            >>> a = Interval(3, 8)
            >>> print(a.hull_with(Interval(4, 7)))
            [3, 8]
            >>> print(a.hull_with(Interval(6, 9)))
            [3, 9]
            >>> print(a.hull_with(Interval(0, 2)))
            [0, 8]
        """
        if isinstance(obj, Interval):
            return Interval(min(self.lb, obj.lb), max(self.ub, obj.ub))
        else:  # assume scalar
            return Interval(min(self.lb, obj), max(self.ub, obj))

    def intersect_with(self, obj: Union["Interval[T]", T]) -> "Interval[T]":
        """
        The `intersect_with` function takes in an object and returns the intersection between the
        object and the current interval.

        :param obj: The `obj` parameter can be either an instance of the `"Interval[T]"` class (which is the same
            class as `self`), or it can be of type `T`, which is a generic type

        :type obj: Union["Interval[T]", T]

        :return: The `intersect_with` method returns an `Interval` object that represents the
            intersection between the current `Interval` object (`self`) and the input object (`obj`).

        .. svgbob::
           :align: center

              <-- self -->
                    <-- obj -->
                    <---->
               intersection

        Examples:
            >>> a = Interval(3, 8)
            >>> print(a.intersect_with(4))
            [4, 4]
            >>> print(a.intersect_with(Interval(4, 7)))
            [4, 7]
            >>> print(a.intersect_with(Interval(6, 9)))
            [6, 8]
            >>> print(a.intersect_with(Interval(3, 5)))
            [3, 5]
            >>> print(a.intersect_with(Interval(5, 7)))
            [5, 7]
            >>> print(a.intersect_with(Interval(3, 6)))
            [3, 6]
            >>> print(a.intersect_with(Interval(5, 8)))
            [5, 8]
            >>> print(a.intersect_with(Interval(3, 7)))
            [3, 7]
            >>> print(a.intersect_with(Interval(0, 2)))
            [3, 2]
        """
        # `a` can be an Interval or int
        # assert self.overlaps(obj)
        if isinstance(obj, Interval):
            return Interval(max(self.lb, obj.lb), min(self.ub, obj.ub))
        else:  # assume scalar
            return Interval(max(self.lb, obj), min(self.ub, obj))

    def min_dist_with(self, obj: Union["Interval[T]", T]) -> T | int:
        """
        The function calculates the minimum distance between two objects.

        :param obj: The parameter `obj` can be of type `"Interval[T]"` or `T`
        :type obj: Union["Interval[T]", T]
        :return: The function `min_dist_with` returns the minimum distance between the given object
            `obj` and the current object `self`.

        .. svgbob::
           :align: center

              <-- self -->   <-- dist -->   <-- obj -->

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
            >>> print(a.min_dist_with(Interval(0, 2)))
            1
        """
        if self < obj:
            return min_dist(self.ub, obj)
        if obj < self:
            return min_dist(self.lb, obj)
        return 0

    def nearest_to(self, obj: T) -> T:
        """
        Return the nearest position with respect to obj

        Examples:
            >>> a = Interval(3, 5)
            >>> print(a.nearest_to(8))
            5
            >>> print(a.nearest_to(0))
            3
            >>> print(a.nearest_to(4))
            4
        """
        if self < obj:
            return self.ub
        if obj < self:
            return self.lb
        return obj

    def displace(self, obj: "Interval[T]") -> "Interval[T]":
        """
        The `displace` function takes an object as an argument and returns a new Interval object with
        the lower and upper bounds displaced by the corresponding bounds of the input object.

        :param obj: The `obj` parameter is an object of the same class as the `self` object. It
            represents another interval that will be used to displace the current interval

        :type obj: "Interval[T]"

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

    def get_center(self) -> T:
        """
        Calculates the center of the point.

        :return: The center of the point.

        Examples:
            >>> a = Interval(3, 7)
            >>> a.get_center()
            5
        """
        return self.lb + (self.ub - self.lb) // 2

    def lower_corner(self) -> T:
        """
        Calculates the lower corner of the point.

        :return: The lower corner of the point.

        Examples:
            >>> a = Interval(3, 7)
            >>> a.lower_corner()
            3
        """
        return self.lb

    def upper_corner(self) -> T:
        """
        Calculates the upper corner of the point.

        :return: The upper corner of the point.

        Examples:
            >>> a = Interval(3, 7)
            >>> a.upper_corner()
            7
        """
        return self.ub

    # def min_dist_change_with(self, obj: Union["Interval[T]", T]):
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
    #         self = obj = self.intersect_with(obj)  # what???
    #     else:  # assume scalar
    #         self._ub = self._lb = obj
    #     return 0

    def enlarge_with(self, alpha: T) -> "Interval[T]":
        """
        The `enlarge_with` function takes a value `alpha` and returns a new instance of the same type
        with the lower bound decreased by `alpha` and the upper bound increased by `alpha`.

        :param alpha: The parameter "alpha" represents the amount by which the interval should be enlarged

        :type alpha: T

        :return: The method `enlarge_with` returns a new instance of the same class (`"Interval[T]"`) with the
            lower bound decreased by `alpha` and the upper bound increased by `alpha`.

        Examples:
            >>> a = Interval(3, 5)
            >>> print(a.enlarge_with(2))
            [1, 7]
        """
        S = type(self)
        return S(self._lb - alpha, self._ub + alpha)


def hull(lhs: Any, rhs: Any) -> "Interval[T]":
    """
    Calculates the convex hull of two objects, returning the smallest interval
    that contains both.

    This function can take two intervals, two scalars, or an interval and a scalar.

    :param lhs: The first object (Interval or scalar).
    :param rhs: The second object (Interval or scalar).
    :return: The smallest `Interval` that contains both `lhs` and `rhs`.

    Examples:
        >>> a = Interval(3, 5)
        >>> print(hull(a, 4))
        [3, 5]
        >>> print(hull(a, Interval(4, 7)))
        [3, 7]
        >>> print(hull(a, Interval(6, 9)))
        [3, 9]
        >>> print(hull(a, Interval(0, 2)))
        [0, 5]
        >>> print(hull(2, 5))
        [2, 5]
    """
    if hasattr(lhs, "hull_with"):
        return lhs.hull_with(rhs)
    elif hasattr(rhs, "hull_with"):
        return rhs.hull_with(lhs)
    else:  # assume scalar
        return Interval(lhs, rhs) if lhs < rhs else Interval(rhs, lhs)


def enlarge(lhs: Any, rhs: T) -> "Interval[T]":
    """
    Enlarges an interval or scalar by a given amount.

    If `lhs` is an `Interval`, it is enlarged by `rhs`. If `lhs` is a scalar, it is
    treated as a zero-width interval and enlarged by `rhs`.

    :param lhs: The interval or scalar to enlarge.
    :param rhs: The amount to enlarge by.
    :return: The enlarged `Interval`.

    Examples:
        >>> a = Interval(3, 5)
        >>> print(enlarge(a, 2))
        [1, 7]
        >>> print(enlarge(a, -1))
        [4, 4]
        >>> print(enlarge(5, 2))
        [3, 7]
    """
    if hasattr(lhs, "enlarge_with"):
        return lhs.enlarge_with(rhs)
    else:  # assume scalar
        return Interval(lhs - rhs, lhs + rhs)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
