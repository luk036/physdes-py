"""
Vector2 Class
"""
from typing import TYPE_CHECKING, Generic, TypeVar

from typing_extensions import Self

if TYPE_CHECKING:
    from .interval import Interval

T1 = TypeVar("T1", int, float, "Interval[int]", "Interval[float]", "Vector2")
T2 = TypeVar("T2", int, float, "Interval[int]", "Interval[float]", "Vector2")


class Vector2(Generic[T1, T2]):
    x_: T1  # Can be int, Interval, and Vector2
    y_: T2  # Can be int and Interval

    __slots__ = ("x_", "y_")

    def __init__(self, x, y) -> None:
        """
        The `__init__` function initializes a Vector2 object with x and y coordinates.

        :param x: The x-coordinate of the vector. It represents the horizontal component of the vector in a
        2D space
        :param y: The parameter `y` represents the y-coordinate of the vector. It is used to specify the
        vertical component of the vector

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(v)
            <3, 4>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d)
            <<3, 4>, 5>
        """
        self.x_ = x
        self.y_ = y

    def __str__(self) -> str:
        """
        The `__str__` function returns a string representation of a Vector2 object in the format "<x, y>".
        :return: The `__str__` method is returning a string representation of the vector object.

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(v)
            <3, 4>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d)
            <<3, 4>, 5>
        """
        return f"<{self.x}, {self.y}>"

    @property
    def x(self) -> T1:
        """
        The function returns the x-coordinate of a vector.
        :return: The method `x` is returning the value of the attribute `x_`.

        Examples:
            >>> v = Vector2(3, 4)
            >>> v.x
            3
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d.x)
            <3, 4>
        """
        return self.x_

    @property
    def y(self) -> T2:
        """
        The function returns the y-coordinate of a vector.
        :return: The method `y` is returning the value of the `y_` attribute.

        Examples:
            >>> v = Vector2(3, 4)
            >>> v.y
            4
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d.y)
            5
        """
        return self.y_

    # def copy(self) -> Self:
    #     """
    #     The `copy` function returns a new instance of the same class with the same values as the original
    #     instance.
    #     :return: The `copy` method is returning a new instance of the same class (`Self`) with the same `x_`
    #     and `y_` attributes.
    #
    #     Examples:
    #         >>> v = Vector2(3, 4)
    #         >>> w = v.copy()
    #         >>> print(w)
    #         <3, 4>
    #         >>> v3d = Vector2(v, 5)  # vector in 3d
    #         >>> w3d = v3d.copy()
    #         >>> print(w3d)
    #         <<3, 4>, 5>
    #     """
    #     T = type(self)
    #     return T(self.x_, self.y_)

    def cross(self, rhs):
        """
        The `cross` function calculates the cross product of two vectors.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents another vector that we
        want to perform the cross product with
        :return: The cross product of the two vectors.

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = Vector2(5, 6)
            >>> v.cross(w)
            -2
        """
        return self.x_ * rhs.y_ - rhs.x_ * self.y_

    def __eq__(self, rhs) -> bool:
        """
        The `__eq__` function checks if two instances of the `Vector2` class are equal by comparing their
        `x_` and `y_` attributes.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the object that is being
        compared to the current object (`self`) in the `__eq__` method
        :return: The `__eq__` method returns a boolean value indicating whether the current object is equal
        to the `rhs` object.

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = Vector2(3, 4)
            >>> v == w
            True
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> w3d = Vector2(w, 6)  # vector in 3d
            >>> v3d == w3d
            False
        """
        return (self.x_, self.y_) == (rhs.x_, rhs.y_)

    def __neg__(self) -> Self:
        """
        The `__neg__` function returns a new instance of the same type with the negated x and y values.
        :return: The `__neg__` method returns a new instance of the same type as `self`, with the negated
        values of `self.x` and `self.y`.

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(-v)
            <-3, -4>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(-v3d)
            <<-3, -4>, -5>
        """
        T = type(self)
        return T(-self.x, -self.y)

    def __iadd__(self, rhs) -> Self:
        """
        The `__iadd__` method is used to implement the in-place addition operator for a Vector2 class.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the object that is being
        added to the current object. In this case, it is a `Vector2` object
        :return: The `__iadd__` method returns `self`, which is an instance of the class.

        Examples:
            >>> v = Vector2(3, 4)
            >>> v += Vector2(5, 6)
            >>> print(v)
            <8, 10>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> v3d += Vector2(v, 1)
            >>> print(v3d)
            <<16, 20>, 6>
        """
        self.x_ += rhs.x
        self.y_ += rhs.y
        return self

    def __add__(self, rhs) -> Self:
        """
        The `__add__` method overloads the `+` operator for the `Vector2` class, allowing two vectors to be
        added together.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the object that is being
        added to the current object. In this case, it is assumed that both `self` and `rhs` are instances of
        the `Vector2` class
        :return: The `__add__` method is returning a new instance of the same type as `self` with the x and
        y components added together.

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = Vector2(5, 6)
            >>> print(v + w)
            <8, 10>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> w3d = Vector2(w, 1)
            >>> print(v3d + w3d)
            <<8, 10>, 6>
        """
        T = type(self)
        return T(self.x + rhs.x, self.y + rhs.y)

    def __isub__(self, rhs) -> Self:
        """
        The `__isub__` method subtracts the x and y components of the right-hand side vector from the x and
        y components of the left-hand side vector and returns the modified left-hand side vector.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the vector that is being
        subtracted from the current vector
        :return: The method `__isub__` returns an instance of the class `Self`.

        Examples:
            >>> v = Vector2(3, 4)
            >>> v -= Vector2(5, 6)
            >>> print(v)
            <-2, -2>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> v3d -= Vector2(v, 1)
            >>> print(v3d)
            <<0, 0>, 4>
        """
        self.x_ -= rhs.x
        self.y_ -= rhs.y
        return self

    def __sub__(self, rhs) -> Self:
        """
        The `__sub__` method subtracts the coordinates of two vectors and returns a new vector with the
        result.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the vector that is being
        subtracted from the current vector
        :return: The `__sub__` method is returning a new instance of the same type (`T`) with the x and y
        components subtracted from the corresponding components of the `rhs` object.

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = Vector2(5, 6)
            >>> print(v - w)
            <-2, -2>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> w3d = Vector2(w, 1)
            >>> print(v3d - w3d)
            <<-2, -2>, 4>
        """
        T = type(self)
        return T(self.x - rhs.x, self.y - rhs.y)

    def __imul__(self, alpha) -> Self:
        """
        The `__imul__` method multiplies the x and y components of a Vector2 object by a scalar value and
        returns the modified object.

        :param alpha: The parameter `alpha` represents the scalar value by which the vector's components
        (`x_` and `y_`) will be multiplied
        :return: The method `__imul__` returns `self`, which is an instance of the class that the method
        belongs to.

        Examples:
            >>> v = Vector2(3, 4)
            >>> v *= 2
            >>> print(v)
            <6, 8>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> v3d *= 2
            >>> print(v3d)
            <<12, 16>, 10>
        """
        self.x_ *= alpha
        self.y_ *= alpha
        return self

    def __mul__(self, alpha) -> Self:
        """
        The `__mul__` method multiplies a vector by a scalar and returns a new vector.

        :param alpha: The parameter `alpha` represents a scalar value that will be multiplied with the `x`
        and `y` components of the vector
        :return: The method `__mul__` returns a new instance of the same type as `self` with the `x` and `y`
        attributes multiplied by `alpha`.

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(v * 2)
            <6, 8>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d * 2)
            <<6, 8>, 10>
        """
        T = type(self)
        return T(self.x * alpha, self.y * alpha)

    def __itruediv__(self, alpha) -> Self:
        """
        The `__itruediv__` method divides the x and y components of a Vector2 object by a given value and
        returns the modified object.

        :param alpha: The parameter `alpha` represents the value by which the `x_` and `y_` attributes of
        the object are divided
        :return: The method is returning the updated instance of the class `self` after performing the
        division operation.

        Examples:
            >>> v = Vector2(6.0, 9.0)
            >>> v /= 2.0
            >>> print(v)
            <3.0, 4.5>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> v3d /= 0.5
            >>> print(v3d)
            <<6.0, 9.0>, 10.0>
        """
        self.x_ /= alpha
        self.y_ /= alpha
        return self

    def __truediv__(self, alpha) -> Self:
        """
        The `__truediv__` method divides a vector by a scalar and returns a new vector with the resulting
        values.

        :param alpha: The parameter `alpha` represents the value by which the vector is divided
        :return: The `__truediv__` method returns a new instance of the same type (`T`) with the `x` and `y`
        attributes divided by `alpha`.

        Examples:
            >>> v = Vector2(6.0, 9.0)
            >>> print(v / 2.0)
            <3.0, 4.5>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d / 2.0)
            <<3.0, 4.5>, 2.5>
        """
        T = type(self)
        return T(self.x / alpha, self.y / alpha)


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    v = Vector2(6.0, 9.0)
    v /= 2.0
    print(v)
    v3d = Vector2(v, 5)  # vector in 3d
    v3d /= 0.5
    print(v3d)
