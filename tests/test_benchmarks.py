"""
Benchmarks for performance-critical ``physdes`` operations.

These benchmarks rely on the ``pytest-benchmark`` plugin.  Run them with::

    pytest tests/test_benchmarks.py --benchmark-only

A regular ``pytest`` invocation still executes each benchmark, but the
module-level ``benchmark`` marker caps the measurement window so the normal
test suite stays fast; the numbers only become meaningful when the benchmarks
are run with ``--benchmark-only`` (or ``--benchmark-enable``).
"""

from __future__ import annotations

from typing import List, Tuple

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from physdes.cts.dme_algorithm import DMEAlgorithm, LinearDelayCalculator, Sink
from physdes.point import Point
from physdes.polygon import Polygon
from physdes.router.routing_tree import GlobalRoutingTree
from physdes.rpolygon import RPolygon
from physdes.steiner_forest.steiner_forest_grid import steiner_forest_grid

# Keep each benchmark short so that a normal ``pytest`` run stays fast while
# still collecting a usable number of rounds.
pytestmark = pytest.mark.benchmark(max_time=0.02, min_rounds=5)

# ---------------------------------------------------------------------------
# Small, deterministic shared inputs (kept tiny so a normal pytest run is fast)
# ---------------------------------------------------------------------------

_STEINER_HEIGHT = 8
_STEINER_WIDTH = 8
_STEINER_PAIRS: List[Tuple[Tuple[int, int], Tuple[int, int]]] = [
    ((0, 0), (3, 2)),
    ((0, 0), (0, 5)),
    ((4, 4), (7, 5)),
    ((4, 4), (5, 7)),
    ((0, 1), (4, 1)),
]

_DME_SINKS: List[Sink] = [
    Sink(f"s{i}", Point(i * 10, i * 5), 1.0 + i * 0.1) for i in range(8)
]

_RPOLYGON_COORDS: List[Tuple[int, int]] = [
    (-2, 2),
    (0, -1),
    (-5, 1),
    (-2, 4),
    (0, -4),
    (-4, 3),
    (-6, -2),
    (5, 1),
    (2, 2),
    (3, -3),
    (-3, -4),
    (1, 4),
]

_POLYGON_COORDS: List[Tuple[int, int]] = [
    (-2, 2),
    (0, -1),
    (-5, 1),
    (-2, 4),
    (0, -4),
    (-4, 3),
    (-6, -2),
    (5, 1),
    (2, 2),
    (3, -3),
    (-3, -3),
    (3, 3),
    (-3, -4),
    (1, 4),
]


def test_bench_steiner_forest_grid(benchmark: BenchmarkFixture) -> None:
    """Benchmark the primal-dual Steiner forest on an 8x8 grid with 5 pairs."""
    benchmark(steiner_forest_grid, _STEINER_HEIGHT, _STEINER_WIDTH, _STEINER_PAIRS)


def test_bench_dme_build_clock_tree(benchmark: BenchmarkFixture) -> None:
    """Benchmark DME merging-tree construction plus top-down embedding."""
    calculator = LinearDelayCalculator(delay_per_unit=0.3, capacitance_per_unit=0.1)

    def build() -> None:
        DMEAlgorithm(_DME_SINKS, delay_calculator=calculator).build_clock_tree()

    benchmark(build)


def test_bench_routing_tree_find_insertion_point(benchmark: BenchmarkFixture) -> None:
    """Benchmark ``_find_insertion_point`` on a small routing tree."""
    tree = GlobalRoutingTree(Point(0, 0))
    steiner_1 = tree.insert_steiner_node(Point(10, 10))
    tree.insert_terminal_node(Point(11, 11), steiner_1)
    steiner_2 = tree.insert_steiner_node(Point(20, 20), steiner_1)
    tree.insert_terminal_node(Point(21, 21), steiner_2)

    benchmark(tree._find_insertion_point, Point(15, 5), 10**12)


def test_bench_rpolygon_signed_area(benchmark: BenchmarkFixture) -> None:
    """Benchmark ``RPolygon`` construction followed by its cached ``signed_area``."""
    points = [Point(xcoord, ycoord) for xcoord, ycoord in _RPOLYGON_COORDS]

    def signed_area() -> int:
        return RPolygon.from_pointset(points).signed_area

    benchmark(signed_area)


def test_bench_polygon_signed_area_x2(benchmark: BenchmarkFixture) -> None:
    """Benchmark ``Polygon`` construction followed by its cached ``signed_area_x2``."""
    points = [Point(xcoord, ycoord) for xcoord, ycoord in _POLYGON_COORDS]

    def signed_area_x2() -> int:
        return Polygon.from_pointset(points).signed_area_x2

    benchmark(signed_area_x2)
