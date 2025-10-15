import pytest
from physdes.router.routing_tree3d import RoutingNode3d, GlobalRoutingTree3d, NodeType
from physdes.point import Point


# Tests for RoutingNode3d
class TestRoutingNode3d:
    def test_init(self):
        node = RoutingNode3d("n1", NodeType.TERMINAL, Point(Point(10, 20), 20))
        assert node.id == "n1"
        assert node.type == NodeType.TERMINAL
        assert node.pt == Point(Point(10, 20), 20)
        assert node.children == []
        assert node.parent is None
        assert node.capacitance == 0.0
        assert node.delay == 0.0

    def test_add_child(self):
        parent = RoutingNode3d("p1", NodeType.STEINER)
        child = RoutingNode3d("c1", NodeType.TERMINAL)
        parent.add_child(child)
        assert len(parent.children) == 1
        assert parent.children[0] == child
        assert child.parent == parent

    def test_remove_child(self):
        parent = RoutingNode3d("p1", NodeType.STEINER)
        child = RoutingNode3d("c1", NodeType.TERMINAL)
        parent.add_child(child)
        parent.remove_child(child)
        assert len(parent.children) == 0
        assert child.parent is None

    def test_remove_non_existent_child(self):
        parent = RoutingNode3d("p1", NodeType.STEINER)
        child = RoutingNode3d("c1", NodeType.TERMINAL)
        non_child = RoutingNode3d("nc1", NodeType.TERMINAL)
        parent.add_child(child)
        parent.remove_child(non_child)
        assert len(parent.children) == 1  # Should not remove anything
        assert child.parent == parent

    def test_get_position(self):
        node = RoutingNode3d("n1", NodeType.TERMINAL, Point(Point(10, 20), 20))
        assert node.get_position() == Point(Point(10, 20), 20)

    def test_manhattan_distance(self):
        node1 = RoutingNode3d("n1", NodeType.TERMINAL, Point(Point(0, 0), 0))
        node2 = RoutingNode3d("n2", NodeType.TERMINAL, Point(Point(3, 4), 4))
        assert node1.manhattan_distance(node2) == 11
        assert node2.manhattan_distance(node1) == 11
        node3 = RoutingNode3d("n3", NodeType.TERMINAL, Point(Point(-1, -1), -1))
        assert node1.manhattan_distance(node3) == 3

    def test_str(self):
        node = RoutingNode3d("n1", NodeType.TERMINAL, Point(Point(10, 20), 20))
        assert str(node) == "TerminalNode(n1, ((10, 20), 20))"
        node2 = RoutingNode3d("s1", NodeType.STEINER, Point(Point(5, 5), 5))
        assert str(node2) == "SteinerNode(s1, ((5, 5), 5))"
        node3 = RoutingNode3d("src", NodeType.SOURCE, Point(Point(0, 0), 0))
        assert str(node3) == "SourceNode(src, ((0, 0), 0))"


