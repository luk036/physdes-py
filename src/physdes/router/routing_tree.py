from enum import Enum, auto
from typing import Any, List, Optional, Tuple

from physdes.point import Point
from physdes.interval import Interval


class NodeType(Enum):
    """Enum representing different types of routing nodes."""

    STEINER = auto()
    TERMINAL = auto()
    SOURCE = auto()


class RoutingNode:
    """Represents a node in the global routing tree."""

    def __init__(self, node_id: str, node_type: NodeType, pt: Point[Any, Any]):
        self.id = node_id
        self.type = node_type
        self.pt = pt
        self.children: List["RoutingNode"] = []
        self.parent: Optional["RoutingNode"] = None
        self.capacitance = 0.0
        self.delay = 0.0
        self.path_length = 0  # for performance-driven routing

    def add_child(self, child_node: "RoutingNode"):
        """Add a child node to this node.

        Examples:
            >>> parent = RoutingNode("p1", NodeType.STEINER, Point(0, 0))
            >>> child = RoutingNode("c1", NodeType.TERMINAL, Point(0, 0))
            >>> parent.add_child(child)
            >>> len(parent.children)
            1
            >>> child.parent == parent
            True
            >>> parent = RoutingNode("p1", NodeType.STEINER, Point(Point(0, 0), 0))
            >>> child = RoutingNode("c1", NodeType.TERMINAL, Point(Point(0, 0), 0))
            >>> parent.add_child(child)
            >>> len(parent.children)
            1
            >>> child.parent == parent
            True
        """
        child_node.parent = self
        self.children.append(child_node)

    def remove_child(self, child_node: "RoutingNode"):
        """Remove a child node.

        Examples:
            >>> parent = RoutingNode("p1", NodeType.STEINER, Point(0, 0))
            >>> child = RoutingNode("c1", NodeType.TERMINAL, Point(0, 0))
            >>> parent.add_child(child)
            >>> parent.remove_child(child)
            >>> len(parent.children)
            0
            >>> child.parent is None
            True
            >>> parent = RoutingNode("p1", NodeType.STEINER, Point(Point(0, 0), 0))
            >>> child = RoutingNode("c1", NodeType.TERMINAL, Point(Point(0, 0), 0))
            >>> parent.add_child(child)
            >>> parent.remove_child(child)
            >>> len(parent.children)
            0
            >>> child.parent is None
            True
        """
        if child_node in self.children:
            self.children.remove(child_node)
            child_node.parent = None

    def get_position(self) -> Point[int, int]:
        """Get the position of the node.

        Returns:
            A Point object.

        Examples:
            >>> from physdes.point import Point
            >>> node = RoutingNode("n1", NodeType.TERMINAL, Point(10, 20))
            >>> node.get_position()
            Point(10, 20)
            >>> node = RoutingNode("n1", NodeType.TERMINAL, Point(Point(10, 20), 20))
            >>> node.get_position()
            Point(Point(10, 20), 20)
        """
        return self.pt

    def manhattan_distance(self, other_node: "RoutingNode") -> int:
        """Calculate Manhattan distance to another node.

        Args:
            other_node: The other node to calculate the distance to.

        Returns:
            The Manhattan distance.

        Examples:
            >>> from physdes.point import Point
            >>> node1 = RoutingNode("n1", NodeType.TERMINAL, Point(0, 0))
            >>> node2 = RoutingNode("n2", NodeType.TERMINAL, Point(3, 4))
            >>> node1.manhattan_distance(node2)
            7
            >>> node1 = RoutingNode("n1", NodeType.TERMINAL, Point(Point(0, 0), 0))
            >>> node2 = RoutingNode("n2", NodeType.TERMINAL, Point(Point(3, 4), 4))
            >>> node1.manhattan_distance(node2)
            11
        """
        return self.pt.min_dist_with(other_node.pt)

    def __str__(self) -> str:
        type_name = self.type.name.capitalize()
        return f"{type_name}Node({self.id}, ({self.pt.xcoord}, {self.pt.ycoord}))"


