"""
Rectilinear Polygon Cutting Algorithms.

This module provides a set of functions for partitioning rectilinear polygons into convex
components. This is a common operation in computational geometry and is used in various
applications, such as VLSI physical design, computer graphics, and robotics.

The core functionality of this module is to take a rectilinear polygon, which may be
concave, and decompose it into a set of smaller, convex rectilinear polygons. This is
achieved by identifying concave vertices and introducing cuts to resolve the concavities.

The main functions provided are:
- `rpolygon_cut_convex()`: A recursive algorithm that cuts a rectilinear polygon into
  convex pieces.
- `rpolygon_cut_explicit()`: An alternative cutting algorithm that also produces convex
  partitions.

These functions are essential for simplifying complex polygon geometries, making them
easier to process in downstream applications. The algorithms are designed to be robust
and efficient, handling various polygon shapes and complexities.
"""

import math
from typing import Callable, List, Optional, Tuple

from mywheel.dllist import Dllink  # type: ignore

from .point import Point
from .rdllist import RDllist

PointSet = List[Point[int, int]]


def find_min_dist_point(lst: PointSet, vcurr: Dllink[int]) -> Tuple[Dllink[int], bool]:
    """
    Finds the point in a polygon that is closest to a given vertex.

    This function is a key helper for the polygon cutting algorithms. When a concave
    vertex is identified, this function is used to find the best vertex to connect it
    to, in order to create a cut that resolves the concavity. The "best" vertex is
    the one that is closest in either the horizontal or vertical direction.

    The function iterates through the vertices of the polygon and calculates the
    Manhattan distance to the given vertex (`vcurr`). It keeps track of the minimum
    distance found and returns the vertex that corresponds to this minimum distance,
    along with a flag indicating whether the closest connection is vertical or horizontal.

    Args:
        lst: A list of points representing the vertices of the polygon.
        vcurr: The vertex from which to measure the distance.

    Returns:
        A tuple containing the closest vertex and a boolean indicating whether the
        connection is vertical (True) or horizontal (False).
    """
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
        vcurr: Dllink[int], cmp2: Callable[[int], bool]
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

    This function implements a recursive algorithm to partition a given rectilinear
    polygon into a set of convex components. The process begins by identifying a
    concave vertex in the polygon. Once a concave vertex is found, a cut is made to
    another vertex in the polygon, effectively splitting the polygon into two smaller
    polygons. This process is then applied recursively to the resulting polygons until
    all of them are convex.

    The choice of the cut is critical for the efficiency and quality of the partitioning.
    This implementation uses the `find_min_dist_point` function to select a cut that
    connects the concave vertex to the nearest vertex in the polygon, which helps to
    create well-shaped partitions.

    Args:
        lst: A list of points representing the vertices of the polygon.
        is_anticlockwise: A boolean indicating the orientation of the polygon.

    Returns:
        A list of point sets, where each point set represents a convex rectilinear polygon.

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
        vstart: Dllink[int], cmp2: Callable[[int], bool]
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

    This function provides an alternative algorithm for partitioning a rectilinear polygon
    into convex components. Like `rpolygon_cut_convex`, it works by identifying concave
    vertices and introducing cuts to resolve them. The underlying logic for selecting
    cuts and performing the partitioning may differ, but the end result is the same: a
    set of convex rectilinear polygons.

    This function can be used as a drop-in replacement for `rpolygon_cut_convex`.
    Depending on the specific geometry of the input polygon, one function may perform
    better than the other. Having both options provides flexibility for different use
    cases.

    Args:
        lst: A list of points representing the vertices of the polygon.
        is_anticlockwise: A boolean indicating the orientation of the polygon.

    Returns:
        A list of point sets, where each point set represents a convex rectilinear polygon.
    """
    rdll = RDllist(len(lst))
    L = rpolygon_cut_explicit_recur(rdll[0], lst, is_anticlockwise, rdll)
    res = list()
    for item in L:
        P = [lst[i] for i in item]
        res.append(P)
    return res
