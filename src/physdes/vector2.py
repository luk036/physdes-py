r"""
Vector2 Class

This code defines a Vector2 class, which represents a two-dimensional vector in mathematics or physics. A vector is an object that has both magnitude and direction, typically represented by x and y coordinates in a 2D space.

The purpose of this code is to provide a reusable structure for working with 2D vectors, along with various operations that can be performed on them. This class can be used in applications like game development, physics simulations, or any scenario where 2D vector calculations are needed.

The Vector2 class takes two inputs when creating a new instance: x and y coordinates. These can be integers, floats, or even other Vector2 objects, allowing for flexible use in different contexts.

The class produces Vector2 objects as outputs, which can be printed, compared, or used in further calculations. It also provides methods for common vector operations like addition, subtraction, multiplication by a scalar, and division by a scalar.

To achieve its purpose, the Vector2 class uses Python's object-oriented programming features. It defines several methods that overload standard operators (like +, -, *, and /), allowing vector objects to be manipulated intuitively. For example, you can add two vectors simply by using the + operator between them.

The class includes important logic flows for vector operations. Addition and subtraction are performed component-wise, meaning the x and y values are added or subtracted separately. Multiplication and division by a scalar apply the operation to both x and y components. There's also a cross product method, which calculates a special type of multiplication between two vectors.

The Vector2 class also implements comparison operations, allowing vectors to be checked for equality. It provides a string representation of the vector for easy printing and debugging.

An interesting feature of this class is its use of generic types, allowing it to work with different numeric types (like integers or floats) or even nested Vector2 objects. This makes the class very flexible and usable in a wide range of scenarios.

Overall, this Vector2 class provides a comprehensive toolkit for working with 2D vectors, encapsulating the mathematical concepts and operations into an easy-to-use Python class. It's designed to be intuitive for beginners while also offering advanced features for more complex use cases.
"""

from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from .interval import Interval

T1 = TypeVar("T1", int, float, "Interval[int]", "Interval[float]", "Vector2[Any, Any]")
T2 = TypeVar("T2", int, float, "Interval[int]", "Interval[float]", "Vector2[Any, Any]")


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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

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

    # def copy(self) -> "Vector2[T1, T2]":
    #     """
    #     The `copy` function returns a new instance of the same class with the same values as the original
    #     instance.
    #     :return: The `copy` method is returning a new instance of the same class (`"Vector2[T1, T2]"`) with the same `x_`
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

    def __neg__(self) -> "Vector2[T1, T2]":
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

    def __iadd__(self, rhs) -> "Vector2[T1, T2]":
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

    def __add__(self, rhs) -> "Vector2[T1, T2]":
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

    def __isub__(self, rhs) -> "Vector2[T1, T2]":
        """
        The `__isub__` method subtracts the x and y components of the right-hand side vector from the x and
        y components of the left-hand side vector and returns the modified left-hand side vector.

        :param rhs: The parameter `rhs` stands for "right-hand side" and represents the vector that is being
            subtracted from the current vector

        :return: The method `__isub__` returns an instance of the class `"Vector2[T1, T2]"`.

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

    def __sub__(self, rhs) -> "Vector2[T1, T2]":
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

    def __imul__(self, alpha) -> "Vector2[T1, T2]":
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

    def __mul__(self, alpha) -> "Vector2[T1, T2]":
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

    def __itruediv__(self, alpha) -> "Vector2[T1, T2]":
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

    def __truediv__(self, alpha) -> "Vector2[T1, T2]":
        """
        The `__truediv__` method divides a vector by a scalar and returns a new vector with the resulting values.

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
