"""
physdes-py — VLSI physical design Python library.

Provides core geometric types (Point, Interval, Rectangle, RPolygon, Polygon,
Vector2, ManhattanArc) and algorithms for clock tree synthesis (DME), global
routing, Steiner forest construction, and polygon decomposition.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    dist_name = "physdes-py"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
