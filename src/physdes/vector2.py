r"""
Vector2 Class

This code defines a Vector2 class, which represents a two-dimensional vector in mathematics
or physics. A vector is an object that has both magnitude and direction, typically
represented by x and y coordinates in a 2D space.

The purpose of this code is to provide a reusable structure for working with 2D vectors,
along with various operations that can be performed on them. This class can be used in
applications like game development, physics simulations, or any scenario where 2D vector
calculations are needed.

The Vector2 class takes two inputs when creating a new instance: x and y coordinates.
These can be integers, floats, or even other Vector2 objects, allowing for flexible use
in different contexts.

The class produces Vector2 objects as outputs, which can be printed, compared, or used in
further calculations. It also provides methods for common vector operations like addition,
subtraction, multiplication by a scalar, and division by a scalar.

To achieve its purpose, the Vector2 class uses Python's object-oriented programming
features. It defines several methods that overload standard operators (like +, -, \*, and
/), allowing vector objects to be manipulated intuitively. For example, you can add two
vectors simply by using the + operator between them.

The class includes important logic flows for vector operations. Addition and subtraction
are performed component-wise, meaning the x and y values are added or subtracted
separately. Multiplication and division by a scalar apply the operation to both x and y
components. There's also a cross product method, which calculates a special type of
multiplication between two vectors.

The Vector2 class also implements comparison operations, allowing vectors to be checked
for equality. It provides a string representation of the vector for easy printing and
debugging.

An interesting feature of this class is its use of generic types, allowing it to work with
different numeric types (like integers or floats) or even nested Vector2 objects. This
makes the class very flexible and usable in a wide range of scenarios.

Overall, this Vector2 class provides a comprehensive toolkit for working with 2D vectors,
encapsulating the mathematical concepts and operations into an easy-to-use Python class.
It\'s designed to be intuitive for beginners while also offering advanced features for more
complex use cases.
"""

from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    pass

T1 = TypeVar("T1", bound=Any)
T2 = TypeVar("T2", bound=Any)


