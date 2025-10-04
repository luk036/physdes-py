import math
from typing import List, Tuple


class RoutingNode:
    """Represents a node in the global routing tree."""

    def __init__(self, node_id: str, node_type: str, x: float = 0, y: float = 0):
        self.id = node_id
        self.type = node_type  # 'steiner', 'terminal', 'source'
        self.x = x
        self.y = y
        self.children = []
        self.parent = None
        self.capacitance = 0.0
        self.delay = 0.0

    def add_child(self, child_node):
        """Add a child node to this node."""
        child_node.parent = self
        self.children.append(child_node)

    def remove_child(self, child_node):
        """Remove a child node."""
        if child_node in self.children:
            self.children.remove(child_node)
            child_node.parent = None

    def get_position(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def manhattan_distance(self, other_node) -> float:
        """Calculate Manhattan distance to another node."""
        return abs(self.x - other_node.x) + abs(self.y - other_node.y)

    def euclidean_distance(self, other_node) -> float:
        """Calculate Euclidean distance to another node."""
        return math.sqrt((self.x - other_node.x) ** 2 + (self.y - other_node.y) ** 2)

    def __str__(self):
        return f"{self.type.capitalize()}Node({self.id}, ({self.x}, {self.y}))"


class GlobalRoutingTree:
    """Global routing tree that supports Steiner node and terminal node insertion."""

    def __init__(self, source_position: Tuple[float, float] = (0, 0)):
        self.source = RoutingNode(
            "source", "source", source_position[0], source_position[1]
        )
        self.nodes = {"source": self.source}
        self.next_steiner_id = 1
        self.next_terminal_id = 1

    def insert_steiner_node(self, x: float, y: float, parent_id: str = None) -> str:
        """Insert a new Steiner node into the routing tree."""
        steiner_id = f"steiner_{self.next_steiner_id}"
        self.next_steiner_id += 1

        steiner_node = RoutingNode(steiner_id, "steiner", x, y)
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

    def insert_terminal_node(self, x: float, y: float, parent_id: str = None) -> str:
        """Insert a new terminal (sink) node into the routing tree."""
        terminal_id = f"terminal_{self.next_terminal_id}"
        self.next_terminal_id += 1

        terminal_node = RoutingNode(terminal_id, "terminal", x, y)
        self.nodes[terminal_id] = terminal_node

        if parent_id is None:
            # If no parent specified, find the nearest node
            nearest_node = self._find_nearest_node(x, y)
            nearest_node.add_child(terminal_node)
        else:
            # Connect to specified parent
            if parent_id in self.nodes:
                parent_node = self.nodes[parent_id]
                parent_node.add_child(terminal_node)
            else:
                raise ValueError(f"Parent node {parent_id} not found")

        return terminal_id

    def insert_node_on_branch(
        self,
        new_node_type: str,
        x: float,
        y: float,
        branch_start_id: str,
        branch_end_id: str,
    ) -> str:
        """Insert a new node on an existing branch between two nodes."""
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
        if new_node_type == "steiner":
            node_id = f"steiner_{self.next_steiner_id}"
            self.next_steiner_id += 1
        elif new_node_type == "terminal":
            node_id = f"terminal_{self.next_terminal_id}"
            self.next_terminal_id += 1
        else:
            raise ValueError("Node type must be 'steiner' or 'terminal'")

        new_node = RoutingNode(node_id, new_node_type, x, y)
        self.nodes[node_id] = new_node

        # Remove direct connection between start and end
        start_node.remove_child(end_node)

        # Insert new node in between
        start_node.add_child(new_node)
        new_node.add_child(end_node)

        return node_id

    def _find_nearest_node(self, x: float, y: float) -> RoutingNode:
        """Find the nearest node to the given coordinates."""
        if not self.nodes:
            return self.source

        target_node = RoutingNode("temp", "temp", x, y)
        nearest_node = self.source
        min_distance = self.source.manhattan_distance(target_node)

        for node in self.nodes.values():
            distance = node.manhattan_distance(target_node)
            if distance < min_distance:
                min_distance = distance
                nearest_node = node

        return nearest_node

    def calculate_wirelength(self) -> float:
        """Calculate total wirelength of the routing tree."""
        total_length = 0.0

        def traverse(node: RoutingNode):
            nonlocal total_length
            for child in node.children:
                total_length += node.manhattan_distance(child)
                traverse(child)

        traverse(self.source)
        return total_length

    def get_tree_structure(self, node: RoutingNode = None, level: int = 0) -> str:
        """Get a string representation of the tree structure."""
        if node is None:
            node = self.source

        result = "  " * level + str(node) + "\n"
        for child in node.children:
            result += self.get_tree_structure(child, level + 1)

        return result

    def find_path_to_source(self, node_id: str) -> List[RoutingNode]:
        """Find the path from a node back to the source."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")

        path = []
        current_node = self.nodes[node_id]

        while current_node is not None:
            path.append(current_node)
            current_node = current_node.parent

        return path[::-1]  # Reverse to get source to node

    def get_all_terminals(self) -> List[RoutingNode]:
        """Get all terminal nodes in the tree."""
        return [node for node in self.nodes.values() if node.type == "terminal"]

    def get_all_steiner_nodes(self) -> List[RoutingNode]:
        """Get all Steiner nodes in the tree."""
        return [node for node in self.nodes.values() if node.type == "steiner"]

    def optimize_steiner_points(self):
        """Simple optimization to remove unnecessary Steiner points."""
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


# Example usage and demonstration
if __name__ == "__main__":
    # Create a global routing tree with source at (0, 0)
    routing_tree = GlobalRoutingTree((0, 0))

    print("=== Global Routing Tree Demo ===")

    # Insert some Steiner nodes
    steiner1 = routing_tree.insert_steiner_node(2, 3)
    steiner2 = routing_tree.insert_steiner_node(4, 1, steiner1)
    steiner3 = routing_tree.insert_steiner_node(1, 5)

    print(f"Inserted Steiner nodes: {steiner1}, {steiner2}, {steiner3}")

    # Insert terminal nodes
    terminal1 = routing_tree.insert_terminal_node(3, 6)
    terminal2 = routing_tree.insert_terminal_node(5, 2, steiner2)
    terminal3 = routing_tree.insert_terminal_node(2, 8)

    print(f"Inserted terminal nodes: {terminal1}, {terminal2}, {terminal3}")

    # Insert a node on an existing branch
    new_steiner = routing_tree.insert_node_on_branch(
        "steiner", 3, 4, steiner1, steiner2
    )
    print(f"Inserted new Steiner node on branch: {new_steiner}")

    # Display tree structure
    routing_tree.visualize_tree()

    # Demonstrate path finding
    print("\n=== Path Finding ===")
    path = routing_tree.find_path_to_source(terminal2)
    print(f"Path from source to {terminal2}:")
    for node in path:
        print(f"  {node}")

    # Calculate wirelength
    print(f"\nTotal wirelength: {routing_tree.calculate_wirelength():.2f}")

    # Show optimization
    print("\n=== After Optimization ===")
    routing_tree.optimize_steiner_points()
    routing_tree.visualize_tree()

    # Add more complex example
    print("\n=== Complex Example ===")
    complex_tree = GlobalRoutingTree((5, 5))

    # Create a more complex routing structure
    s1 = complex_tree.insert_steiner_node(3, 3)
    s2 = complex_tree.insert_steiner_node(7, 3)
    s3 = complex_tree.insert_steiner_node(3, 7)
    s4 = complex_tree.insert_steiner_node(7, 7)

    # Add terminals at the corners
    t1 = complex_tree.insert_terminal_node(1, 1, s1)
    t2 = complex_tree.insert_terminal_node(9, 1, s2)
    t3 = complex_tree.insert_terminal_node(1, 9, s3)
    t4 = complex_tree.insert_terminal_node(9, 9, s4)

    complex_tree.visualize_tree()
