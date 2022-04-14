class Vector2:
    __slots__ = ("_x", "_y")

    def __init__(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(v)
            <3, 4>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d)
            <<3, 4>, 5>
        """
        self._x = x
        self._y = y

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(v)
            <3, 4>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d)
            <<3, 4>, 5>
        """
        return "<{self.x}, {self.y}>".format(self=self)

    @property
    def x(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> v = Vector2(3, 4)
            >>> v.x
            3
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d.x)
            <3, 4>
        """
        return self._x

    @property
    def y(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> v = Vector2(3, 4)
            >>> v.y
            4
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d.y)
            5
        """
        return self._y

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = v.copy()
            >>> print(w)
            <3, 4>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> w3d = v3d.copy()
            >>> print(w3d)
            <<3, 4>, 5>
        """
        return Vector2(self._x, self._y)

    def cross(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> v = Vector2(3, 4)
            >>> w = Vector2(5, 6)
            >>> v.cross(w)
            -2
        """
        return self._x * rhs._y - rhs._x * self._y

    def __eq__(self, rhs) -> bool:
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            bool: [description]

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
        return (self._x, self._y) == (rhs._x, rhs._y)

    def __neg__(self):
        """[summary]

        Returns:
            [type]: [description]

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(-v)
            <-3, -4>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(-v3d)
            <<-3, -4>, -5>
        """
        return Vector2(-self.x, -self.y)

    def __iadd__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

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
        self._x += rhs.x
        self._y += rhs.y
        return self

    def __add__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

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
        return Vector2(self.x + rhs.x, self.y + rhs.y)

    def __isub__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

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
        self._x -= rhs.x
        self._y -= rhs.y
        return self

    def __sub__(self, rhs):
        """[summary]

        Args:
            rhs ([type]): [description]

        Returns:
            [type]: [description]

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
        return Vector2(self.x - rhs.x, self.y - rhs.y)

    def __imul__(self, alpha):
        """[summary]

        Args:
            alpha ([type]): [description]

        Returns:
            [type]: [description]

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
        self._x *= alpha
        self._y *= alpha
        return self

    def __mul__(self, alpha):
        """[summary]

        Args:
            alpha ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> v = Vector2(3, 4)
            >>> print(v * 2)
            <6, 8>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d * 2)
            <<6, 8>, 10>
        """
        return Vector2(self.x * alpha, self.y * alpha)

    def __itruediv__(self, alpha):
        """[summary]

        Args:
            alpha ([type]): [description]

        Returns:
            [type]: [description]

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
        self._x /= alpha
        self._y /= alpha
        return self

    def __truediv__(self, alpha):
        """[summary]

        Args:
            alpha ([type]): [description]

        Returns:
            [type]: [description]

        Examples:
            >>> v = Vector2(6.0, 9.0)
            >>> print(v / 2.0)
            <3.0, 4.5>
            >>> v3d = Vector2(v, 5)  # vector in 3d
            >>> print(v3d / 2.0)
            <<3.0, 4.5>, 2.5>
        """
        return Vector2(self.x / alpha, self.y / alpha)


if __name__ == "__main__":
    v = Vector2(3, 4)
    w = -v
    print(w >= v)

    v3d = Vector2(v, 5)  # vector in 3d
    w3d = Vector2(w, 5)  # vector in 3d
    print(w >= v)
