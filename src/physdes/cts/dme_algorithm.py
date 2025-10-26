"""
Deferred Merge Embedding (DME) Algorithm for Clock Tree Synthesis.

This module provides a comprehensive implementation of the Deferred Merge Embedding (DME)
algorithm, a widely used technique for constructing zero-skew clock trees in VLSI design.
The DME algorithm is known for its efficiency and effectiveness in minimizing clock skew,
a critical factor in high-performance digital circuits.

The implementation leverages the Strategy Pattern for delay calculation, allowing for
pluggable delay models. This design provides the flexibility to switch between different
delay calculation strategies, such as linear and Elmore delay models, without altering
the core algorithm. This modular approach makes it easy to extend the system with new
delay models as needed.

Key components of the module include:
- `Sink`: Represents a clock sink with position and capacitance.
- `TreeNode`: Defines the structure of the clock tree.
- `DelayCalculator`: An abstract base class for delay calculation strategies.
- `LinearDelayCalculator`: A concrete implementation of the linear delay model.
- `ElmoreDelayCalculator`: A concrete implementation of the Elmore delay model.
- `DMEAlgorithm`: The main class that orchestrates the clock tree synthesis process.
"""

import doctest
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from icecream import ic  # type: ignore

from physdes.manhattan_arc import ManhattanArc
from physdes.point import Point


@dataclass
class Sink:
    """Represents a clock sink with position and capacitance

    Examples:
        >>> sink = Sink(name="s1", position=Point(10, 20), capacitance=1.5)
        >>> sink.name
        's1'
        >>> sink.position
        Point(10, 20)
        >>> sink.capacitance
        1.5
        >>> sink = Sink(name="s1", position=Point(Point(10, 20), 20), capacitance=1.5)
        >>> sink.name
        's1'
        >>> sink.position
        Point(Point(10, 20), 20)
        >>> sink.capacitance
        1.5
    """

    name: str
    position: Point
    capacitance: float = 1.0


@dataclass
class TreeNode:
    """Represents a node in the clock tree

    Examples:
        >>> node = TreeNode(name="n1", position=Point(30, 40))
        >>> node.name
        'n1'
        >>> node.position
        Point(30, 40)
        >>> node = TreeNode(name="n1", position=Point(Point(30, 40), 40))
        >>> node.name
        'n1'
        >>> node.position
        Point(Point(30, 40), 40)
    """

    name: str
    position: Point
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None
    parent: Optional["TreeNode"] = None
    wire_length: int = 0
    delay: float = 0.0
    capacitance: float = 0.0
    need_elongation = False


class DelayCalculator(ABC):
    """Abstract base class for delay calculation strategies"""

    @abstractmethod
    def calculate_wire_delay(self, length: int, load_capacitance: float) -> float:
        """Calculate wire delay for given length and load capacitance"""
        pass

    @abstractmethod
    def calculate_wire_delay_per_unit(self, load_capacitance: float) -> float:
        """Calculate delay per unit length for given load capacitance"""
        pass

    @abstractmethod
    def calculate_wire_capacitance(self, length: int) -> float:
        """Calculate wire capacitance for given length"""
        pass

    @abstractmethod
    def calculate_tapping_point(
        self, node_left: TreeNode, node_right: TreeNode, distance: int
    ) -> Tuple[int, float]:
        """Calculate extra length based on skew"""
        pass


