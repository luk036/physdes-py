"""
physdes-py — VLSI physical design Python library.

Provides core geometric types (Point, Interval, Rectangle, RPolygon, Polygon,
Vector2, ManhattanArc) and algorithms for clock tree synthesis (DME), global
routing, Steiner forest construction, and polygon decomposition.
"""

import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.9`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "physdes-py"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
