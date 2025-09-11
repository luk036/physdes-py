import subprocess
import sys

from hypothesis import given
from hypothesis.strategies import integers

from physdes.vector2 import Vector2


@given(integers(), integers(), integers(), integers())
def test_Vector2_hypo(a, b, c, d):
    p = Vector2(a, b)
    q = Vector2(c, d)
    r = Vector2(-b, c)
    assert p + q == q + p
    assert p - q == -(q - p)
    assert (p + q) + r == p + (q + r)


def test_Vector2():
    # using boost::multiprecision::cpp_int
    # static_assert(Integral<cpp_int>
    a = 3
    b = 4
    c = 5
    d = 6

    p = Vector2(a, b)
    q = Vector2(c, d)

    assert Vector2(8, 10) == (p + q)
    assert Vector2(8, 2) != (p + q)
    assert Vector2(-2, -2) == (p - q)
    assert Vector2(6, 8) == (p * 2)
    # assert Vector2(4, 5) == (p + q) / 2
    assert p != q

    assert p + q == q + p
    assert p - q == -(q - p)
    # assert p * 3 == 3 * p
    # assert p + (q - p) / 2 == (p + q) / 2

    r = Vector2(-b, c)
    assert (p + q) + r == p + (q + r)


def test_arithmetic():
    """
    The function `test_arithmetic` tests various arithmetic operations on instances of the `Vector2`
    class.
    """
    a = Vector2(3, 5)
    b = Vector2(5, 7)
    assert a + b == Vector2(8, 12)
    assert a - b == Vector2(-2, -2)
    assert a * 2 == Vector2(6, 10)
    assert a / 2 == Vector2(1.5, 2.5)
    assert -a == Vector2(-3, -5)
    assert a.cross(b) == -4

    a += b
    assert a == Vector2(8, 12)
    a -= b
    assert a == Vector2(3, 5)
    a *= 2
    assert a == Vector2(6, 10)
    a /= 2
    assert a == Vector2(3, 5)


def test_repr():
    v = Vector2(3, 5)
    assert repr(v) == "Vector2(3, 5)"


def test_main_run_as_script():
    """CLI Tests"""
    result = subprocess.run(
        [sys.executable, "-m", "physdes.vector2"], capture_output=True, text=True
    )
    assert "<3.0, 4.5>" in result.stdout
    assert "<<6.0, 9.0>, 10.0>" in result.stdout