class LinearDelayCalculator(DelayCalculator):
    """Linear delay model: delay = k * length"""

    def __init__(self, delay_per_unit: float = 1.0, capacitance_per_unit: float = 1.0):
        """
        Initialize linear delay calculator

        Args:
            delay_per_unit: Delay per unit wire length
            capacitance_per_unit: Capacitance per unit wire length

        Examples:
            >>> calc = LinearDelayCalculator(delay_per_unit=0.5, capacitance_per_unit=0.2)
            >>> calc.delay_per_unit
            0.5
        """
        self.delay_per_unit = delay_per_unit
        self.capacitance_per_unit = capacitance_per_unit

    def calculate_wire_delay(self, length: int, load_capacitance: float) -> float:
        """
        Calculate wire delay using linear model

        Args:
            length: Wire length
            load_capacitance: Load capacitance (ignored in linear model)

        Returns:
            Wire delay

        Examples:
            >>> calc = LinearDelayCalculator(delay_per_unit=0.5)
            >>> calc.calculate_wire_delay(10, 5.0)
            5.0
        """
        return self.delay_per_unit * length

    def calculate_wire_delay_per_unit(self, load_capacitance: float) -> float:
        """
        Calculate delay per unit length

        Args:
            load_capacitance: Load capacitance (ignored in linear model)

        Returns:
            Delay per unit length

        Examples:
            >>> calc = LinearDelayCalculator(delay_per_unit=0.5)
            >>> calc.calculate_wire_delay_per_unit(5.0)
            0.5
        """
        return self.delay_per_unit

    def calculate_wire_capacitance(self, length: int) -> float:
        """
        Calculate wire capacitance

        Args:
            length: Wire length

        Returns:
            Wire capacitance

        Examples:
            >>> calc = LinearDelayCalculator(capacitance_per_unit=0.2)
            >>> calc.calculate_wire_capacitance(10)
            2.0
        """
        return self.capacitance_per_unit * length

    def calculate_tapping_point(
        self, node_left: TreeNode, node_right: TreeNode, distance: int
    ) -> Tuple[int, float]:
        """Calculate extra length based on skew"""
        # Compute required delay balancing
        skew = node_right.delay - node_left.delay
        extend_left = round((skew / self.delay_per_unit + distance) / 2)
        delay_left = node_left.delay + extend_left * self.delay_per_unit
        node_left.wire_length = extend_left
        node_right.wire_length = distance - extend_left
        # delay_right = node_right.delay + (distance - extend_left) * self.delay_per_unit
        if extend_left < 0:
            ic(extend_left)
            node_left.wire_length = 0
            node_right.wire_length = distance - extend_left
            extend_left = 0
            delay_left = node_left.delay
            node_right.need_elongation = True
        elif extend_left > distance:
            ic(extend_left)
            node_right.wire_length = 0
            node_right.wire_length = extend_left
            extend_left = distance
            delay_left = node_right.delay
            node_left.need_elongation = True
        return extend_left, delay_left


class ElmoreDelayCalculator(DelayCalculator):
    """Elmore delay model for RC trees"""

    def __init__(self, unit_resistance: float = 1.0, unit_capacitance: float = 1.0):
        """
        Initialize Elmore delay calculator

        Args:
            unit_resistance: Resistance per unit length
            unit_capacitance: Capacitance per unit length

        Examples:
            >>> calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
            >>> calc.unit_resistance
            0.1
        """
        self.unit_resistance = unit_resistance
        self.unit_capacitance = unit_capacitance

    def calculate_wire_delay(self, length: int, load_capacitance: float) -> float:
        """
        Calculate Elmore delay for a wire segment

        Args:
            length: Wire length
            load_capacitance: Load capacitance at the end of the wire

        Returns:
            Elmore delay

        Examples:
            >>> calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
            >>> calc.calculate_wire_delay(10, 5.0)
            6.0
        """
        wire_resistance = self.unit_resistance * length
        wire_capacitance = self.unit_capacitance * length
        # Elmore delay: R_wire * (C_wire/2 + C_load)
        return wire_resistance * (wire_capacitance / 2 + load_capacitance)

    def calculate_wire_delay_per_unit(self, load_capacitance: float) -> float:
        """
        Calculate Elmore delay per unit length

        Args:
            load_capacitance: Load capacitance

        Returns:
            Delay per unit length

        Examples:
            >>> calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
            >>> calc.calculate_wire_delay_per_unit(5.0)
            0.51
        """
        return self.unit_resistance * (self.unit_capacitance / 2 + load_capacitance)

    def calculate_wire_capacitance(self, length: int) -> float:
        """
        Calculate wire capacitance

        Args:
            length: Wire length

        Returns:
            Wire capacitance

        Examples:
            >>> calc = ElmoreDelayCalculator(unit_capacitance=0.2)
            >>> calc.calculate_wire_capacitance(10)
            2.0
        """
        return self.unit_capacitance * length

    def calculate_tapping_point(
        self, node_left: TreeNode, node_right: TreeNode, distance: int
    ) -> Tuple[int, float]:
        """Calculate extra length based on skew"""
        # Compute required delay balancing
        skew = node_right.delay - node_left.delay
        r = distance * self.unit_resistance
        c = distance * self.unit_capacitance
        z = (skew + r * (node_right.capacitance + c / 2.0)) / (
            r * (c + node_right.capacitance + node_left.capacitance)
        )
        extend_left = round(z * distance)
        r_left = extend_left * self.unit_resistance
        c_left = extend_left * self.unit_capacitance
        delay_left = node_left.delay + r_left * (c_left / 2.0 + node_left.capacitance)
        node_left.wire_length = extend_left
        node_right.wire_length = distance - extend_left
        # delay_right = node_right.delay + (distance - extend_left) * self.delay_per_unit
        if extend_left < 0:
            ic(extend_left)
            node_left.wire_length = 0
            node_right.wire_length = distance - extend_left
            extend_left = 0
            delay_left = node_left.delay
            node_right.need_elongation = True
        elif extend_left > distance:
            ic(extend_left)
            node_right.wire_length = 0
            node_right.wire_length = extend_left
            extend_left = distance
            delay_left = node_right.delay
            node_left.need_elongation = True
        return extend_left, delay_left


