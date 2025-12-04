"""
Unit tests for Clock Tree Visualization module
"""

import sys
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET

import pytest

from physdes.cts.clk_tree_vis import (
    ClockTreeVisualizer,
    create_comparison_visualization,
    create_delay_model_comparison,
    create_interactive_svg,
)
from physdes.cts.dme_algorithm import (
    DMEAlgorithm,
    ElmoreDelayCalculator,
    LinearDelayCalculator,
    Sink,
    TreeNode,
)
from physdes.point import Point

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_tree() -> TreeNode:
    """Create a sample clock tree for testing"""
    s1 = TreeNode("s1", Point(10, 20), capacitance=1.0, delay=1.0)
    s2 = TreeNode("s2", Point(30, 40), capacitance=1.5, delay=1.2)
    _ = TreeNode("s3", Point(50, 10), capacitance=2.0, delay=0.8)
    root = TreeNode("root", Point(30, 25), left=s1, right=s2)
    s2.parent = root
    s1.parent = root

    # Add wire lengths for testing
    s1.wire_length = 15
    s2.wire_length = 20

    return root


@pytest.fixture
def sample_sinks() -> List[Sink]:
    """Create sample sinks for testing"""
    return [
        Sink("s1", Point(10, 20), 1.0),
        Sink("s2", Point(30, 40), 1.5),
        Sink("s3", Point(50, 10), 2.0),
    ]


@pytest.fixture
def sample_analysis() -> dict:
    """Create sample analysis results"""
    return {
        "max_delay": 1.5,
        "min_delay": 0.8,
        "skew": 0.7,
        "total_wirelength": 150,
        "sink_delays": [1.0, 1.2, 0.8],
        "delay_model": "LinearDelayCalculator",
    }


@pytest.fixture
def sample_tree_data(
    sample_tree: TreeNode, sample_sinks: List[Sink], sample_analysis: dict
) -> dict:
    """Create sample tree data for testing"""
    return {
        "tree": sample_tree,
        "sinks": sample_sinks,
        "analysis": sample_analysis,
        "title": "Test Tree",
    }