# Tests for GlobalRoutingTree3d
class TestGlobalRoutingTree3d:
    def test_init(self):
        tree3d = GlobalRoutingTree3d()
        assert tree3d.source.id == "source"
        assert tree3d.source.type == NodeType.SOURCE
        assert tree3d.source.pt == Point(Point(0, 0), 0)
        assert tree3d.nodes["source"] == tree3d.source
        assert tree3d.next_steiner_id == 1
        assert tree3d.next_terminal_id == 1

        tree3d_at_pos = GlobalRoutingTree3d(Point(Point(10, 10), 10))
        assert tree3d_at_pos.source.pt == Point(Point(10, 10), 10)

    def test_insert_steiner_node_to_source(self):
        tree3d = GlobalRoutingTree3d()
        steiner_id = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
        assert steiner_id == "steiner_1"
        assert tree3d.nodes[steiner_id].pt == Point(Point(1, 1), 1)
        assert tree3d.nodes[steiner_id].type == NodeType.STEINER
        assert tree3d.nodes[steiner_id].parent == tree3d.source
        assert tree3d.source.children[0] == tree3d.nodes[steiner_id]
        assert tree3d.next_steiner_id == 2

    def test_insert_steiner_node_to_parent(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
        s2_id = tree3d.insert_steiner_node(Point(Point(2, 2), 2), s1_id)
        assert s2_id == "steiner_2"
        assert tree3d.nodes[s2_id].parent == tree3d.nodes[s1_id]
        assert tree3d.nodes[s1_id].children[0] == tree3d.nodes[s2_id]

    def test_insert_steiner_node_invalid_parent(self):
        tree3d = GlobalRoutingTree3d()
        with pytest.raises(ValueError, match="Parent node non_existent not found"):
            tree3d.insert_steiner_node(Point(Point(1, 1), 1), "non_existent")

    def test_insert_terminal_node_nearest(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(10, 10), 10))
        t1_id = tree3d.insert_terminal_node(
            Point(Point(11, 11), 11)
        )  # Should connect to s1_id
        assert t1_id == "terminal_1"
        assert tree3d.nodes[t1_id].parent.id == tree3d.nodes[s1_id].id
        assert tree3d.nodes[s1_id].children[0] == tree3d.nodes[t1_id]

    def test_insert_terminal_node_to_parent(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
        t1_id = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1_id)
        assert t1_id == "terminal_1"
        assert tree3d.nodes[t1_id].parent == tree3d.nodes[s1_id]
        assert tree3d.nodes[s1_id].children[0] == tree3d.nodes[t1_id]

    def test_insert_terminal_node_invalid_parent(self):
        tree3d = GlobalRoutingTree3d()
        with pytest.raises(ValueError, match="Parent node non_existent not found"):
            tree3d.insert_terminal_node(Point(Point(1, 1), 1), "non_existent")

    def test_insert_node_on_branch(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(0, 0), 0))
        s2_id = tree3d.insert_steiner_node(Point(Point(2, 2), 2), s1_id)
        new_s_id = tree3d.insert_node_on_branch(
            NodeType.STEINER, Point(Point(1, 1), 1), s1_id, s2_id
        )

        assert new_s_id == "steiner_3"
        assert tree3d.nodes[new_s_id].parent == tree3d.nodes[s1_id]
        assert tree3d.nodes[new_s_id].children[0] == tree3d.nodes[s2_id]
        assert tree3d.nodes[s2_id].parent == tree3d.nodes[new_s_id]
        assert tree3d.nodes[s1_id].children[0] == tree3d.nodes[new_s_id]
        assert s2_id not in [child.id for child in tree3d.nodes[s1_id].children]

    def test_insert_node_on_branch_terminal(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(0, 0), 0))
        s2_id = tree3d.insert_steiner_node(Point(Point(2, 2), 2), s1_id)
        new_t_id = tree3d.insert_node_on_branch(
            NodeType.TERMINAL, Point(Point(1, 1), 1), s1_id, s2_id
        )

        assert new_t_id == "terminal_1"
        assert tree3d.nodes[new_t_id].type == NodeType.TERMINAL
        assert tree3d.nodes[new_t_id].parent == tree3d.nodes[s1_id]
        assert tree3d.nodes[new_t_id].children[0] == tree3d.nodes[s2_id]

    def test_insert_node_on_branch_invalid_branch_nodes(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(0, 0), 0))
        with pytest.raises(ValueError, match="One or both branch nodes not found"):
            tree3d.insert_node_on_branch(
                NodeType.STEINER, Point(Point(1, 1), 1), s1_id, "non_existent"
            )
        with pytest.raises(ValueError, match="One or both branch nodes not found"):
            tree3d.insert_node_on_branch(
                NodeType.STEINER, Point(Point(1, 1), 1), "non_existent", s1_id
            )

    def test_insert_node_on_branch_not_direct_child(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(0, 0), 0))
        s2_id = tree3d.insert_steiner_node(Point(Point(2, 2), 2))
        with pytest.raises(
            ValueError, match=f"{s2_id} is not a direct child of {s1_id}"
        ):
            tree3d.insert_node_on_branch(
                NodeType.STEINER, Point(Point(1, 1), 1), s1_id, s2_id
            )

    def test_insert_node_on_branch_invalid_node_type(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(0, 0), 0))
        s2_id = tree3d.insert_steiner_node(Point(Point(2, 2), 2), s1_id)
        with pytest.raises(
            ValueError, match="Node type must be NodeType.STEINER or NodeType.TERMINAL"
        ):
            tree3d.insert_node_on_branch(
                NodeType.SOURCE, Point(Point(1, 1), 1), s1_id, s2_id
            )

    def test_find_nearest_node(self):
        tree3d = GlobalRoutingTree3d(Point(Point(0, 0), 0))
        s1_id = tree3d.insert_steiner_node(Point(Point(10, 10), 10))
        s2_id = tree3d.insert_steiner_node(Point(Point(20, 20), 20))
        _ = tree3d.insert_terminal_node(Point(Point(5, 5), 5), s1_id)  # Connected to s1

        nearest_to_origin = tree3d._find_nearest_node(Point(Point(1, 1), 1))
        assert nearest_to_origin == tree3d.source

        nearest_to_s1 = tree3d._find_nearest_node(Point(Point(9, 9), 9))
        assert nearest_to_s1 == tree3d.nodes[s1_id]

        nearest_to_s2 = tree3d._find_nearest_node(Point(Point(21, 21), 21))
        assert nearest_to_s2 == tree3d.nodes[s2_id]

    def test_calculate_wirelength(self):
        tree3d = GlobalRoutingTree3d()
        s1 = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
        _ = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1)
        # source(0,0) -> s1(1,1) = 2
        # s1(1,1) -> t1(2,2) = 2
        # Total = 4
        assert tree3d.calculate_wirelength() == 6

        tree3d2 = GlobalRoutingTree3d(Point(Point(0, 0), 0))
        s1 = tree3d2.insert_steiner_node(Point(Point(1, 0), 0))
        s2 = tree3d2.insert_steiner_node(Point(Point(1, 1), 1), s1)
        _ = tree3d2.insert_terminal_node(Point(Point(0, 1), 1), s2)
        # source(0,0) -> s1(1,0) = 1
        # s1(1,0) -> s2(1,1) = 1
        # s2(1,1) -> t1(0,1) = 1
        # Total = 3
        assert tree3d2.calculate_wirelength() == 4

    def test_get_tree_structure(self):
        tree3d = GlobalRoutingTree3d()
        s1 = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
        _ = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1)
        expected_structure = (
            "SourceNode(source, ((0, 0), 0))\n"
            + "  SteinerNode(steiner_1, ((1, 1), 1))\n"
            + "    TerminalNode(terminal_1, ((2, 2), 2))\n"
        )
        assert tree3d.get_tree_structure() == expected_structure

    def test_find_path_to_source(self):
        tree3d = GlobalRoutingTree3d()
        s1 = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
        t1 = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1)
        path = tree3d.find_path_to_source(t1)
        assert len(path) == 3
        assert path[0].id == "source"
        assert path[1].id == "steiner_1"
        assert path[2].id == "terminal_1"

        with pytest.raises(ValueError, match="Node non_existent not found"):
            tree3d.find_path_to_source("non_existent")

    def test_get_all_terminals(self):
        tree3d = GlobalRoutingTree3d()
        _ = tree3d.insert_terminal_node(Point(Point(1, 1), 1))
        s1 = tree3d.insert_steiner_node(Point(Point(2, 2), 2))
        _ = tree3d.insert_terminal_node(Point(Point(3, 3), 3), s1)
        terminals = tree3d.get_all_terminals()
        assert len(terminals) == 2
        terminal_ids = {node.id for node in terminals}
        assert "terminal_1" in terminal_ids
        assert "terminal_2" in terminal_ids
        # Verify all returned nodes are actually terminals
        for terminal in terminals:
            assert terminal.type == NodeType.TERMINAL

    def test_get_all_steiner_nodes(self):
        tree3d = GlobalRoutingTree3d()
        _ = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
        t1 = tree3d.insert_terminal_node(Point(Point(2, 2), 2))
        _ = tree3d.insert_steiner_node(Point(Point(3, 3), 3), t1)
        steiner_nodes = tree3d.get_all_steiner_nodes()
        assert len(steiner_nodes) == 2
        steiner_ids = {node.id for node in steiner_nodes}
        assert "steiner_1" in steiner_ids
        assert "steiner_2" in steiner_ids
        # Verify all returned nodes are actually steiner nodes
        for steiner in steiner_nodes:
            assert steiner.type == NodeType.STEINER

    def test_optimize_steiner_points(self):
        tree3d = GlobalRoutingTree3d()
        s1_id = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
        t1_id = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1_id)
        # Initial state: source -> s1 -> t1
        assert len(tree3d.get_all_steiner_nodes()) == 1
        assert tree3d.nodes[t1_id].parent.id == s1_id

        tree3d.optimize_steiner_points()
        # After optimization: source -> t1 (s1 should be removed)
        assert len(tree3d.get_all_steiner_nodes()) == 0
        assert tree3d.nodes[t1_id].parent.id == "source"
        assert tree3d.nodes[t1_id] in tree3d.source.children
        assert s1_id not in tree3d.nodes

        # Test with a steiner node that should not be removed (multiple children)
        tree3d2 = GlobalRoutingTree3d()
        s1_id_2 = tree3d2.insert_steiner_node(Point(Point(1, 1), 1))
        _ = tree3d2.insert_terminal_node(Point(Point(2, 2), 2), s1_id_2)
        _ = tree3d2.insert_terminal_node(Point(Point(0, 2), 2), s1_id_2)
        assert len(tree3d2.get_all_steiner_nodes()) == 1
        tree3d2.optimize_steiner_points()
        assert (
            len(tree3d2.get_all_steiner_nodes()) == 1
        )  # s1_id_2 should not be removed

        # Test with a steiner node that should not be removed (no parent - source)
        tree3d3 = GlobalRoutingTree3d()
        _ = tree3d3.insert_steiner_node(Point(Point(1, 1), 1))  # Connected to source
        assert len(tree3d3.get_all_steiner_nodes()) == 1
        tree3d3.optimize_steiner_points()
        assert (
            len(tree3d3.get_all_steiner_nodes()) == 1
        )  # s1_id_3 should not be removed

    def test_node_type_enum_values(self):
        """Test that NodeType enum has the expected values"""
        assert NodeType.STEINER.name == "STEINER"
        assert NodeType.TERMINAL.name == "TERMINAL"
        assert NodeType.SOURCE.name == "SOURCE"

        # Test enum comparison
        node = RoutingNode3d("test", NodeType.TERMINAL)
        assert node.type == NodeType.TERMINAL
        assert node.type != NodeType.STEINER
