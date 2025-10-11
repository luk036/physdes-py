"""
Deferred Merge Embedding (DME) Algorithm for Clock Tree Synthesis

This module implements the DME algorithm for constructing zero-skew clock trees in VLSI physical design.
The algorithm balances clock delays to all sinks while minimizing wirelength.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from physdes.merge_obj import MergeObj
from physdes.point import Point
from physdes.interval import Interval


@dataclass
class Sink:
    """Represents a clock sink with position and capacitance"""

    name: str
    position: Point[int, int]
    capacitance: float = 1.0


@dataclass
class TreeNode:
    """Represents a node in the clock tree"""

    name: str
    position: Point[int, int]
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None
    parent: Optional["TreeNode"] = None
    wire_length: float = 0.0
    delay: float = 0.0
    capacitance: float = 0.0


class DMEAlgorithm:
    """
    Deferred Merge Embedding (DME) Algorithm for Clock Tree Synthesis

    The DME algorithm constructs a zero-skew clock tree by:
    1. Building a bottom-up merging tree (usually from a minimum spanning tree)
    2. Computing merging segments for each internal node
    3. Embedding the internal nodes to minimize wirelength while maintaining zero skew
    """

    def __init__(self, unit_resistance: float = 1.0, unit_capacitance: float = 1.0):
        """
        Initialize DME algorithm with technology parameters

        Args:
            unit_resistance: Resistance per unit length
            unit_capacitance: Capacitance per unit length
        """
        self.unit_resistance = unit_resistance
        self.unit_capacitance = unit_capacitance
        self.tapering_factor = 0.7  # Buffer/wire sizing factor

    def build_clock_tree(self, sinks: List[Sink]) -> TreeNode:
        """
        Build a zero-skew clock tree for the given sinks

        Args:
            sinks: List of clock sinks with positions and capacitances

        Returns:
            Root node of the clock tree
        """
        if not sinks:
            raise ValueError("No sinks provided")

        # Step 1: Create initial leaf nodes
        nodes = [
            TreeNode(name=s.name, position=s.position, capacitance=s.capacitance)
            for s in sinks
        ]

        # Step 2: Build merging tree using balanced bipartition
        merging_tree = self._build_merging_tree(nodes)

        # Step 3: Perform bottom-up merging segment computation
        merging_segments = self._compute_merging_segments(merging_tree)

        # Step 4: Perform top-down embedding
        clock_tree = self._embed_tree(merging_tree, merging_segments)

        # Step 5: Compute delays and wire lengths
        self._compute_tree_parameters(clock_tree)

        return clock_tree

    def _build_merging_tree(self, nodes: List[TreeNode]) -> TreeNode:
        """
        Build a balanced merging tree using recursive bipartition

        Args:
            nodes: List of tree nodes to merge

        Returns:
            Root node of the merging tree
        """
        if len(nodes) == 1:
            return nodes[0]

        # Sort nodes by x-coordinate for balanced partitioning
        sorted_nodes = sorted(nodes, key=lambda n: n.position.xcoord)

        # Split into two balanced groups
        mid = len(sorted_nodes) // 2
        left_group = sorted_nodes[:mid]
        right_group = sorted_nodes[mid:]

        # Recursively build subtrees
        left_child = self._build_merging_tree(left_group)
        right_child = self._build_merging_tree(right_group)

        # Create parent node (position will be determined during embedding)
        parent = TreeNode(
            name=f"n{len(nodes)}",
            position=Point(0, 0),  # Temporary position
            left=left_child,
            right=right_child,
        )
        left_child.parent = parent
        right_child.parent = parent

        return parent

    def _compute_merging_segments(self, root: TreeNode) -> Dict[str, MergeObj]:
        """
        Compute merging segments for all nodes in bottom-up order

        Args:
            root: Root node of the merging tree

        Returns:
            Dictionary mapping node names to their merging segments
        """
        merging_segments = {}

        def compute_segment(node: TreeNode) -> MergeObj:
            if node.left is None and node.right is None:
                # Leaf node: merging segment is the sink point
                ms = MergeObj.construct(node.position.xcoord, node.position.ycoord)
                merging_segments[node.name] = ms
                return ms

            # Internal node: compute from children
            left_ms = compute_segment(node.left)
            right_ms = compute_segment(node.right)

            # Compute merging cost (Manhattan distance between segments)
            distance = left_ms.min_dist_with(right_ms)

            # Compute required delay balancing
            left_delay = node.left.delay + self._wire_delay(
                distance, node.left.capacitance
            )
            right_delay = node.right.delay + self._wire_delay(
                distance, node.right.capacitance
            )

            # Adjust for zero skew
            skew = abs(left_delay - right_delay)
            if skew > 1e-6:
                # Need to balance delays by adjusting wire lengths
                if left_delay > right_delay:
                    # Right branch needs longer wire
                    extra_length = skew / self._wire_delay_per_unit(
                        node.right.capacitance
                    )
                    right_ms = self._extend_segment(right_ms, extra_length)
                else:
                    # Left branch needs longer wire
                    extra_length = skew / self._wire_delay_per_unit(
                        node.left.capacitance
                    )
                    left_ms = self._extend_segment(left_ms, extra_length)

            # Merge the segments
            merged_segment = left_ms.merge_with(right_ms)
            merging_segments[node.name] = merged_segment

            # Update node capacitance (sum of children + wire capacitance)
            wire_cap = self._wire_capacitance(distance)
            node.capacitance = node.left.capacitance + node.right.capacitance + wire_cap

            return merged_segment

        compute_segment(root)
        return merging_segments

    def _embed_tree(
        self, merging_tree: TreeNode, merging_segments: Dict[str, MergeObj]
    ) -> TreeNode:
        """
        Embed the clock tree by selecting actual positions for internal nodes

        Args:
            merging_tree: The merging tree structure
            merging_segments: Computed merging segments for all nodes

        Returns:
            Embedded clock tree with actual positions
        """

        def embed_node(node: TreeNode, parent_segment: Optional[MergeObj] = None):
            if node is None:
                return

            if parent_segment is None:
                # Root node: choose center of merging segment
                node_segment = merging_segments[node.name]
                # For root, we can choose any point in the segment, typically the center
                node.position = self._segment_center(node_segment)
            else:
                # Internal node: choose point in merging segment closest to parent
                node_segment = merging_segments[node.name]
                node.position = self._nearest_point_in_segment(
                    node_segment, parent_segment
                )

                # Compute wire length to parent
                if node.parent:
                    node.wire_length = self._manhattan_distance(
                        node.position, node.parent.position
                    )

            # Recursively embed children
            embed_node(node.left, merging_segments[node.name] if node.left else None)
            embed_node(node.right, merging_segments[node.name] if node.right else None)

        embed_node(merging_tree)
        return merging_tree

    def _compute_tree_parameters(self, root: TreeNode):
        """
        Compute delays and other parameters for the entire tree

        Args:
            root: Root node of the clock tree
        """

        def compute_delays(node: TreeNode, parent_delay: float = 0.0):
            if node is None:
                return

            # Compute delay from parent to this node
            if node.parent:
                wire_delay = self._wire_delay(node.wire_length, node.capacitance)
                node.delay = parent_delay + wire_delay
            else:
                node.delay = 0.0  # Root has zero delay

            # Recursively compute for children
            compute_delays(node.left, node.delay)
            compute_delays(node.right, node.delay)

        compute_delays(root)

    def _wire_delay(self, length: float, load_capacitance: float) -> float:
        """
        Compute Elmore delay for a wire segment

        Args:
            length: Wire length
            load_capacitance: Load capacitance at the end of the wire

        Returns:
            Elmore delay
        """
        wire_resistance = self.unit_resistance * length
        wire_capacitance = self.unit_capacitance * length
        # Elmore delay: R_wire * (C_wire/2 + C_load)
        return wire_resistance * (wire_capacitance / 2 + load_capacitance)

    def _wire_delay_per_unit(self, load_capacitance: float) -> float:
        """
        Compute delay per unit length for a wire

        Args:
            load_capacitance: Load capacitance

        Returns:
            Delay per unit length
        """
        return self.unit_resistance * (self.unit_capacitance / 2 + load_capacitance)

    def _wire_capacitance(self, length: float) -> float:
        """
        Compute wire capacitance

        Args:
            length: Wire length

        Returns:
            Wire capacitance
        """
        return self.unit_capacitance * length

    def _extend_segment(self, segment: MergeObj, extra_length: float) -> MergeObj:
        """
        Extend a merging segment to increase wire length

        Args:
            segment: Original merging segment
            extra_length: Amount to extend

        Returns:
            Extended merging segment
        """
        # For simplicity, extend in both x and y directions
        # In practice, this would depend on the segment orientation
        return segment.enlarge_with(int(extra_length / 2))

    def _segment_center(self, segment: MergeObj) -> Point[int, int]:
        """
        Find the center point of a merging segment

        Args:
            segment: Merging segment

        Returns:
            Center point
        """
        # Extract coordinates from the segment's internal Point representation
        x_center = self._get_center(segment.impl.xcoord)
        y_center = self._get_center(segment.impl.ycoord)
        return Point(x_center, y_center)

    def _get_center(self, coord) -> int:
        """
        Get center value from coordinate (handles both int and Interval)

        Args:
            coord: Coordinate value (int or Interval)

        Returns:
            Center value as integer
        """
        if isinstance(coord, Interval):
            return (coord.lb + coord.ub) // 2
        return coord

    def _nearest_point_in_segment(
        self, segment: MergeObj, target_segment: MergeObj
    ) -> Point[int, int]:
        """
        Find the point in segment that is nearest to the target segment

        Args:
            segment: Source segment to find point in
            target_segment: Target segment to get close to

        Returns:
            Nearest point in source segment to target segment
        """
        # For simplicity, use the segment center
        # In a full implementation, this would find the actual nearest point
        return self._segment_center(segment)

    def _manhattan_distance(self, p1: Point, p2: Point) -> float:
        """
        Compute Manhattan distance between two points

        Args:
            p1: First point
            p2: Second point

        Returns:
            Manhattan distance
        """
        return abs(p1.xcoord - p2.xcoord) + abs(p1.ycoord - p2.ycoord)

    def analyze_skew(self, root: TreeNode) -> Dict[str, Any]:
        """
        Analyze clock skew in the constructed tree

        Args:
            root: Root node of the clock tree

        Returns:
            Dictionary with skew analysis results
        """
        sink_delays = []

        def collect_sink_delays(node: TreeNode):
            if node is None:
                return
            if node.left is None and node.right is None:
                sink_delays.append(node.delay)
            collect_sink_delays(node.left)
            collect_sink_delays(node.right)

        collect_sink_delays(root)

        max_delay = max(sink_delays)
        min_delay = min(sink_delays)
        skew = max_delay - min_delay

        return {
            "max_delay": max_delay,
            "min_delay": min_delay,
            "skew": skew,
            "sink_delays": sink_delays,
            "total_wirelength": self._total_wirelength(root),
        }

    def _total_wirelength(self, root: TreeNode) -> float:
        """
        Compute total wirelength of the clock tree

        Args:
            root: Root node of the clock tree

        Returns:
            Total wirelength
        """
        total = 0.0

        def sum_wirelength(node: TreeNode):
            nonlocal total
            if node is None:
                return
            total += node.wire_length
            sum_wirelength(node.left)
            sum_wirelength(node.right)

        sum_wirelength(root)
        return total


def get_tree_statistics(root) -> Dict[str, Any]:
    """
    Extract comprehensive statistics from the clock tree

    Args:
        root: Root node of the clock tree

    Returns:
        Dictionary with tree statistics
    """
    nodes = []
    wires = []
    sinks = []

    def traverse(node, parent=None):
        if not node:
            return

        nodes.append(
            {
                "name": node.name,
                "position": (node.position.xcoord, node.position.ycoord),
                "type": "sink"
                if node.left is None and node.right is None
                else "internal",
                "delay": getattr(node, "delay", 0),
                "capacitance": getattr(node, "capacitance", 0),
            }
        )

        if node.left is None and node.right is None:
            sinks.append(node.name)

        if parent:
            wires.append(
                {
                    "from": parent.name,
                    "to": node.name,
                    "length": getattr(node, "wire_length", 0),
                    "from_pos": (parent.position.xcoord, parent.position.ycoord),
                    "to_pos": (node.position.xcoord, node.position.ycoord),
                }
            )

        traverse(node.left, node)
        traverse(node.right, node)

    traverse(root)

    return {
        "nodes": nodes,
        "wires": wires,
        "sinks": sinks,
        "total_nodes": len(nodes),
        "total_sinks": len(sinks),
        "total_wires": len(wires),
    }


# Example usage and testing
def example_dme_usage():
    """Example demonstrating how to use the DME algorithm"""

    # Create clock sinks
    sinks = [
        Sink("s1", Point(10, 20), 1.0),
        Sink("s2", Point(30, 40), 1.0),
        Sink("s3", Point(50, 10), 1.0),
        Sink("s4", Point(70, 30), 1.0),
        Sink("s5", Point(90, 50), 1.0),
    ]

    # Create DME algorithm instance
    dme = DMEAlgorithm(unit_resistance=0.1, unit_capacitance=0.2)

    # Build clock tree
    clock_tree = dme.build_clock_tree(sinks)

    # Analyze results
    analysis = dme.analyze_skew(clock_tree)

    print("DME Clock Tree Synthesis Results:")
    print(f"Maximum delay: {analysis['max_delay']:.3f}")
    print(f"Minimum delay: {analysis['min_delay']:.3f}")
    print(f"Clock skew: {analysis['skew']:.3f}")
    print(f"Total wirelength: {analysis['total_wirelength']:.3f}")

    return clock_tree, analysis


if __name__ == "__main__":
    # Run example
    clock_tree, analysis = example_dme_usage()
