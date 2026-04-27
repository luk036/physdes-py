import pytest

from physdes.interval import Interval
from physdes.point import Point
from physdes.router.routing_tree import GlobalRoutingTree, NodeType
from physdes.router.routing_visualizer import (
    save_routing_tree_svg,
    visualize_routing_tree_svg,
    visualize_routing_tree3d_svg,
)


class TestRoutingVisualizer2D:
    """Test 2D routing tree visualization"""

    def test_source_only_tree(self) -> None:
        tree = GlobalRoutingTree(Point(0, 0))
        svg = visualize_routing_tree_svg(tree)
        assert "<circle" in svg
        assert "Source" in svg

    def test_same_x_coordinate(self) -> None:
        tree = GlobalRoutingTree(Point(0, 0))
        tree.insert_terminal_node(Point(0, 1))
        tree.insert_terminal_node(Point(0, 2))
        svg = visualize_routing_tree_svg(tree)
        assert "<circle" in svg

    def test_same_y_coordinate(self) -> None:
        tree = GlobalRoutingTree(Point(0, 0))
        tree.insert_terminal_node(Point(1, 0))
        tree.insert_terminal_node(Point(2, 0))
        svg = visualize_routing_tree_svg(tree)
        assert "<circle" in svg

    def test_visualize_with_keepouts(self) -> None:
        tree = GlobalRoutingTree(Point(0, 0))
        s1 = tree.insert_steiner_node(Point(1, 1))
        tree.insert_terminal_node(Point(2, 2), s1)
        keepouts = [Point(Interval(5, 10), Interval(5, 10))]
        svg = visualize_routing_tree_svg(tree, keepouts=keepouts)
        assert "<rect" in svg


class TestRoutingVisualizer3D:
    """Test 3D routing tree visualization"""

    def test_source_only_3d_tree(self) -> None:
        tree = GlobalRoutingTree(Point(Point(0, 0), 0))
        svg = visualize_routing_tree3d_svg(tree)
        assert "<circle" in svg
        assert "Source" in svg

    def test_3d_tree_same_x(self) -> None:
        tree = GlobalRoutingTree(Point(Point(0, 0), 0))
        tree.insert_terminal_node(Point(Point(0, 0), 1))
        tree.insert_terminal_node(Point(Point(0, 0), 2))
        svg = visualize_routing_tree3d_svg(tree)
        assert "<circle" in svg

    def test_3d_tree_same_y(self) -> None:
        tree = GlobalRoutingTree(Point(Point(0, 0), 0))
        tree.insert_terminal_node(Point(Point(1, 0), 0))
        tree.insert_terminal_node(Point(Point(2, 0), 0))
        svg = visualize_routing_tree3d_svg(tree)
        assert "<circle" in svg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])