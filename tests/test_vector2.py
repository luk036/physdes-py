from physdes.recti import vector2


def test_vector2():
    # using boost::multiprecision::cpp_int
    # static_assert(Integral<cpp_int>
    a = 3
    b = 4
    c = 5
    d = 6
    # f = -30
    # g = 4
    # z = 0
    # h = -g

    p = vector2(a, b)
    q = vector2(c, d)

    assert vector2(8, 10) == (p + q)
    assert vector2(-2, -2) == (p - q)
    assert vector2(6, 8) == (p * 2)
    # assert vector2(4, 5) == (p + q) / 2
    assert p != q