class TestClockTreeVisualizer:
    """Test cases for ClockTreeVisualizer class"""

    def test_visualizer_initialization(self) -> None:
        """Test ClockTreeVisualizer initialization"""
        visualizer = ClockTreeVisualizer(
            margin=30,
            node_radius=6,
            wire_width=2,
            sink_color="#00FF00",
            internal_color="#0000FF",
        )

        assert visualizer.margin == 30
        assert visualizer.node_radius == 6
        assert visualizer.wire_width == 2
        assert visualizer.sink_color == "#00FF00"
        assert visualizer.internal_color == "#0000FF"

    def test_visualize_tree_creation(
        self, sample_tree: TreeNode, sample_sinks: List[Sink], tmp_path: Path
    ) -> None:
        """Test basic tree visualization creation"""
        visualizer = ClockTreeVisualizer()
        output_file = tmp_path / "test_tree.svg"

        svg_content = visualizer.visualize_tree(
            sample_tree, sample_sinks, str(output_file), 400, 300
        )

        # Check that file was created
        assert output_file.exists()

        # Check that SVG content is returned
        assert isinstance(svg_content, str)
        assert "<svg" in svg_content
        assert "</svg>" in svg_content

        # Validate SVG structure
        self._validate_svg_structure(svg_content)

    def test_visualize_tree_with_analysis(
        self,
        sample_tree: TreeNode,
        sample_sinks: List[Sink],
        sample_analysis: dict,
        tmp_path: Path,
    ) -> None:
        """Test tree visualization with analysis information"""
        visualizer = ClockTreeVisualizer()
        output_file = tmp_path / "test_tree_with_analysis.svg"

        svg_content = visualizer.visualize_tree(
            sample_tree, sample_sinks, str(output_file), 500, 400, sample_analysis
        )

        # Check that analysis information is included
        assert "Clock Tree Analysis" in svg_content
        assert "LinearDelayCalculator" in svg_content
        assert "Max Delay: 1.500" in svg_content
        assert "Skew: 0.700" in svg_content

    def test_collect_all_nodes(self, sample_tree: TreeNode) -> None:
        """Test node collection from tree"""
        visualizer = ClockTreeVisualizer()
        nodes = visualizer._collect_all_nodes(sample_tree)

        assert len(nodes) == 3  # root, s1, s2
        node_names = [node.name for node in nodes]
        assert "root" in node_names
        assert "s1" in node_names
        assert "s2" in node_names

    def test_calculate_bounds(
        self, sample_tree: TreeNode, sample_sinks: List[Sink]
    ) -> None:
        """Test bounding box calculation"""
        visualizer = ClockTreeVisualizer()
        nodes = visualizer._collect_all_nodes(sample_tree)
        min_x, min_y, max_x, max_y = visualizer._calculate_bounds(nodes, sample_sinks)

        # Check that bounds include all points with padding
        assert min_x <= 10  # s1 x
        assert min_y <= 10  # s3 y
        assert max_x >= 50  # s3 x
        assert max_y >= 40  # s2 y

    def test_draw_wires(self, sample_tree: TreeNode) -> None:
        """Test wire drawing functionality"""
        visualizer = ClockTreeVisualizer()

        def scale_coord(x, y):
            return x, y  # Identity scaling for testing

        svg_elements = visualizer._draw_wires(sample_tree, scale_coord)

        # Should have wires from root to s1 and root to s2
        assert len(svg_elements) >= 2
        wire_elements = [elem for elem in svg_elements if "line" in elem]
        assert len(wire_elements) == 2

    def test_draw_nodes(self, sample_tree: TreeNode, sample_sinks: List[Sink]) -> None:
        """Test node drawing functionality"""
        visualizer = ClockTreeVisualizer()

        def scale_coord(x, y):
            return x, y  # Identity scaling for testing

        svg_elements = visualizer._draw_nodes(sample_tree, sample_sinks, scale_coord)

        # Should have nodes for root, s1, s2
        circle_elements = [elem for elem in svg_elements if "circle" in elem]
        text_elements = [
            elem
            for elem in svg_elements
            if "text" in elem and 'class="node-label"' in elem
        ]

        assert len(circle_elements) == 3
        assert len(text_elements) == 3

        # Check that node names are included
        svg_text = " ".join(svg_elements)
        assert "root" in svg_text
        assert "s1" in svg_text
        assert "s2" in svg_text

    def test_create_analysis_box(self) -> None:
        """Test analysis box creation"""
        visualizer = ClockTreeVisualizer()
        analysis = {
            "delay_model": "TestModel",
            "max_delay": 2.0,
            "min_delay": 1.0,
            "skew": 1.0,
            "total_wirelength": 200,
            "sink_delays": [1.0, 1.5, 2.0],
        }

        analysis_elements = visualizer._create_analysis_box(analysis, 500)

        assert len(analysis_elements) > 0
        analysis_text = " ".join(analysis_elements)
        assert "Clock Tree Analysis" in analysis_text
        assert "TestModel" in analysis_text
        assert "Max Delay: 2.000" in analysis_text

    def _validate_svg_structure(self, svg_content: str) -> None:
        """Helper method to validate SVG structure"""
        try:
            # Basic XML validation
            ET.fromstring(svg_content)
        except ET.ParseError as e:
            pytest.fail(f"Invalid SVG XML: {e}")

        # Check for essential SVG elements
        assert 'xmlns="http://www.w3.org/2000/svg"' in svg_content
        assert "<svg" in svg_content
        assert "</svg>" in svg_content


class TestInteractiveVisualization:
    """Test cases for interactive visualization functions"""

    def test_create_interactive_svg(
        self,
        sample_tree: TreeNode,
        sample_sinks: List[Sink],
        sample_analysis: dict,
        tmp_path: Path,
    ) -> None:
        """Test interactive SVG creation"""
        output_file = tmp_path / "interactive_tree.svg"

        svg_content = create_interactive_svg(
            sample_tree, sample_sinks, sample_analysis, str(output_file)
        )

        assert output_file.exists()
        assert "<svg" in svg_content
        assert "Clock Tree Analysis" in svg_content

    def test_create_comparison_visualization(
        self, sample_tree_data: dict, tmp_path: Path
    ) -> None:
        """Test comparison visualization with multiple trees"""
        output_file = tmp_path / "comparison.svg"

        # Create multiple tree data sets
        tree_data_sets = [
            sample_tree_data,
            sample_tree_data,
        ]  # Using same data twice for testing

        svg_content = create_comparison_visualization(
            tree_data_sets, str(output_file), 800, 600
        )

        assert output_file.exists()
        assert "<svg" in svg_content
        assert "Test Tree" in svg_content  # Should appear twice

    def test_create_comparison_visualization_single_tree(
        self, sample_tree_data: dict, tmp_path: Path
    ) -> None:
        """Test comparison visualization with single tree"""
        output_file = tmp_path / "single_comparison.svg"

        svg_content = create_comparison_visualization(
            [sample_tree_data], str(output_file), 600, 400
        )

        assert output_file.exists()
        assert "Test Tree" in svg_content

    def test_create_comparison_visualization_empty_data(self) -> None:
        """Test comparison visualization with empty data"""
        with pytest.raises(ValueError, match="No tree data provided"):
            create_comparison_visualization([])

    def test_create_delay_model_comparison(
        self, sample_tree_data: dict, tmp_path: Path
    ) -> None:
        """Test delay model comparison visualization"""
        output_file = tmp_path / "delay_model_comparison.svg"

        # Use same data for both models for testing
        linear_data = sample_tree_data.copy()
        elmore_data = sample_tree_data.copy()
        elmore_data["analysis"] = elmore_data["analysis"].copy()
        elmore_data["analysis"]["delay_model"] = "ElmoreDelayCalculator"

        svg_content = create_delay_model_comparison(
            linear_data, elmore_data, str(output_file)
        )

        assert output_file.exists()
        assert "<svg" in svg_content
        assert "Linear Delay Model" in svg_content
        assert "Elmore Delay Model" in svg_content


