class vector2:
    __slots__ = ('_x', '_y')

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def copy(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return vector2(self._x, self._y)

    def __iadd__(self, rhs):
        self._x += rhs.x
        self._y += rhs.y
        return self

    def __add__(self, rhs):
        tmp = self.copy()
        return tmp.__iadd__(rhs)

    def __isub__(self, rhs):
        self._x -= rhs.x
        self._y -= rhs.y
        return self

    def __sub__(self, rhs):
        tmp = self.copy()
        return tmp.__isub__(rhs)

    def __imul__(self, alpha):
        self._x *= alpha
        self._y *= alpha
        return self

    def __mul__(self, alpha):
        tmp = self.copy()
        return tmp.__imul__(alpha)

    def __idiv__(self, alpha):
        self._x /= alpha
        self._y /= alpha
        return self

    def __div__(self, alpha):
        tmp = self.copy()
        return tmp.__idiv__(alpha)

    def __eq__(self, rhs) -> bool:
        return (self._x, self._y) == (rhs._x, rhs._y)

    def __ne__(self, rhs) -> bool:
        return not self.__eq__(rhs)

    # no less than comparison