class Vector2(Generic[T1, T2]):
    x_: T1  # Can be int, Interval, and Vector2
    y_: T2  # Can be int and Interval

    __slots__ = ("x_", "y_")

    def __init__(self, x: T1, y: T2) -> None:
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

    def __repr__(self) -> str:
        """
        The `__repr__` function returns a string representation of a `Vector2` object, including the class
        name and its coordinates, which is useful for debugging.

        :return: The `__repr__` method is returning a string representation of the `Vector2` object.

        Examples:
            >>> v = Vector2(3, 4)
            >>> repr(v)
            'Vector2(3, 4)'
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> repr(v3d)
            'Vector2(Vector2(3, 4), 5)'
        """
        return f"{self.__class__.__name__}({repr(self.x)}, {repr(self.y)})"

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

    def cross(self, rhs: "Vector2[T1, T2]") -> Any:
        """
        Calculates the 2D cross product of this vector with another vector.

        The 2D cross product is a scalar value that is positive if `rhs` is to the
        "left" of this vector, negative if to the "right", and zero if they are
        collinear.

        :param rhs: The other vector to compute the cross product with.
        :type rhs: Vector2[T1, T2]
        :return: The scalar value of the 2D cross product.

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = Vector2(5, 6)
            >>> v.cross(w)
            -2
            >>> v_parallel = Vector2(3, 4)
            >>> w_parallel = Vector2(6, 8)
            >>> v_parallel.cross(w_parallel)
            0
            >>> v_positive = Vector2(1, 0)
            >>> w_positive = Vector2(0, 1)
            >>> v_positive.cross(w_positive)
            1
        """
        return self.x_ * rhs.y_ - rhs.x_ * self.y_

    def __eq__(self, rhs: object) -> bool:
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
            >>> v_diff = Vector2(1, 2)
            >>> w_diff = Vector2(3, 4)
            >>> v_diff == w_diff
            False
        """
        if not isinstance(rhs, Vector2):
            return NotImplemented
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

    def __iadd__(self, rhs: "Vector2[T1, T2]") -> "Vector2[T1, T2]":
        """
        Performs in-place addition of another vector to this vector.

        This method adds the components of the `rhs` vector to the corresponding
        components of this vector, modifying the vector in place.

        :param rhs: The vector to add to this one.
        :type rhs: Vector2[T1, T2]
        :return: The modified vector (`self`).

        Examples:
            >>> v = Vector2(3, 4)
            >>> v += Vector2(5, 6)
            >>> print(v)
            <8, 10>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> v3d += Vector2(v, 1)
            >>> print(v3d)
            <<16, 20>, 6>
            >>> v_nested = Vector2(Vector2(1, 2), 3)
            >>> v_nested += Vector2(Vector2(4, 5), 6)
            >>> print(v_nested)
            <<5, 7>, 9>
        """
        self.x_ += rhs.x
        self.y_ += rhs.y
        return self

    def __add__(self, rhs: "Vector2[T1, T2]") -> "Vector2[T1, T2]":
        """
        Adds this vector to another vector, returning a new vector.

        This method adds the components of the `rhs` vector to the corresponding
        components of this vector and returns a new `Vector2` object with the result.

        :param rhs: The vector to add to this one.
        :type rhs: Vector2[T1, T2]
        :return: A new `Vector2` object representing the sum.

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = Vector2(5, 6)
            >>> print(v + w)
            <8, 10>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> w3d = Vector2(w, 1)
            >>> print(v3d + w3d)
            <<8, 10>, 6>
            >>> v_nested = Vector2(Vector2(1, 2), 3)
            >>> w_nested = Vector2(Vector2(4, 5), 6)
            >>> print(v_nested + w_nested)
            <<5, 7>, 9>
        """
        T = type(self)
        return T(self.x + rhs.x, self.y + rhs.y)

    def __isub__(self, rhs: "Vector2[T1, T2]") -> "Vector2[T1, T2]":
        """
        Performs in-place subtraction of another vector from this vector.

        This method subtracts the components of the `rhs` vector from the corresponding
        components of this vector, modifying the vector in place.

        :param rhs: The vector to subtract from this one.
        :type rhs: Vector2[T1, T2]
        :return: The modified vector (`self`).

        Examples:
            >>> v = Vector2(3, 4)
            >>> v -= Vector2(5, 6)
            >>> print(v)
            <-2, -2>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> v3d -= Vector2(v, 1)
            >>> print(v3d)
            <<0, 0>, 4>
            >>> v_nested = Vector2(Vector2(5, 7), 9)
            >>> v_nested -= Vector2(Vector2(4, 5), 6)
            >>> print(v_nested)
            <<1, 2>, 3>
        """
        self.x_ -= rhs.x
        self.y_ -= rhs.y
        return self

    def __sub__(self, rhs: "Vector2[T1, T2]") -> "Vector2[T1, T2]":
        """
        Subtracts another vector from this vector, returning a new vector.

        This method subtracts the components of the `rhs` vector from the corresponding
        components of this vector and returns a new `Vector2` object with the result.

        :param rhs: The vector to subtract from this one.
        :type rhs: Vector2[T1, T2]
        :return: A new `Vector2` object representing the difference.

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = Vector2(5, 6)
            >>> print(v - w)
            <-2, -2>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> w3d = Vector2(w, 1)
            >>> print(v3d - w3d)
            <<-2, -2>, 4>
            >>> v_nested = Vector2(Vector2(5, 7), 9)
            >>> w_nested = Vector2(Vector2(4, 5), 6)
            >>> print(v_nested - w_nested)
            <<1, 2>, 3>
        """
        T = type(self)
        return T(self.x - rhs.x, self.y - rhs.y)

    def __imul__(self, alpha: float) -> "Vector2[T1, T2]":
        """
        Performs in-place multiplication of this vector by a scalar.

        This method multiplies both components of this vector by the scalar `alpha`,
        modifying the vector in place.

        :param alpha: The scalar value to multiply the vector by.
        :type alpha: float
        :return: The modified vector (`self`).

        Examples:
            >>> v = Vector2(3, 4)
            >>> v *= 2
            >>> print(v)
            <6, 8>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> v3d *= 2
            >>> print(v3d)
            <<12, 16>, 10>
            >>> v_nested = Vector2(Vector2(1, 2), 3)
            >>> v_nested *= 2
            >>> print(v_nested)
            <<2, 4>, 6>
        """
        self.x_ *= alpha
        self.y_ *= alpha
        return self

    def __mul__(self, alpha: float) -> "Vector2[T1, T2]":
        """
        Multiplies this vector by a scalar, returning a new vector.

        This method multiplies both components of this vector by the scalar `alpha`
        and returns a new `Vector2` object with the result.

        :param alpha: The scalar value to multiply the vector by.
        :type alpha: float
        :return: A new `Vector2` object representing the product.

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(v * 2)
            <6, 8>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d * 2)
            <<6, 8>, 10>
            >>> v_nested = Vector2(Vector2(1, 2), 3)
            >>> print(v_nested * 2)
            <<2, 4>, 6>
        """
        T = type(self)
        return T(self.x * alpha, self.y * alpha)
    
    def __rmul__(self, alpha: float) -> "Vector2[T1, T2]":
        """
        Multiplies a scalar by this vector, returning a new vector.

        This method enables scalar * vector multiplication by delegating
        to the __mul__ method.

        :param alpha: The scalar value to multiply the vector by.
        :type alpha: float
        :return: A new `Vector2` object representing the product.

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(2 * v)
            <6, 8>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(2 * v3d)
            <<6, 8>, 10>
            >>> v_nested = Vector2(Vector2(1, 2), 3)
            >>> print(2 * v_nested)
            <<2, 4>, 6>
        """
        return self.__mul__(alpha)

    def __itruediv__(self, alpha: float) -> "Vector2[T1, T2]":
        """
        Performs in-place true division of this vector by a scalar.

        This method divides both components of this vector by the scalar `alpha`,
        modifying the vector in place.

        :param alpha: The scalar value to divide the vector by.
        :type alpha: float
        :return: The modified vector (`self`).

        Examples:
            >>> v = Vector2(6.0, 9.0)
            >>> v /= 2.0
            >>> print(v)
            <3.0, 4.5>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> v3d /= 0.5
            >>> print(v3d)
            <<6.0, 9.0>, 10.0>
            >>> v_nested = Vector2(Vector2(2.0, 4.0), 6.0)
            >>> v_nested /= 2.0
            >>> print(v_nested)
            <<1.0, 2.0>, 3.0>
        """
        self.x_ /= alpha
        self.y_ /= alpha
        return self

    def __truediv__(self, alpha: float) -> "Vector2[T1, T2]":
        """
        Divides this vector by a scalar, returning a new vector.

        This method divides both components of this vector by the scalar `alpha`
        and returns a new `Vector2` object with the result.

        :param alpha: The scalar value to divide the vector by.
        :type alpha: float
        :return: A new `Vector2` object representing the quotient.

        Examples:
            >>> v = Vector2(6.0, 9.0)
            >>> print(v / 2.0)
            <3.0, 4.5>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d / 2.0)
            <<3.0, 4.5>, 2.5>
            >>> v_nested = Vector2(Vector2(2.0, 4.0), 6.0)
            >>> print(v_nested / 2.0)
            <<1.0, 2.0>, 3.0>
            >>> print(v / -2.0)
            <-3.0, -4.5>
        """
        T = type(self)
        return T(self.x / alpha, self.y / alpha)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
