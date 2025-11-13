import sys
import os

# Add experimental to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from physdes.steiner_forest.steiner_forest_grid import steiner_forest_grid


def test_steiner_forest_grid():
    h = 8
    w = 8
    pairs = [
        ((0, 0), (3, 2)),
        ((0, 0), (0, 5)),
        ((4, 4), (7, 5)),
        ((4, 4), (5, 7)),
        ((0, 1), (4, 1)),
    ]

    F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
        h, w, pairs
    )

    expected_cost = 17.0
    expected_F_pruned = [
        (0, 1, 1.0),
        (1, 2, 1.0),
        (4, 5, 1.0),
        (18, 26, 1.0),
        (25, 26, 1.0),
        (25, 33, 1.0),
        (36, 37, 1.0),
        (39, 47, 1.0),
        (53, 61, 1.0),
        (2, 3, 1.0),
        (2, 10, 1.0),
        (3, 4, 1.0),
        (10, 18, 1.0),
        (37, 38, 1.0),
        (37, 45, 1.0),
        (38, 39, 1.0),
        (45, 53, 1.0),
    ]
    expected_sources = {0, 1, 36}
    expected_terminals = {33, 5, 47, 26, 61}
    expected_steiner_nodes = {2, 3, 4, 37, 38, 39, 10, 45, 18, 53, 25}

    # Sort the edges for consistent comparison
    F_pruned_sorted = sorted([(min(u, v), max(u, v)) for u, v, _ in F_pruned])
    expected_F_pruned_sorted = sorted(
        [(min(u, v), max(u, v)) for u, v, _ in expected_F_pruned]
    )

    assert total_cost == expected_cost
    assert F_pruned_sorted == expected_F_pruned_sorted
    assert sources == expected_sources
    assert terminals == expected_terminals
    assert steiner_nodes == expected_steiner_nodes