class DMEAlgorithm:
    """
    Deferred Merge Embedding (DME) Algorithm for Clock Tree Synthesis
    with configurable delay calculation strategy
    """

    def __init__(self, sinks: List[Sink], delay_calculator: DelayCalculator):
        """
        Initialize DME algorithm with delay calculation strategy

        Args:
            sinks: List of clock sinks with positions and capacitances
            delay_calculator: Strategy for delay calculation

        Examples:
            >>> linear_calc = LinearDelayCalculator(delay_per_unit=0.5)
            >>> sinks = [Sink("s1", Point(10, 20), 1.0)]
            >>> dme = DMEAlgorithm(sinks, delay_calculator=linear_calc)
            >>> isinstance(dme.delay_calculator, LinearDelayCalculator)
            True

            >>> elmore_calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
            >>> dme = DMEAlgorithm(sinks, delay_calculator=elmore_calc)
            >>> isinstance(dme.delay_calculator, ElmoreDelayCalculator)
            True
        """
        if not sinks:
            raise ValueError("No sinks provided")

        self.sinks = sinks
        self.delay_calculator = delay_calculator
        self.node_id = 0

    def build_clock_tree(self) -> TreeNode:
        """
        Build a zero-skew clock tree for the given sinks

        Returns:
            Root node of the clock tree
        """
        # Step 1: Create initial leaf nodes
        nodes = [
            TreeNode(name=s.name, position=s.position, capacitance=s.capacitance)
            for s in self.sinks
        ]

        # Step 2: Build merging tree using balanced bipartition
        merging_tree = self._build_merging_tree(nodes, False)

        # Step 3: Perform bottom-up merging segment computation
        merging_segments = self._compute_merging_segments(merging_tree)

        # Step 4: Perform top-down embedding
        clock_tree = self._embed_tree(merging_tree, merging_segments)

        # Step 5: Compute delays and wire lengths
        self._compute_tree_parameters(clock_tree)

        return clock_tree

    def _build_merging_tree(
        self, nodes: List["TreeNode"], vertical: bool
    ) -> "TreeNode":
        """
        Build a balanced merging tree using recursive bipartition

        Args:
            nodes: List of tree nodes to merge

        Returns:
            Root node of the merging tree
        """
        if len(nodes) == 1:
            return nodes[0]

        # Sort nodes along the appropriate axis (x or y) to facilitate balanced partitioning.
        # This ensures that the division into left and right groups is as even as possible,
        # which is crucial for building a balanced merging tree.
        sorted_nodes = (
            sorted(nodes, key=lambda n: n.position.xcoord)
            if vertical
            else sorted(nodes, key=lambda n: n.position.ycoord)
        )

        # Split the sorted nodes into two balanced groups: left and right.
        # The 'mid' index ensures an approximately equal distribution of nodes
        # between the two child subtrees.
        mid = len(sorted_nodes) // 2
        left_group = sorted_nodes[:mid]
        right_group = sorted_nodes[mid:]

        # Recursively build the left and right subtrees. The 'vertical' parameter is toggled
        # to alternate the sorting axis (x then y, or y then x) at each level of recursion.
        # This ensures that the tree is balanced in both dimensions.
        left_child = self._build_merging_tree(left_group, not vertical)
        right_child = self._build_merging_tree(right_group, not vertical)

        # Create a new parent node for the two subtrees. Its position is temporary
        # and will be determined during the embedding phase. A unique ID is assigned
        # to each new internal node.
        parent = TreeNode(
            name=f"n{self.node_id}",
            position=left_child.position,  # Temporary position
            left=left_child,
            right=right_child,
        )
        self.node_id += 1

        # Assign the newly created parent to its children, establishing the tree structure.
        left_child.parent = parent
        right_child.parent = parent

        return parent

    def _compute_merging_segments(self, root: "TreeNode") -> Dict[str, ManhattanArc]:
        """
        Compute merging segments for all nodes in bottom-up order

        Args:
            root: Root node of the merging tree

        Returns:
            Dictionary mapping node names to their merging segments
        """
        merging_segments = {}

        def compute_segment(node: "TreeNode") -> ManhattanArc:
            if node.left is None and node.right is None:
                # If it's a leaf node (a sink), its merging segment is simply its position.
                # The delay for a leaf node is considered 0.0 at this stage.
                ms = ManhattanArc.from_point(node.position)
                merging_segments[node.name] = ms
                return ms

            # If it's an internal node, recursively compute the merging segments for its children.
            # This bottom-up approach ensures that child segments are computed before parent segments.
            if node.left is None or node.right is None:
                raise ValueError("Internal node must have both left and right children")
            left_ms = compute_segment(node.left)
            right_ms = compute_segment(node.right)

            # Calculate the Manhattan distance between the two child merging segments.
            # This distance represents the minimum possible wire length required to connect them.
            distance = left_ms.min_dist_with(right_ms)
            # ic(distance)

            # Calculate the tapping point and delay for the merged segment using the configured
            # delay calculator strategy. This step is crucial for achieving zero-skew by
            # determining how to balance the delays from the left and right branches.
            (
                extend_left,
                delay_left,
            ) = self.delay_calculator.calculate_tapping_point(
                node.left, node.right, distance
            )
            node.delay = delay_left
            # Merge the left and right segments based on the calculated tapping point.
            # The 'extend_left' parameter dictates how much the left segment needs to be
            # extended to meet the zero-skew requirement.
            merged_segment = left_ms.merge_with(right_ms, extend_left)
            merging_segments[node.name] = merged_segment

            # Update the capacitance of the current node. This includes the capacitances
            # of its children and the capacitance of the wire segment connecting them.
            wire_cap = self.delay_calculator.calculate_wire_capacitance(distance)
            node.capacitance = node.left.capacitance + node.right.capacitance + wire_cap
            return merged_segment

        compute_segment(root)
        return merging_segments

    def _embed_tree(
        self, merging_tree: "TreeNode", merging_segments: Dict[str, ManhattanArc]
    ) -> "TreeNode":
        """
        Embed the clock tree by selecting actual positions for internal nodes

        Args:
            merging_tree: The merging tree structure
            merging_segments: Computed merging segments for all nodes

        Returns:
            Embedded clock tree with actual positions
        """

        def embed_node(
            node: Optional["TreeNode"], parent_segment: Optional[ManhattanArc] = None
        ):
            if node is None:
                return

            if parent_segment is None:
                # If it's the root node (no parent segment), its position is chosen as
                # the upper corner of its merging segment. This is an arbitrary but consistent
                # choice for the root's physical location.
                node_segment = merging_segments[node.name]
                node.position = node_segment.get_upper_corner()
            else:
                # For internal nodes, the actual position is determined by finding the point
                # within its merging segment that is closest to its parent's position.
                # This minimizes the wire length connecting the node to its parent.
                node_segment = merging_segments[node.name]
                # Compute wire length to parent
                if node.parent:
                    node.position = node_segment.nearest_point_to(node.parent.position)
                    node.wire_length = node.position.min_dist_with(node.parent.position)

            # Recursively call embed_node for the left and right children.
            # The merging segment of the current node becomes the 'parent_segment'
            # for its children, guiding their embedding process.
            embed_node(node.left, merging_segments[node.name])
            embed_node(node.right, merging_segments[node.name])

        embed_node(merging_tree)
        return merging_tree

    def _compute_tree_parameters(self, root: "TreeNode"):
        """
        Compute delays and other parameters for the entire tree

        Args:
            root: Root node of the clock tree
        """

        def compute_delays(node: Optional["TreeNode"], parent_delay: float = 0.0):
            if node is None:
                return

            # If the node has a parent, calculate the wire delay from the parent to this node.
            # This calculation uses the configured delay_calculator strategy, taking into
            # account the wire length and the node's capacitance.
            if node.parent:
                wire_delay = self.delay_calculator.calculate_wire_delay(
                    node.wire_length, node.capacitance
                )
                # The total delay to this node is the parent's delay plus the wire delay.
                node.delay = parent_delay + wire_delay
            else:
                # The root node of the clock tree has a zero delay by definition.
                node.delay = 0.0  # Root has zero delay

            # Recursively compute delays for the children, passing the current node's
            # delay as the parent_delay for the next level.
            compute_delays(node.left, node.delay)
            compute_delays(node.right, node.delay)

        compute_delays(root)

    # def _extend_segment(self, segment: ManhattanArc, extra_length: int) -> ManhattanArc:
    #     """
    #     Extend a merging segment to increase wire length

    #     Args:
    #         segment: Original merging segment
    #         extra_length: Amount to extend

    #     Returns:
    #         Extended merging segment
    #     """
    #     # For simplicity, extend in both x and y directions
    #     return segment.enlarge_with(extra_length // 2)

    # def _segment_center(self, segment: ManhattanArc) -> Point[int, int]:
    #     """
    #     Find the center point of a merging segment

    #     Args:
    #         segment: Merging segment

    #     Returns:
    #         Center point
    #     """
    #     x_center = self._get_center(segment.impl.xcoord)
    #     y_center = self._get_center(segment.impl.ycoord)
    #     return Point(x_center, y_center)

    # def _get_center(self, coord: Any) -> int:
    #     """
    #     Get center value from coordinate (handles both int and Interval)

    #     Args:
    #         coord: Coordinate value (int or Interval)

    #     Returns:
    #         Center value as integer

    #     Examples:
    #         >>> dme = DMEAlgorithm(LinearDelayCalculator())
    #         >>> dme._get_center(10)
    #         10
    #         >>> dme._get_center(Interval(10, 20))
    #         15
    #     """
    #     if isinstance(coord, Interval):
    #         return (coord.lb + coord.ub) // 2
    #     return coord

    # def _nearest_point_in_segment(
    #     self, segment: ManhattanArc, target_segment: ManhattanArc
    # ):
    #     """
    #     Find the point in segment that is nearest to the target segment

    #     Args:
    #         segment: Source segment to find point in
    #         target_segment: Target segment to get close to

    #     Returns:
    #         Nearest point in source segment to target segment
    #     """
    #     # For simplicity, use the segment center
    #     # return segment.get_center()
    #     return segment.nearest_point_to(target_segment)

    def analyze_skew(self, root: "TreeNode") -> Dict[str, Any]:
        """
        Analyze clock skew in the constructed tree

        Args:
            root: Root node of the clock tree

        Returns:
            Dictionary with skew analysis results
        """
        sink_delays = []

        def collect_sink_delays(node: Optional["TreeNode"]):
            if node is None:
                return
            if node.left is None and node.right is None:
                sink_delays.append(node.delay)
            if node.left:
                collect_sink_delays(node.left)
            if node.right:
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
            "delay_model": self.delay_calculator.__class__.__name__,
        }

    def _total_wirelength(self, root: "TreeNode") -> int:
        """
        Compute total wirelength of the clock tree

        Args:
            root: Root node of the clock tree

        Returns:
            Total wirelength
        """
        total = 0

        def sum_wirelength(node: Optional["TreeNode"]):
            nonlocal total
            if node is None:
                return
            total += node.wire_length
            if node.left:
                sum_wirelength(node.left)
            if node.right:
                sum_wirelength(node.right)

        sum_wirelength(root)
        return total


