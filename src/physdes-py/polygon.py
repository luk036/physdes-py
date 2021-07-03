from itertools import filterfalse, tee

from .recti import vector2


class polygon:
    def __init__(self, coords):
        """[summary]

        Args:
            coords ([type]): [description]
        """
        self._origin = coords[0]
        self._vecs = list(c - coords[0] for c in coords[1:])

    def __iadd__(self, rhs: vector2):
        """[summary]

        Args:
            rhs (vector2): [description]

        Returns:
            [type]: [description]
        """
        self._origin += rhs
        return self

    def signed_area_x2(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        assert len(self._vecs) >= 2
        vecs = self._vecs
        res = vecs[0].x * vecs[1].y - vecs[-1].x * vecs[-2].y
        for v0, v1, v2 in zip(vecs[:-2], vecs[1:-1], vecs[2:]):
            res += v1.x * (v2.y - v0.y)
        return res

    def is_rectilinear(self):
        '''@todo '''
        pass


def partition(pred, iterable):
    'Use a predicate to partition entries into true entries and false entries'
    # partition(is_odd, range(10)) --> 1 9 3 7 5 and 4 0 8 2 6
    t1, t2 = tee(iterable)
    return filter(pred, t1), filterfalse(pred, t2)


# def create_xmono_polygon(lst):
#     """[summary]

#     Arguments:
#         lst {[type]} -- [description]

#     Returns:
#         [type] -- [description]
#     """
#     assert len(lst) >= 3

#     leftmost = min(lst)
#     rightmost = max(lst)
#     d = rightmost - leftmost
#     [lst1, lst2] = partition(lambda a: d.cross(a - leftmost) <= 0, lst)
#     lst1 = sorted(lst1)
#     lst2 = sorted(lst2, reverse=True)
#     return lst1 + lst2


def create_mono_polygon(lst, dir):
    """[summary]

    Args:
        lst ([type]): [description]

    Returns:
        [type]: [description]
    """
    assert len(lst) >= 3

    max_pt = max(lst, key=dir)
    min_pt = min(lst, key=dir)
    d = max_pt - min_pt
    [lst1, lst2] = partition(lambda a: d.cross(a - min_pt) <= 0, lst)
    lst1 = sorted(lst1, key=dir)
    lst2 = sorted(lst2, key=dir, reverse=True)
    return lst1 + lst2


def create_ymono_polygon(lst):
    return create_mono_polygon(lst, lambda a: (a.y, a.x))


def create_xmono_polygon(lst):
    return create_mono_polygon(lst, lambda a: (a.x, a.y))


def create_test_polygon(lst):
    """[summary]

    Args:
        lst ([type]): [description]

    Returns:
        [type]: [description]
    """
    upmost = max(lst, key=lambda a: (a.y, a.x))
    downmost = min(lst, key=lambda a: (a.y, a.x))
    d = upmost - downmost

    def right_left(a):
        return d.x * (a.y - downmost.y) < (a.x - downmost.x) * d.y

    [lst1, lst2] = partition(right_left, lst)
    lst1 = list(lst1)  # note!!!!
    lst2 = list(lst2)  # note!!!!
    upmost1 = max(lst1, key=lambda a: (a.x, a.y))
    [lst3, lst4] = partition(lambda a: a.y < upmost1.y, lst1)
    downmost2 = min(lst2, key=lambda a: (a.x, a.y))
    [lst5, lst6] = partition(lambda a: a.y > downmost2.y, lst2)

    if d.x < 0:
        lsta = sorted(lst6, key=lambda a: (a.x, a.y), reverse=True)
        lstb = sorted(lst5, key=lambda a: (a.y, a.x))
        lstc = sorted(lst4, key=lambda a: (a.x, a.y))
        lstd = sorted(lst3, key=lambda a: (a.y, a.x), reverse=True)
    else:
        lsta = sorted(lst3, key=lambda a: (a.x, a.y))
        lstb = sorted(lst4, key=lambda a: (a.y, a.x))
        lstc = sorted(lst5, key=lambda a: (a.x, a.y), reverse=True)
        lstd = sorted(lst6, key=lambda a: (a.y, a.x), reverse=True)
    return lsta + lstb + lstc + lstd


def point_in_polygon(S, q):
    """determine if a point is within a polygon

    The code below is from Wm. Randolph Franklin <wrf@ecse.rpi.edu>
    (see URL below) with some minor modifications for integer. It returns
    true for strictly interior points, false for strictly exterior, and ub
    for points on the boundary.  The boundary behavior is complex but
    determined; in particular, for a partition of a region into polygons,
    each point is "in" exactly one polygon.
    (See p.243 of [O'Rourke (C)] for a discussion of boundary behavior.)

    See http://www.faqs.org/faqs/graphics/algorithms-faq/ Subject 2.03

    Args:
        S ([type]): [description]
        q ([type]): [description]

    Returns:
        [type]: [description]
    """
    c = False
    p0 = S[-1]
    for p1 in S:
        if (p1.y <= q.y and q.y < p0.y) \
          or (p0.y <= q.y and q.y < p1.y):
            d = (q - p0).cross(p1 - p0)
            if p1.y > p0.y:
                if d < 0:
                    c = not c
            else:  # v1.y < v0.y
                if d > 0:
                    c = not c
        p0 = p1
    return c