class GlobalRoutingTree:
    """Global routing tree that supports Steiner node and terminal node insertion.

    .. svgbob::
       :align: center

             +--.----------o
             |   `.        |
             |     `.      |
             |       `.    |
             o---------`---+

                +--<---o
                |
                *-------->---o
                |
         o--->--+

    """

    def __init__(self, source_position: Point[Any, Any]):
        """
        Initializes the GlobalRoutingTree.

        Args:
            source_position: The starting point for the routing.

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(1, 1))
            >>> tree.source.pt
            Point(1, 1)
            >>> tree3d = GlobalRoutingTree(Point(Point(1, 1), 1))
            >>> tree3d.source.pt
            Point(Point(1, 1), 1)
        """
        self.source = RoutingNode("source", NodeType.SOURCE, source_position)
        self.nodes = {"source": self.source}
        self.next_steiner_id = 1
        self.next_terminal_id = 1

    def insert_steiner_node(
        self,
        pt: Point[Any, Any],
        parent_id: Optional[str] = None,
    ) -> str:
        """Insert a new Steiner node into the routing tree.

        Args:
            x: The x-coordinate of the new node.
            y: The y-coordinate of the new node.
            parent_id: The ID of the parent node. If None, connect to the source.

        Returns:
            The ID of the new Steiner node.

        Examples:
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> steiner_id = tree.insert_steiner_node(Point(1, 1))
            >>> steiner_id
            'steiner_1'
            >>> tree.nodes[steiner_id].parent == tree.source
            True
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> steiner_id = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
            >>> steiner_id
            'steiner_1'
            >>> tree3d.nodes[steiner_id].parent == tree3d.source
            True
        """
        steiner_id = f"steiner_{self.next_steiner_id}"
        self.next_steiner_id += 1

        steiner_node = RoutingNode(steiner_id, NodeType.STEINER, pt)
        self.nodes[steiner_id] = steiner_node

        if parent_id is None:
            # If no parent specified, connect to source
            self.source.add_child(steiner_node)
        else:
            # Connect to specified parent
            if parent_id in self.nodes:
                parent_node = self.nodes[parent_id]
                parent_node.add_child(steiner_node)
            else:
                raise ValueError(f"Parent node {parent_id} not found")

        return steiner_id

    def _find_nearest_node(self, pt: Point[Any, Any]) -> "RoutingNode":
        """Find the nearest node to the given coordinates."""
        if not self.nodes:
            return self.source

        target_node = RoutingNode("temp", NodeType.STEINER, pt)
        nearest_node = self.source
        min_distance = self.source.manhattan_distance(target_node)

        for node in self.nodes.values():
            distance = node.manhattan_distance(target_node)
            if distance < min_distance:
                min_distance = distance
                nearest_node = node

        return nearest_node

    def insert_terminal_node(
        self,
        pt: Point[Any, Any],
        parent_id: Optional[str] = None,
    ) -> str:
        """Insert a new terminal (sink) node into the routing tree.

        Args:
            pt: The position of the new node.
            parent_id: The ID of the parent node. If None, find the nearest node.

        Returns:
            The ID of the new terminal node.

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> terminal_id = tree.insert_terminal_node(Point(1, 1))
            >>> terminal_id
            'terminal_1'
            >>> tree.nodes[terminal_id].parent == tree.source
            True
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> terminal_id = tree3d.insert_terminal_node(Point(Point(1, 1), 1))
            >>> terminal_id
            'terminal_1'
            >>> tree3d.nodes[terminal_id].parent == tree3d.source
            True
        """
        terminal_id = f"terminal_{self.next_terminal_id}"
        self.next_terminal_id += 1

        terminal_node = RoutingNode(terminal_id, NodeType.TERMINAL, pt)

        if parent_id is None:
            # If no parent specified, find the nearest node
            nearest_node = self._find_nearest_node(pt)
            nearest_node.add_child(terminal_node)
        else:
            # Connect to specified parent
            if parent_id in self.nodes:
                parent_node = self.nodes[parent_id]
                parent_node.add_child(terminal_node)
            else:
                raise ValueError(f"Parent node {parent_id} not found")

        self.nodes[terminal_id] = terminal_node

        return terminal_id

    def insert_node_on_branch(
        self,
        new_node_type: NodeType,
        pt: Point[Any, Any],
        branch_start_id: str,
        branch_end_id: str,
    ) -> str:
        """Insert a new node on an existing branch between two nodes.

        .. svgbob::
           :align: center

            Before:
            +-------------+      +-----------+
            | branch_start|----->| branch_end|
            +-------------+      +-----------+

            After:
            +-------------+      +----------+      +-----------+
            | branch_start|----->| new_node |----->| branch_end|
            +-------------+      +----------+      +-----------+

        Args:
            new_node_type: The type of the new node (NodeType.STEINER or NodeType.TERMINAL).
            x: The x-coordinate of the new node.
            y: The y-coordinate of the new node.
            branch_start_id: The ID of the starting node of the branch.
            branch_end_id: The ID of the ending node of the branch.

        Returns:
            The ID of the new node.

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> s1 = tree.insert_steiner_node(Point(1, 1))
            >>> t1 = tree.insert_terminal_node(Point(2, 2), s1)
            >>> new_id = tree.insert_node_on_branch(NodeType.STEINER, Point(1, 2), s1, t1)
            >>> new_id
            'steiner_2'
            >>> tree.nodes[new_id].parent.id == s1
            True
            >>> tree.nodes[t1].parent.id == new_id
            True
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> s1 = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
            >>> t1 = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1)
            >>> new_id = tree3d.insert_node_on_branch(NodeType.STEINER, Point(Point(1, 2), 2), s1, t1)
            >>> new_id
            'steiner_2'
            >>> tree3d.nodes[new_id].parent.id == s1
            True
            >>> tree3d.nodes[t1].parent.id == new_id
            True
        """
        if branch_start_id not in self.nodes or branch_end_id not in self.nodes:
            raise ValueError("One or both branch nodes not found")

        start_node = self.nodes[branch_start_id]
        end_node = self.nodes[branch_end_id]

        # Verify that end_node is a child of start_node
        if end_node not in start_node.children:
            raise ValueError(
                f"{branch_end_id} is not a direct child of {branch_start_id}"
            )

        # Create new node
        if new_node_type == NodeType.STEINER:
            node_id = f"steiner_{self.next_steiner_id}"
            self.next_steiner_id += 1
        elif new_node_type == NodeType.TERMINAL:
            node_id = f"terminal_{self.next_terminal_id}"
            self.next_terminal_id += 1
        else:
            raise ValueError("Node type must be NodeType.STEINER or NodeType.TERMINAL")

        new_node = RoutingNode(node_id, new_node_type, pt)
        self.nodes[node_id] = new_node

        # Remove direct connection between start and end
        start_node.remove_child(end_node)

        # Insert new node in between
        start_node.add_child(new_node)
        new_node.add_child(end_node)

        return node_id

    def _find_insertion_point(
        self,
        pt: Point[Any, Any],
        keepouts: Optional[List[Point[Interval[int], Interval[int]]]] = None,
        allowed_wirelength: Optional[int] = None,
    ) -> Tuple[Optional["RoutingNode"], "RoutingNode"]:
        """
        Find the nearest insertion point to the given coordinates, avoiding keepouts.

        Args:
            pt: The point to insert.
            keepouts: A list of rectangular regions to avoid.
            allowed_wirelength: The maximum allowed wirelength from the source.

        Returns:
            A tuple containing the parent node and the nearest node for insertion.

        .. svgbob::
           :align: center

            source          "nearest_pt"
               O-------#--------o-----------o sink 2
                       |        :
                       |  +---+ :
                       |  |   | :
                       |  |   | :
                       |  |   | o pt
                       |  +---+
                       o   keepout
                  sink 1

        Examples:
            >>> from physdes.point import Point
            >>> from physdes.interval import Interval
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> _ = tree.insert_terminal_node(Point(10, 0))
            >>> keepouts = [Point(Interval(4, 6), Interval(-1, 1))]
            >>> parent, nearest = tree._find_insertion_point(Point(5, 5), keepouts)
            >>> nearest.pt
            Point(0, 0)
        """
        if not self.nodes:
            return None, self.source

        nearest_node = self.source
        parent_node = None
        min_distance = self.source.pt.min_dist_with(pt)

        def traverse(node: "RoutingNode"):
            nonlocal nearest_node
            nonlocal parent_node
            nonlocal min_distance
            for child in node.children:
                possible_path = node.pt.hull_with(child.pt)
                distance = possible_path.min_dist_with(pt)
                nearest_pt = possible_path.nearest_to(pt)

                if allowed_wirelength is not None:
                    path_length = (
                        node.path_length + node.pt.min_dist_with(nearest_pt) + distance
                    )
                    if path_length > allowed_wirelength:
                        continue

                if distance < min_distance:
                    block = False
                    if keepouts is not None:
                        path1 = nearest_pt.hull_with(pt)
                        path2 = nearest_pt.hull_with(node.pt)
                        path3 = nearest_pt.hull_with(child.pt)
                        for keepout in keepouts:
                            if (
                                keepout.contains(nearest_pt)
                                or keepout.blocks(path1)
                                or keepout.blocks(path2)
                                or keepout.blocks(path3)
                            ):
                                block = True
                                break
                    if not block:
                        min_distance = distance
                        if nearest_pt == node.pt:
                            nearest_node = node
                            parent_node = None
                        elif nearest_pt == child.pt:
                            nearest_node = child
                            parent_node = None
                        else:  # need to insert steiner point
                            nearest_node = child
                            parent_node = node
                traverse(child)

        traverse(self.source)
        return parent_node, nearest_node

    def insert_terminal_with_steiner(
        self,
        pt: Point[Any, Any],
        keepouts: Optional[List[Point[Interval[int], Interval[int]]]] = None,
    ):
        """
        Inserts a terminal node, adding a Steiner point if it reduces wire length.

        .. svgbob::
           :align: center

                parent
                  O
                  |
                  |
                  o-----------o child
                 /
                /
               o pt

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> tree.insert_terminal_with_steiner(Point(2, 2))
            >>> tree.calculate_wirelength()
            4
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> tree3d.insert_terminal_with_steiner(Point(Point(2, 2), 2))
            >>> tree3d.calculate_wirelength()
            6
            >>> from physdes.interval import Interval
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> _ = tree.insert_terminal_node(Point(10, 0))
            >>> keepouts = [Point(Interval(4, 6), Interval(-1, 1))]
            >>> tree.insert_terminal_with_steiner(Point(5, 5), keepouts)
            >>> tree.calculate_wirelength()
            20
        """
        terminal_id = f"terminal_{self.next_terminal_id}"
        self.next_terminal_id += 1

        terminal_node = RoutingNode(terminal_id, NodeType.TERMINAL, pt)

        parent_node, nearest_node = self._find_insertion_point(pt, keepouts)

        if parent_node is None:
            nearest_node.add_child(terminal_node)
        else:  # need to insert steiner point
            node_id = f"steiner_{self.next_steiner_id}"
            self.next_steiner_id += 1

            possible_path = parent_node.pt.hull_with(nearest_node.pt)
            nearest_pt = possible_path.nearest_to(pt)  # type: ignore
            new_node = RoutingNode(node_id, NodeType.STEINER, nearest_pt)
            self.nodes[node_id] = new_node

            # Remove direct connection between parent and nearest node
            parent_node.remove_child(nearest_node)

            # Insert new node in between
            parent_node.add_child(new_node)
            new_node.add_child(nearest_node)
            new_node.add_child(terminal_node)

        self.nodes[terminal_id] = terminal_node

        return

    def insert_terminal_with_constraints(
        self,
        pt: Point[Any, Any],
        allowed_wirelength: int,
        keepouts: Optional[List[Point[Interval[int], Interval[int]]]] = None,
    ):
        """
        Inserts a terminal node with wirelength constraints, adding a Steiner point if it reduces wire length.

        Args:
            pt: The position of the terminal to insert.
            allowed_wirelength: The maximum allowed wirelength from the source.
            keepouts: A list of rectangular regions to avoid.

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> tree.insert_terminal_with_constraints(Point(2, 2), 10)
            >>> tree.calculate_wirelength()
            4
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> tree3d.insert_terminal_with_constraints(Point(Point(2, 2), 2), 10)
            >>> tree3d.calculate_wirelength()
            6
            >>> from physdes.interval import Interval
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> _ = tree.insert_terminal_node(Point(10, 0))
            >>> keepouts = [Point(Interval(4, 6), Interval(-1, 1))]
            >>> tree.insert_terminal_with_constraints(Point(5, 5), 100, keepouts)
            >>> tree.calculate_wirelength()
            20
        """
        terminal_id = f"terminal_{self.next_terminal_id}"
        self.next_terminal_id += 1

        terminal_node = RoutingNode(terminal_id, NodeType.TERMINAL, pt)

        parent_node, nearest_node = self._find_insertion_point(
            pt, keepouts, allowed_wirelength
        )

        if parent_node is None:
            nearest_node.add_child(terminal_node)
            terminal_node.path_length = (
                nearest_node.path_length + nearest_node.pt.min_dist_with(pt)
            )
        else:  # need to insert steiner point
            node_id = f"steiner_{self.next_steiner_id}"
            self.next_steiner_id += 1

            possible_path = parent_node.pt.hull_with(nearest_node.pt)
            nearest_pt = possible_path.nearest_to(pt)
            new_node = RoutingNode(node_id, NodeType.STEINER, nearest_pt)
            self.nodes[node_id] = new_node

            # Remove direct connection between parent and nearest node
            parent_node.remove_child(nearest_node)

            # Insert new node in between
            parent_node.add_child(new_node)
            new_node.path_length = (
                parent_node.path_length + parent_node.pt.min_dist_with(nearest_pt)
            )
            new_node.add_child(nearest_node)
            new_node.add_child(terminal_node)
            terminal_node.path_length = new_node.path_length + nearest_pt.min_dist_with(
                pt
            )

        self.nodes[terminal_id] = terminal_node

        return

    def calculate_wirelength(self) -> int:
        """Calculate total wirelength of the routing tree.

        Returns:
            The total wirelength.

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> s1 = tree.insert_steiner_node(Point(1, 1))
            >>> t1 = tree.insert_terminal_node(Point(2, 2), s1)
            >>> tree.calculate_wirelength()
            4
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> s1 = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
            >>> t1 = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1)
            >>> tree3d.calculate_wirelength()
            6
        """
        total_length = 0

        def traverse(node: "RoutingNode"):
            nonlocal total_length
            for child in node.children:
                total_length += node.manhattan_distance(child)
                traverse(child)

        traverse(self.source)
        return total_length

    def get_tree_structure(
        self,
        node: Optional["RoutingNode"] = None,
        level: int = 0,
    ) -> str:
        """Get a string representation of the tree structure."""
        if node is None:
            node = self.source

        result = "  " * level + str(node) + "\n"
        for child in node.children:
            result += self.get_tree_structure(child, level + 1)

        return result

    def find_path_to_source(self, node_id: str) -> List["RoutingNode"]:
        """Find the path from a node back to the source.

        Args:
            node_id: The ID of the node to find the path from.

        Returns:
            A list of nodes representing the path from the source to the given node.

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> s1 = tree.insert_steiner_node(Point(1, 1))
            >>> t1 = tree.insert_terminal_node(Point(2, 2), s1)
            >>> path = tree.find_path_to_source(t1)
            >>> len(path)
            3
            >>> path[0].id
            'source'
            >>> path[1].id
            'steiner_1'
            >>> path[2].id
            'terminal_1'
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> s1 = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
            >>> t1 = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1)
            >>> path = tree3d.find_path_to_source(t1)
            >>> len(path)
            3
            >>> path[0].id
            'source'
            >>> path[1].id
            'steiner_1'
            >>> path[2].id
            'terminal_1'
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")

        path = []
        current_node: Optional[RoutingNode] = self.nodes[node_id]

        while current_node is not None:
            path.append(current_node)
            current_node = current_node.parent

        return path[::-1]  # Reverse to get source to node

    def get_all_terminals(self) -> List["RoutingNode"]:
        """Get all terminal nodes in the tree.

        Returns:
            A list of all terminal nodes.

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> t1 = tree.insert_terminal_node(Point(1, 1))
            >>> t2 = tree.insert_terminal_node(Point(2, 2))
            >>> terminals = tree.get_all_terminals()
            >>> len(terminals)
            2
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> t1 = tree3d.insert_terminal_node(Point(Point(1, 1), 1))
            >>> t2 = tree3d.insert_terminal_node(Point(Point(2, 2), 2))
            >>> terminals = tree3d.get_all_terminals()
            >>> len(terminals)
            2
        """
        return [node for node in self.nodes.values() if node.type == NodeType.TERMINAL]

    def get_all_steiner_nodes(self) -> List["RoutingNode"]:
        """Get all Steiner nodes in the tree.

        Returns:
            A list of all Steiner nodes.

        Examples:
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> s1 = tree.insert_steiner_node(Point(1, 1))
            >>> s2 = tree.insert_steiner_node(Point(2, 2))
            >>> steiners = tree.get_all_steiner_nodes()
            >>> len(steiners)
            2
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> s1 = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
            >>> s2 = tree3d.insert_steiner_node(Point(Point(2, 2), 2))
            >>> steiners = tree3d.get_all_steiner_nodes()
            >>> len(steiners)
            2
        """
        return [node for node in self.nodes.values() if node.type == NodeType.STEINER]

    def optimize_steiner_points(self) -> None:
        """Simple optimization to remove unnecessary Steiner points.

        Examples:
            >>> from physdes.point import Point
            >>> tree = GlobalRoutingTree(Point(0, 0))
            >>> s1 = tree.insert_steiner_node(Point(1, 1))
            >>> t1 = tree.insert_terminal_node(Point(2, 2), s1)
            >>> tree.optimize_steiner_points()
            >>> len(tree.get_all_steiner_nodes())
            0
            >>> tree3d = GlobalRoutingTree(Point(Point(0, 0), 0))
            >>> s1 = tree3d.insert_steiner_node(Point(Point(1, 1), 1))
            >>> t1 = tree3d.insert_terminal_node(Point(Point(2, 2), 2), s1)
            >>> tree3d.optimize_steiner_points()
            >>> len(tree3d.get_all_steiner_nodes())
            0
        """
        steiner_nodes = self.get_all_steiner_nodes()

        for steiner in steiner_nodes:
            # If Steiner node has only one child and one parent, it can be removed
            if len(steiner.children) == 1 and steiner.parent is not None:
                parent = steiner.parent
                child = steiner.children[0]

                # Remove Steiner node and connect parent directly to child
                parent.remove_child(steiner)
                parent.add_child(child)

                # Remove from nodes dictionary
                del self.nodes[steiner.id]

    def visualize_tree(self):
        """Simple ASCII visualization of the routing tree."""
        print("Global Routing Tree Structure:")
        print("=" * 40)
        print(self.get_tree_structure())
        print(f"Total wirelength: {self.calculate_wirelength():.2f}")
        print(f"Total nodes: {len(self.nodes)}")
        print(f"Terminals: {len(self.get_all_terminals())}")
        print(f"Steiner points: {len(self.get_all_steiner_nodes())}")

    def visualize_tree3d(self):
        """Simple ASCII visualization of the routing tree3d."""
        print("Global Routing Tree3d Structure:")
        print("=" * 40)
        print(self.get_tree_structure())
        print(f"Total wirelength: {self.calculate_wirelength():.2f}")
        print(f"Total nodes: {len(self.nodes)}")
        print(f"Terminals: {len(self.get_all_terminals())}")
        print(f"Steiner points: {len(self.get_all_steiner_nodes())}")
