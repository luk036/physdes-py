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

    def cross(self, rhs):
        return self._x * rhs._y - rhs._x * self._y

    def __str__(self):
        return '<{self.x}, {self.y}>'.format(self=self)


class point:
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
        return point(self._x, self._y)

    def __lt__(self, rhs) -> bool:
        return (self.x, self.y) < (rhs.x, rhs.y)

    def __gt__(self, rhs) -> bool:
        return (self.x, self.y) > (rhs.x, rhs.y)

    def __le__(self, rhs) -> bool:
        return (self.x, self.y) <= (rhs.x, rhs.y)

    def __ge__(self, rhs) -> bool:
        return (self.x, self.y) >= (rhs.x, rhs.y)

    def __eq__(self, rhs) -> bool:
        return (self.x, self.y) == (rhs.x, rhs.y)

    def __ne__(self, rhs) -> bool:
        return (self.x, self.y) != (rhs.x, rhs.y)

    def __iadd__(self, rhs: vector2):
        self._x += rhs.x
        self._y += rhs.y
        return self

    def __add__(self, rhs: vector2):
        tmp = self.copy()
        return tmp.__iadd__(rhs)

    def __isub__(self, rhs: vector2):
        self._x -= rhs.x
        self._y -= rhs.y
        return self

    def __sub__(self, rhs):
        if isinstance(rhs, vector2):
            tmp = self.copy()
            return tmp.__isub__(rhs)
        elif isinstance(rhs, point):
            return vector2(self.x - rhs.x, self.y - rhs.y)
        else:
            raise NotImplementedError()

    def flip(self):
        return point(self.y, self.x)

    def __str__(self):
        return '({self.x}, {self.y})'.format(self=self)


class dualpoint(point):
    def __init__(self, x, y):
        point.__init__(self, x, y)

    @property
    def x(self):
        return self._y

    @property
    def y(self):
        return self._x


class interval:
    __slots__ = ('_lower', '_upper')

    def __init__(self, lower, upper):
        self._lower = lower
        self._upper = upper

    @property
    def lower(self):
        return self._lower

    @property
    def upper(self):
        return self._upper

    def copy(self):
        return interval(self._lower, self._upper)

    def len(self):
        return self.upper - self.lower

    def __eq__(self, rhs) -> bool:
        return (self.lower, self.upper) == (rhs.lower, rhs.upper)

    def __lt__(self, rhs) -> bool:
        if isinstance(rhs, interval):
            return self.upper < rhs.lower
        return self.upper < rhs

    def __gt__(self, rhs) -> bool:
        if isinstance(rhs, interval):
            return self.lower > rhs.upper
        return self.lower > rhs

    def __le__(self, rhs) -> bool:
        if isinstance(rhs, interval):
            return not (rhs.upper < self.lower)
        return not (rhs < self.lower)

    def __ge__(self, rhs) -> bool:
        if isinstance(rhs, interval):
            return not (self.upper < rhs.lower)
        return not (self.upper < rhs)

    def contains(self, a) -> bool:
        # `a` can be an interval or int
        if isinstance(a, interval):
            return not (a.lower < self.lower or self.upper < a.upper)
        return not (a < self.lower or self.upper < a)

    def __str__(self):
        return '[{self.lower}, {self.upper}]'.format(self=self)


class rectangle(point):
    def __init__(self, x: interval, y: interval):
        point.__init__(self, x, y)

    @property
    def lower(self):
        return point(self.x.lower, self.y.lower)

    @property
    def upper(self):
        return point(self.x.upper, self.y.upper)

    def copy(self):
        return rectangle(self._x, self._y)

    # def __eq__(self, rhs) -> bool:
    #     return self.x == rhs.x and self.y == rhs.y

    def flip(self):
        return rectangle(self.y, self.x)

    def __str__(self):
        return '({self.x}, {self.y})'.format(self=self)

    # `a` can be point, vsegment, hsegment, or rectangle
    def contains(self, a) -> bool:
        return self.x.contains(a.x)\
            and self.y.contains(a.y)

    def area(self):
        return self.x.len() * self.y.len()


class vsegment(point):
    def __init__(self, x, y):
        point.__init__(self, x, y)

    def copy(self):
        return vsegment(self._x, self._y)

    # `a` can be point or vsegment
    def contains(self, a) -> bool:
        return self.x == a.x\
            and self.y.contains(a.y)

    def flip(self):
        return hsegment(self.y, self.x)


class hsegment(point):
    def __init__(self, x, y):
        point.__init__(self, x, y)

    def copy(self):
        return hsegment(self._x, self._y)

    # `a` can be point or hsegment
    def contains(self, a) -> bool:
        return self.y == a.y \
            and self.x.contains(a.x)

    def flip(self):
        return vsegment(self.y, self.x)


def test_recti(obj):
    print(obj)
    obj2 = obj.copy()
    assert obj2 == obj
    obj3 = obj2.flip().flip()
    assert obj3 == obj


if __name__ == '__main__':
    v = vector2(1, 2)
    p = point(3, 4)
    q = point(5, 6)
    intv1 = interval(2, 8)
    intv3 = interval(1, 10)
    R = rectangle(intv1, intv3)
    vseg = vsegment(4, intv1)
    hseg = hsegment(intv3, 11)

    print(v)
    print(q)
    print(intv1)
    print(intv3)

    v2 = v.copy()
    assert v2 == v

    intv2 = intv1.copy()
    assert intv2 == intv1
    assert intv2.contains(5)
    assert intv3.contains(intv2)

    test_recti(p)
    test_recti(vseg)
    test_recti(hseg)
    test_recti(R)

    assert R.contains(p)
    assert R.contains(vseg)
    assert not R.contains(hseg)
