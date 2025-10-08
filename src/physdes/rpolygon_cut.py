import math
from typing import Callable, List, Optional, Tuple
from mywheel.dllist import Dllink
from .point import Point
from .rdllist import RDllist

PointSet = List[Point[int, int]]


def find_min_dist_point(lst: PointSet, vcurr: Dllink[int]) -> Tuple[Dllink[int], bool]:
    vnext = vcurr.next
    vprev = vcurr.prev
    vi = vnext.next
    min_value = math.inf
    vertical = True
    v_min = vcurr
    pcurr = lst[vcurr.data]
    while id(vi) != id(vprev):
        p0 = lst[vi.prev.data]
        p1 = lst[vi.data]
        p2 = lst[vi.next.data]
        vec_i = p1.displace(pcurr)
        if (p0.ycoord <= pcurr.ycoord <= p1.ycoord) or (
            p1.ycoord <= pcurr.ycoord <= p0.ycoord
        ):
            if abs(vec_i.x_) < min_value:
                min_value = abs(vec_i.x_)
                v_min = vi
                vertical = True
        if (p2.xcoord <= pcurr.xcoord <= p1.xcoord) or (
            p1.xcoord <= pcurr.xcoord <= p2.xcoord
        ):
            if abs(vec_i.y_) < min_value:
                min_value = abs(vec_i.y_)
                v_min = vi
                vertical = False
        vi = vi.next
    return v_min, vertical


def rpolygon_cut_convex_recur(
    v1: Dllink[int], lst: PointSet, is_anticlockwise: bool, rdll: RDllist
) -> List[List[int]]:
    r"""
    .. svgbob::
       :align: center

                                            p0 (p_min, vertical = True)
                                       ┌────o
                ┌──────────o           │    │
                │          │      p2   │    │
           ┌────o          └──────o    │    │
           │                      │    │    │
           │                      └────o~~~~o p_new
           │                           p1   │
           o───────┐                        │
                   │                        │
                   o────┐                   │
                        +~~~o────┐          │
                        │   │    │          │
                        o───┘    │   o──────┘
                                 │   │
                                 o───┘
    """
    v2 = v1.next
    v3 = v2.next
    if id(v3) == id(v1):  # rectangle
        L = [v1.data, v2.data]
        return [L]
    if id(v3.next) == id(v1):  # monotone
        L = [v1.data, v2.data, v3.data]
        return [L]

    def _find_concave_point(
        vcurr: Dllink[int], cmp2: Callable
    ) -> Optional[Dllink[int]]:
        vstop = vcurr
        while True:
            vnext = vcurr.next
            vprev = vcurr.prev
            p0 = lst[vprev.data]
            p1 = lst[vcurr.data]
            p2 = lst[vnext.data]
            v1 = p1.displace(p0)
            v2 = p2.displace(p1)
            if v1.x_ * v2.x_ < 0 or v1.y_ * v2.y_ < 0:
                area_diff = (p1.ycoord - p0.ycoord) * (p2.xcoord - p1.xcoord)
                if cmp2(area_diff):
                    return vcurr
            vcurr = vnext
            if id(vcurr) == id(vstop):
                break
        return None  # convex

    vcurr = (
        _find_concave_point(v1, lambda a: a > 0)
        if is_anticlockwise
        else _find_concave_point(v1, lambda a: a < 0)
    )

    if vcurr is None:  # convex
        L = [v1.data] + [vi.data for vi in rdll.from_node(v1.data)]
        return [L]

    v_min, vertical = find_min_dist_point(lst, vcurr)
    n = len(lst)
    p_min = lst[v_min.data]
    p1 = lst[vcurr.data]
    rdll.cycle.append(Dllink(n))
    new_node = rdll[n]
    if vertical:
        new_node.next = vcurr.next
        new_node.prev = v_min.prev
        v_min.prev.next = new_node
        vcurr.next.prev = new_node
        vcurr.next = v_min
        v_min.prev = vcurr
        p_new = Point(p_min.xcoord, p1.ycoord)
    else:
        new_node.prev = vcurr.prev
        new_node.next = v_min.next
        v_min.next.prev = new_node
        vcurr.prev.next = new_node
        vcurr.prev = v_min
        v_min.next = vcurr
        p_new = Point(p1.xcoord, p_min.ycoord)
    lst.append(p_new)

    L1 = rpolygon_cut_convex_recur(vcurr, lst, is_anticlockwise, rdll)
    L2 = rpolygon_cut_convex_recur(new_node, lst, is_anticlockwise, rdll)
    return L1 + L2


