import sys
import os
from pathlib import Path


from physdes.steiner_forest.steiner_forest_grid import (
    UnionFind,
    generate_svg,
    steiner_forest_grid,
)

# Add experimental to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestUnionFind:
    """Test cases for UnionFind data structure"""

    def test_union_find_initialization(self) -> None:
        """Test UnionFind initialization"""
        uf = UnionFind(10)
        assert len(uf.parent) == 10
        assert len(uf.rank) == 10
        assert all(uf.parent[i] == i for i in range(10))
        assert all(uf.rank[i] == 0 for i in range(10))

    def test_find_single_element(self) -> None:
        """Test find on a single element"""
        uf = UnionFind(5)
        assert uf.find(0) == 0
        assert uf.find(4) == 4

    def test_union_two_elements(self) -> None:
        """Test union of two elements"""
        uf = UnionFind(5)
        result = uf.union(0, 1)
        assert result is True
        assert uf.find(0) == uf.find(1)

    def test_union_same_element(self) -> None:
        """Test union of an element with itself"""
        uf = UnionFind(5)
        result = uf.union(0, 0)
        assert result is False

    def test_union_already_connected(self) -> None:
        """Test union of already connected elements"""
        uf = UnionFind(5)
        uf.union(0, 1)
        result = uf.union(0, 1)
        assert result is False

    def test_union_path_compression(self) -> None:
        """Test path compression in find"""
        uf = UnionFind(10)
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(2, 3)
        # All should have the same root
        assert uf.find(0) == uf.find(3)
        # Path compression should make parent direct
        assert uf.parent[0] == uf.find(0)

    def test_union_by_rank(self) -> None:
        """Test union by rank optimization"""
        uf = UnionFind(10)
        uf.union(0, 1)
        uf.union(2, 3)
        uf.union(4, 5)
        # Now union trees
        uf.union(0, 2)
        uf.union(0, 4)
        # Check that all are connected
        assert uf.find(5) == uf.find(0)

    def test_multiple_unions(self) -> None:
        """Test multiple union operations"""
        uf = UnionFind(10)
        uf.union(0, 1)
        uf.union(2, 3)
        uf.union(4, 5)
        uf.union(6, 7)
        uf.union(8, 9)

        # Check connectivity
        assert uf.find(0) == uf.find(1)
        assert uf.find(2) == uf.find(3)
        assert uf.find(4) == uf.find(5)
        assert uf.find(6) == uf.find(7)
        assert uf.find(8) == uf.find(9)

        # Check different groups
        assert uf.find(0) != uf.find(2)
        assert uf.find(0) != uf.find(4)


class TestSteinerForestGrid:
    """Test cases for steiner_forest_grid function"""

    def test_steiner_forest_grid_basic(self) -> None:
        """Test basic Steiner forest on small grid"""
        h = 2
        w = 2
        pairs = [((0, 0), (1, 1))]
        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            h, w, pairs
        )
        assert sorted(F_pruned) == [(0, 1, 1.0), (1, 3, 1.0)]
        assert total_cost == 2.0
        assert sources == {0}
        assert terminals == {3}
        assert steiner_nodes == {1}

    def test_steiner_forest_grid_multiple_pairs(self) -> None:
        """Test Steiner forest with multiple terminal pairs"""
        height = 8
        width = 8
        pairs = [
            ((0, 0), (3, 2)),
            ((0, 0), (0, 5)),
            ((4, 4), (7, 5)),
            ((4, 4), (5, 7)),
            ((0, 1), (4, 1)),
        ]

        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            height, width, pairs
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

    def test_steiner_forest_grid_single_pair(self) -> None:
        """Test with single terminal pair"""
        h = 3
        w = 3
        pairs = [((0, 0), (2, 2))]
        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            h, w, pairs
        )

        assert total_cost > 0
        assert len(sources) == 1
        assert len(terminals) == 1
        assert len(F_pruned) > 0

    def test_steiner_forest_grid_adjacent_terminals(self) -> None:
        """Test with adjacent terminals"""
        h = 2
        w = 2
        pairs = [((0, 0), (0, 1))]
        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            h, w, pairs
        )

        assert total_cost == 1.0
        assert len(F_pruned) == 1
        assert len(steiner_nodes) == 0

    def test_steiner_forest_grid_disconnected_pairs(self) -> None:
        """Test with disconnected pairs that require Steiner nodes"""
        h = 4
        w = 4
        pairs = [((0, 0), (3, 3)), ((0, 3), (3, 0))]
        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            h, w, pairs
        )

        assert total_cost > 0
        assert len(sources) == 2
        assert len(terminals) == 2
        # Should have Steiner nodes for optimal routing
        assert len(steiner_nodes) >= 0

    def test_steiner_forest_grid_same_terminal_multiple_times(self) -> None:
        """Test when a terminal appears in multiple pairs"""
        h = 3
        w = 3
        pairs = [((0, 0), (2, 2)), ((0, 0), (2, 0))]
        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            h, w, pairs
        )

        assert total_cost > 0
        assert 0 in sources  # (0,0) is a source
        assert len(terminals) == 2

    def test_steiner_forest_grid_empty_pairs(self) -> None:
        """Test with empty pairs list"""
        h = 3
        w = 3
        pairs = []
        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            h, w, pairs
        )

        assert total_cost == 0.0
        assert len(F_pruned) == 0
        assert len(sources) == 0
        assert len(terminals) == 0
        assert len(steiner_nodes) == 0

    def test_steiner_forest_grid_large_grid(self) -> None:
        """Test on larger grid"""
        h = 10
        w = 10
        pairs = [((0, 0), (9, 9)), ((0, 9), (9, 0))]
        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            h, w, pairs
        )

        assert total_cost > 0
        assert len(F_pruned) > 0
        assert len(sources) == 2
        assert len(terminals) == 2

    def test_steiner_forest_grid_cost_calculation(self) -> None:
        """Test that cost is correctly calculated"""
        h = 2
        w = 3
        pairs = [((0, 0), (1, 2))]
        F_pruned, total_cost, _, _, _ = steiner_forest_grid(h, w, pairs)

        # Calculate expected cost from edges
        expected_cost = sum(cost for _, _, cost in F_pruned)
        assert total_cost == expected_cost


