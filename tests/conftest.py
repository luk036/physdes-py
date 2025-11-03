"""
Dummy conftest.py for physdes.

If you don't know what this is for, just leave it empty.
Read more about conftest.py under:
- https://docs.pytest.org/en/stable/fixture.html
- https://docs.pytest.org/en/stable/writing_plugins.html
"""

# import pytest

from random import randint

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


def generate_3d_random_points():
    """Generate a set of random 3D source and terminal points."""
    scale_z = 100
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [hgen.pop() for _ in range(7)]
    terminals = [
        Point(Point(xcoord, randint(0, 3) * scale_z), ycoord)
        for xcoord, ycoord in coords
    ]
    src_coord = hgen.pop()
    source = Point(Point(src_coord[0], randint(0, 3) * scale_z), src_coord[1])
    return source, terminals, scale_z


def generate_3d_random_points_with_index():
    """Generate a set of random 3D source and terminal points with index-based z-coordinate."""
    scale_z = 100
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(19)
    coords = [(hgen.pop(), i) for i in range(7)]
    terminals = [
        Point(Point(xcoord - 1000, (i % 4) * scale_z), ycoord - 1000)
        for ([xcoord, ycoord], i) in coords
    ]
    src_coord = hgen.pop()
    source = Point(Point(src_coord[0] - 1000, 0), src_coord[1] - 1000)
    return source, terminals, scale_z


def generate_2d_init_points():
    """Generate 2D points for global router initialization test."""
    source = Point(0, 0)
    terminals = [Point(10, 0), Point(1, 0), Point(5, 0)]
    return source, terminals


def generate_3d_init_points():
    """Generate 3D points for global router 3D initialization test."""
    source = Point(Point(0, 0), 0)
    terminals = [Point(Point(10, 0), 0), Point(Point(1, 0), 0), Point(Point(5, 0), 0)]
    return source, terminals


def generate_2d_simple_points():
    """Generate 2D points for simple routing test."""
    source = Point(0, 0)
    terminals = [Point(1, 1), Point(2, 2)]
    return source, terminals


def generate_3d_simple_points():
    """Generate 3D points for simple 3D routing test."""
    source = Point(Point(0, 0), 0)
    terminals = [Point(Point(1, 1), 1), Point(Point(2, 2), 2)]
    return source, terminals


def get_polygon_svg_elements(points, fill_color, stroke_color, opacity):
    polygon_points_str = []
    p0 = points[-1]
    for p1 in points:
        polygon_points_str.append(f"{p0.xcoord},{p0.ycoord}")
        p0 = p1
    polygon_svg = (
        f'  <polygon points="{" ".join(polygon_points_str)}"\n'
        f'  fill="{fill_color}" stroke="{stroke_color}" opacity="{opacity}"/>'
    )
    return polygon_svg


def get_circle_svg_elements(points, circle_radius=10, fill_color="black"):
    circle_svgs = []
    for p in points:
        circle_svgs.append(
            f'  <circle cx="{p.xcoord}" cy="{p.ycoord}" r="{circle_radius}" fill="{fill_color}" />'
        )
    return "\n".join(circle_svgs)