class TestIntegration:
    """Integration tests with actual DME algorithm"""

    def test_end_to_end_visualization(self, tmp_path: Path) -> None:
        """Test complete workflow from DME algorithm to visualization"""
        # Create sinks
        sinks = [
            Sink("s1", Point(0, 0), 1.0),
            Sink("s2", Point(20, 0), 1.0),
            Sink("s3", Point(0, 20), 1.0),
        ]

        # Build clock tree
        calculator = LinearDelayCalculator(delay_per_unit=0.5)
        dme = DMEAlgorithm(sinks, delay_calculator=calculator)
        clock_tree = dme.build_clock_tree()
        analysis = dme.analyze_skew(clock_tree)

        # Create visualization
        visualizer = ClockTreeVisualizer()
        output_file = tmp_path / "integration_test.svg"

        svg_content = visualizer.visualize_tree(
            clock_tree, sinks, str(output_file), analysis=analysis
        )

        # Verify results
        assert output_file.exists()
        assert "<svg" in svg_content
        assert "Clock Tree Analysis" in svg_content
        assert "LinearDelayCalculator" in svg_content

        # Verify tree structure is represented
        assert "s1" in svg_content
        assert "s2" in svg_content
        assert "s3" in svg_content

    def test_multiple_delay_models_comparison(self, tmp_path: Path) -> None:
        """Test comparison visualization with trees from different delay models"""
        sinks = [
            Sink("s1", Point(0, 0), 1.0),
            Sink("s2", Point(30, 0), 2.0),
            Sink("s3", Point(0, 30), 1.5),
        ]

        # Linear model tree
        linear_calc = LinearDelayCalculator(delay_per_unit=0.3)
        dme_linear = DMEAlgorithm(sinks, delay_calculator=linear_calc)
        tree_linear = dme_linear.build_clock_tree()
        analysis_linear = dme_linear.analyze_skew(tree_linear)

        # Elmore model tree
        elmore_calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
        dme_elmore = DMEAlgorithm(sinks, delay_calculator=elmore_calc)
        tree_elmore = dme_elmore.build_clock_tree()
        analysis_elmore = dme_elmore.analyze_skew(tree_elmore)

        # Create comparison
        linear_data = {
            "tree": tree_linear,
            "sinks": sinks,
            "analysis": analysis_linear,
            "title": "Linear Model",
        }
        elmore_data = {
            "tree": tree_elmore,
            "sinks": sinks,
            "analysis": analysis_elmore,
            "title": "Elmore Model",
        }

        output_file = tmp_path / "model_comparison.svg"
        svg_content = create_delay_model_comparison(
            linear_data, elmore_data, str(output_file)
        )

        assert output_file.exists()
        assert "Linear Delay Model" in svg_content
        assert "Elmore Delay Model" in svg_content


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_visualize_empty_tree(
        self, sample_sinks: List[Sink], tmp_path: Path
    ) -> None:
        """Test visualization with minimal tree"""
        # Single node tree
        single_node = TreeNode("s1", Point(10, 20))

        visualizer = ClockTreeVisualizer()
        output_file = tmp_path / "empty_tree.svg"

        svg_content = visualizer.visualize_tree(
            single_node, sample_sinks, str(output_file), 200, 200
        )

        assert output_file.exists()
        assert "s1" in svg_content

    def test_visualize_tree_no_sinks(
        self, sample_tree: TreeNode, tmp_path: Path
    ) -> None:
        """Test visualization with empty sinks list"""
        visualizer = ClockTreeVisualizer()
        output_file = tmp_path / "no_sinks.svg"

        visualizer.visualize_tree(sample_tree, [], str(output_file), 300, 300)

        assert output_file.exists()
        # Should still create valid SVG even with no original sinks

    def test_visualize_tree_none_analysis(
        self, sample_tree: TreeNode, sample_sinks: List[Sink], tmp_path: Path
    ) -> None:
        """Test visualization with None analysis"""
        visualizer = ClockTreeVisualizer()
        output_file = tmp_path / "none_analysis.svg"

        visualizer.visualize_tree(
            sample_tree, sample_sinks, str(output_file), analysis=None
        )

        assert output_file.exists()
        # Should create SVG without analysis box


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
