from typing import List

from .point import Point
from .polygon import Polygon
from .rpolygon import RPolygon
from .vector2 import Vector2

PointSet = List[Point[int, int]]


def to_polygon(rpolygon: RPolygon) -> Polygon[int]:
    """
    The `to_polygon` function converts a rectilinear polygon to a standard polygon.

    :return: A `Polygon` object representing the converted polygon.

    Examples:
        >>> from .point import Point
        >>> from .rpolygon import RPolygon
        >>> coords = [
        ...     (3, -3),
        ...     (5, 1),
        ...     (2, 2),
        ...     (3, 3),
        ...     (1, 4),
        ... ]
        >>> S = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
        >>> P = RPolygon.from_pointset(S)
        >>> polygon = to_polygon(P)
        >>> polygon.signed_area_x2
        10
    """
    new_vecs: List[Vector2[int, int]] = []
    current_pt: Vector2[int, int] = Vector2(0, 0)

    for next_pt in rpolygon._vecs:
        if current_pt.x != next_pt.x and current_pt.y != next_pt.y:
            # Add intermediate point for non-rectilinear segment
            new_vecs.append(Vector2(next_pt.x, current_pt.y))
        new_vecs.append(next_pt)
        current_pt = next_pt

    # Closing segment
    first_pt: Vector2[int, int] = Vector2(0, 0)
    if current_pt.x != first_pt.x and current_pt.y != first_pt.y:
        new_vecs.append(Vector2(first_pt.x, current_pt.y))

    return Polygon(rpolygon._origin, new_vecs)