def rpolygon_cut_convex(lst: PointSet, is_anticlockwise: bool) -> List[PointSet]:
    """
    Cuts a rectilinear polygon into a set of convex rectilinear polygons.

    Examples:
        >>> from .point import Point
        >>> lst = [Point(0, 0), Point(1, 2), Point(2, 1)]
        >>> hull = rpolygon_cut_convex(lst, False)
        >>> len(hull)
        1
    """
    rdll = RDllist(len(lst))
    L = rpolygon_cut_convex_recur(rdll[0], lst, is_anticlockwise, rdll)
    res = list()
    for item in L:
        P = [lst[i] for i in item]
        res.append(P)
    return res


def rpolygon_cut_explicit_recur(
    v1: Dllink[int], lst: PointSet, is_anticlockwise: bool, rdll: RDllist
) -> List[List[int]]:
    r"""
    .. svgbob::
       :align: center

                ┌──────────o
                │          │
           ┌────o~~~~~~~~~~└──────o
           │                      │
           │                      └─────────o
           │                                │
           o───────┐                        │
                   │                        │
                   o────┐                   │
                        o────────┐          │
                                 │          │
                                 +~~~o──────┘
                                 │   │
                                 o───┘
    """
    v2 = v1.next
    if id(v2.next) == id(v1):  # rectangle
        L = [v1.data, v2.data]
        return [L]

    def find_explicit_concave_point(
        vstart: Dllink[int], cmp2: Callable
    ) -> Optional[Dllink[int]]:
        vcurr = vstart
        while True:
            vnext = vcurr.next
            vprev = vcurr.prev
            p0 = lst[vprev.data]
            p1 = lst[vcurr.data]
            p2 = lst[vnext.data]
            area_diff = (p1.ycoord - p0.ycoord) * (p2.xcoord - p1.xcoord)
            if cmp2(area_diff):
                return vcurr
            vcurr = vnext
            if id(vcurr) == id(vstart):
                break
        return None  # convex

    vcurr = (
        find_explicit_concave_point(v1, lambda a: a > 0)
        if is_anticlockwise
        else find_explicit_concave_point(v1, lambda a: a < 0)
    )

    if vcurr is None:  # convex
        L = [v1.data] + [vi.data for vi in rdll.from_node(v1.data)]
        return [L]

    v_min, vertical = find_min_dist_point(lst, vcurr)
    n = len(lst)
    p_min = lst[v_min.data]
    p1 = lst[vcurr.data]
    rdll.cycle.append(Dllink(n))
    new_node = rdll[n]
    if vertical:
        new_node.next = vcurr.next
        new_node.prev = v_min.prev
        v_min.prev.next = new_node
        vcurr.next.prev = new_node
        vcurr.next = v_min
        v_min.prev = vcurr
        p_new = Point(p_min.xcoord, p1.ycoord)
    else:
        new_node.prev = vcurr.prev
        new_node.next = v_min.next
        v_min.next.prev = new_node
        vcurr.prev.next = new_node
        vcurr.prev = v_min
        v_min.next = vcurr
        p_new = Point(p1.xcoord, p_min.ycoord)
    lst.append(p_new)

    L1 = rpolygon_cut_explicit_recur(vcurr, lst, is_anticlockwise, rdll)
    L2 = rpolygon_cut_explicit_recur(new_node, lst, is_anticlockwise, rdll)
    return L1 + L2


def rpolygon_cut_explicit(lst: PointSet, is_anticlockwise: bool) -> List[PointSet]:
    """
    Cuts a rectilinear polygon into a set of convex rectilinear polygons.
    """
    rdll = RDllist(len(lst))
    L = rpolygon_cut_explicit_recur(rdll[0], lst, is_anticlockwise, rdll)
    res = list()
    for item in L:
        P = [lst[i] for i in item]
        res.append(P)
    return res
