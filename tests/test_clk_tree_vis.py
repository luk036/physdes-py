import pytest
from unittest.mock import patch, mock_open
from physdes.clk_tree_vis import (
    ClockTreeVisualizer,
    create_interactive_svg,
    _add_analysis_info,
)
from physdes.dme_algorithm import Sink, TreeNode
from physdes.point import Point


@pytest.fixture
def sample_tree():
    """Create a sample clock tree for testing."""
    s1 = TreeNode(name="s1", position=Point(10, 20), capacitance=1.0)
    s2 = TreeNode(name="s2", position=Point(30, 40), capacitance=1.0)
    internal_node = TreeNode(name="n1", position=Point(20, 30), left=s1, right=s2)
    s1.parent = internal_node
    s2.parent = internal_node
    return internal_node


@pytest.fixture
def sample_sinks():
    """Create a sample list of sinks."""
    return [
        Sink("s1", Point(10, 20)),
        Sink("s2", Point(30, 40)),
    ]


def test_visualizer_init():
    """Test ClockTreeVisualizer initialization."""
    vis = ClockTreeVisualizer(margin=10, node_radius=5)
    assert vis.margin == 10
    assert vis.node_radius == 5


def test_collect_all_nodes(sample_tree):
    """Test the _collect_all_nodes method."""
    vis = ClockTreeVisualizer()
    nodes = vis._collect_all_nodes(sample_tree)
    assert len(nodes) == 3
    names = {node.name for node in nodes}
    assert names == {"s1", "s2", "n1"}


def test_calculate_bounds(sample_tree, sample_sinks):
    """Test the _calculate_bounds method."""
    vis = ClockTreeVisualizer()
    nodes = vis._collect_all_nodes(sample_tree)
    bounds = vis._calculate_bounds(nodes, sample_sinks)
    # These values depend on the padding logic, so we check ranges
    assert bounds[0] < 10
    assert bounds[1] < 20
    assert bounds[2] > 30
    assert bounds[3] > 40


@patch("builtins.open", new_callable=mock_open)
def test_visualize_tree(mock_file, sample_tree, sample_sinks):
    """Test the visualize_tree method."""
    vis = ClockTreeVisualizer()
    svg_content = vis.visualize_tree(sample_tree, sample_sinks, filename="test.svg")

    mock_file.assert_called_once_with("test.svg", "w")
    handle = mock_file()
    handle.write.assert_called_once_with(svg_content)

    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    # 3 nodes (2 sinks, 1 internal)
    assert svg_content.count("<circle") == 3
    # 2 wires from internal to sinks
    assert svg_content.count("<line") == 2


def test_add_analysis_info():
    """Test the _add_analysis_info function."""
    svg_content = '<svg>\n<g class="clock-tree">\n</g>\n</svg>'
    analysis = {
        "max_delay": 1.23,
        "min_delay": 1.20,
        "skew": 0.03,
        "total_wirelength": 120.5,
        "sink_delays": [1.23, 1.20],
    }
    enhanced_svg = _add_analysis_info(svg_content, analysis)
    assert "Clock Tree Analysis" in enhanced_svg
    assert "Max Delay: 1.230" in enhanced_svg
    assert "Skew: 0.030" in enhanced_svg


@patch("builtins.open", new_callable=mock_open)
def test_create_interactive_svg(mock_file, sample_tree, sample_sinks):
    """Test the create_interactive_svg function.
    This test characterizes the current behavior, which may not be correct.
    The file is opened twice.
    """
    analysis = {"skew": 0.03}
    svg_content = create_interactive_svg(
        sample_tree, sample_sinks, analysis, filename="interactive.svg"
    )

    assert mock_file.call_count == 2
    mock_file.assert_called_with("interactive.svg", "w")
    assert "Clock Tree Analysis" in svg_content