def get_tree_statistics(root: "TreeNode") -> Dict[str, Any]:
    """
    Extract comprehensive statistics from the clock tree

    Args:
        root: Root node of the clock tree

    Returns:
        Dictionary with tree statistics

    Examples:
        >>> from physdes.point import Point
        >>> from physdes.cts.dme_algorithm import TreeNode, get_tree_statistics
        >>> s1 = TreeNode(name="s1", position=Point(10, 20))
        >>> s2 = TreeNode(name="s2", position=Point(30, 40))
        >>> root = TreeNode(name="n1", position=Point(20, 30), left=s1, right=s2)
        >>> stats = get_tree_statistics(root)
        >>> stats["total_nodes"]
        3
        >>> stats["total_sinks"]
        2
    """
    nodes = []
    wires = []
    sinks = []

    def traverse(node: Optional["TreeNode"], parent: Optional["TreeNode"] = None):
        if not node:
            return

        nodes.append(
            {
                "name": node.name,
                "position": (node.position.xcoord, node.position.ycoord),
                "type": (
                    "sink" if node.left is None and node.right is None else "internal"
                ),
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
def example_dme_usage() -> Tuple[
    "TreeNode", "TreeNode", Dict[str, Any], Dict[str, Any]
]:
    """Example demonstrating how to use the DME algorithm with different delay models"""

    # Create clock sinks
    sinks = [
        Sink("s1", Point(10, 20), 1.0),
        Sink("s2", Point(30, 40), 1.0),
        Sink("s3", Point(50, 10), 1.0),
        Sink("s4", Point(70, 30), 1.0),
        Sink("s5", Point(90, 50), 1.0),
    ]

    print("=== Linear Delay Model ===")
    linear_calc = LinearDelayCalculator(delay_per_unit=0.5, capacitance_per_unit=0.2)
    dme_linear = DMEAlgorithm(sinks, delay_calculator=linear_calc)
    clock_tree_linear = dme_linear.build_clock_tree()
    analysis_linear = dme_linear.analyze_skew(clock_tree_linear)

    print(f"Delay Model: {analysis_linear['delay_model']}")
    print(f"Maximum delay: {analysis_linear['max_delay']:.3f}")
    print(f"Minimum delay: {analysis_linear['min_delay']:.3f}")
    print(f"Clock skew: {analysis_linear['skew']:.3f}")
    print(f"Total wirelength: {analysis_linear['total_wirelength']:.3f}")

    print("\n=== Elmore Delay Model ===")
    elmore_calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
    dme_elmore = DMEAlgorithm(sinks, delay_calculator=elmore_calc)
    clock_tree_elmore = dme_elmore.build_clock_tree()
    analysis_elmore = dme_elmore.analyze_skew(clock_tree_elmore)

    print(f"Delay Model: {analysis_elmore['delay_model']}")
    print(f"Maximum delay: {analysis_elmore['max_delay']:.3f}")
    print(f"Minimum delay: {analysis_elmore['min_delay']:.3f}")
    print(f"Clock skew: {analysis_elmore['skew']:.3f}")
    print(f"Total wirelength: {analysis_elmore['total_wirelength']:.3f}")

    return clock_tree_linear, clock_tree_elmore, analysis_linear, analysis_elmore


if __name__ == "__main__":
    # Run example
    (
        clock_tree_linear,
        clock_tree_elmore,
        analysis_linear,
        analysis_elmore,
    ) = example_dme_usage()
    doctest.testmod()
