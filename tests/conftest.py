"""
Dummy conftest.py for physdes.

If you don't know what this is for, just leave it empty.
Read more about conftest.py under:
- https://docs.pytest.org/en/stable/fixture.html
- https://docs.pytest.org/en/stable/writing_plugins.html
"""

# import pytest

from lds_gen.ilds import Halton
from physdes.point import Point

def generate_random_points():
    """Generate a set of random source and terminal points."""
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [hgen.pop() for _ in range(7)]
    terminals = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    src_coord = hgen.pop()
    source = Point(src_coord[0], src_coord[1])
    return source, terminals

def generate_special_points():
    """Generate a special set of source and terminal points."""
    coords = [
        (-10, 0),
        (-9, -1),
        (-8, -2),
        (-7, -3),
        (-6, -4),
        (-5, -5),
        (-4, -6),
        (-3, -7),
        (-2, -8),
        (-1, -9),
        (0, -10),
    ]
    terminals = [Point(xcoord, ycoord) for xcoord, ycoord in coords]
    source = Point(0, 0)
    return source, terminals