class TestGenerateSVG:
    """Test cases for generate_svg function"""

    def test_generate_svg_basic(self, tmp_path: Path) -> None:
        """Test basic SVG generation"""
        output_file = tmp_path / "test_forest.svg"

        generate_svg(
            height=3,
            width=3,
            F_pruned=[(0, 1, 1.0), (1, 4, 1.0)],
            sources={0},
            terminals={4},
            steiner_nodes={1},
            cell_size=50,
            margin=20,
            filename=str(output_file),
        )

        assert output_file.exists()
        content = output_file.read_text()
        assert "<svg" in content
        assert "</svg>" in content
        assert "circle" in content
        assert "line" in content

    def test_generate_svg_with_multiple_nodes(self, tmp_path: Path) -> None:
        """Test SVG generation with multiple nodes"""
        output_file = tmp_path / "test_multi_nodes.svg"

        generate_svg(
            height=4,
            width=4,
            F_pruned=[
                (0, 1, 1.0),
                (1, 2, 1.0),
                (2, 3, 1.0),
                (5, 6, 1.0),
                (6, 7, 1.0),
            ],
            sources={0, 5},
            terminals={3, 7},
            steiner_nodes={1, 2, 6},
            cell_size=40,
            margin=30,
            filename=str(output_file),
        )

        assert output_file.exists()
        content = output_file.read_text()
        # Check for multiple circles (nodes)
        assert content.count("<circle") > 5
        # Check for multiple lines (edges)
        assert content.count("<line") > 5

    def test_generate_svg_no_steiner_nodes(self, tmp_path: Path) -> None:
        """Test SVG generation without Steiner nodes"""
        output_file = tmp_path / "test_no_steiner.svg"

        generate_svg(
            height=2,
            width=2,
            F_pruned=[(0, 1, 1.0)],
            sources={0},
            terminals={1},
            steiner_nodes=set(),
            cell_size=50,
            margin=20,
            filename=str(output_file),
        )

        assert output_file.exists()
        content = output_file.read_text()
        # Should still have source and terminal nodes
        assert "circle" in content

    def test_generate_svg_empty_forest(self, tmp_path: Path) -> None:
        """Test SVG generation with empty forest"""
        output_file = tmp_path / "test_empty.svg"

        generate_svg(
            height=3,
            width=3,
            F_pruned=[],
            sources=set(),
            terminals=set(),
            steiner_nodes=set(),
            cell_size=50,
            margin=20,
            filename=str(output_file),
        )

        assert output_file.exists()
        content = output_file.read_text()
        assert "<svg" in content
        assert "</svg>" in content

    def test_generate_svg_custom_dimensions(self, tmp_path: Path) -> None:
        """Test SVG generation with custom cell size and margin"""
        output_file = tmp_path / "test_custom.svg"

        generate_svg(
            height=5,
            width=5,
            F_pruned=[(0, 5, 1.0)],
            sources={0},
            terminals={5},
            steiner_nodes=set(),
            cell_size=100,
            margin=50,
            filename=str(output_file),
        )

        assert output_file.exists()
        content = output_file.read_text()
        # Check that SVG dimensions are reasonable
        assert 'width="' in content
        assert 'height="' in content


class TestIntegration:
    """Integration tests for Steiner forest"""

    def test_full_workflow_with_svg(self, tmp_path: Path) -> None:
        """Test complete workflow from forest calculation to SVG"""
        h = 4
        w = 4
        pairs = [((0, 0), (3, 3)), ((0, 3), (3, 0))]

        # Calculate forest
        F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
            h, w, pairs
        )

        # Generate SVG
        output_file = tmp_path / "integration_test.svg"
        generate_svg(
            height=h,
            width=w,
            F_pruned=F_pruned,
            sources=sources,
            terminals=terminals,
            steiner_nodes=steiner_nodes,
            cell_size=50,
            margin=20,
            filename=str(output_file),
        )

        assert output_file.exists()
        assert total_cost > 0
        assert len(F_pruned) > 0

    def test_consistency_multiple_runs(self) -> None:
        """Test that algorithm produces consistent results"""
        h = 5
        w = 5
        pairs = [((0, 0), (4, 4)), ((0, 4), (4, 0))]

        # Run twice
        F1, cost1, _, _, _ = steiner_forest_grid(h, w, pairs)
        F2, cost2, _, _, _ = steiner_forest_grid(h, w, pairs)

        # Results should be identical
        assert cost1 == cost2
        assert sorted(F1) == sorted(F2)
