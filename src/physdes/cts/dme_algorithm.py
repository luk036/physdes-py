"""
Deferred Merge Embedding (DME) Algorithm for Clock Tree Synthesis.

This module provides a comprehensive implementation of the Deferred Merge Embedding (DME)
algorithm, a widely used technique for constructing prescribed-skew (not necessarily zero) clock trees in VLSI design.
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
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from physdes.manhattan_arc import ManhattanArc
from physdes.manhattan_arc_3d import ManhattanArc3D
from physdes.point import Point
from physdes.skeleton import _logger


class Sink:
    """Represents a clock sink with position and capacitance"""

    __slots__ = ("name", "position", "capacitance")

    def __init__(self, name: str, position: Point, capacitance: float = 1.0) -> None:
        self.name = name
        self.position = position
        self.capacitance = capacitance


class TreeNode:
    """Represents a node in the clock tree"""

    __slots__ = (
        "name",
        "position",
        "left",
        "right",
        "parent",
        "segment",
        "wire_length",
        "delay",
        "capacitance",
        "need_elongation",
    )

    def __init__(
        self,
        name: str,
        position: Point,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
        parent: Optional["TreeNode"] = None,
        wire_length: int = 0,
        delay: float = 0.0,
        capacitance: float = 0.0,
    ) -> None:
        self.name = name
        self.position = position
        self.left = left
        self.right = right
        self.parent = parent
        self.segment = None  # merging segment, set during DME
        self.wire_length = wire_length
        self.delay = delay
        self.capacitance = capacitance
        self.need_elongation = False


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
        self,
        node_left: TreeNode,
        node_right: TreeNode,
        distance: int,
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
        self,
        node_left: TreeNode,
        node_right: TreeNode,
        distance: int,
    ) -> Tuple[int, float]:
        """Calculate extra length based on skew"""
        if distance == 0:
            return 0, max(node_left.delay, node_right.delay)

        # Compute required delay balancing
        skew = node_right.delay - node_left.delay
        extend_left = round((skew / self.delay_per_unit + distance) / 2)
        delay_left = node_left.delay + extend_left * self.delay_per_unit

        extend_left, delay_left = self._handle_boundary_conditions(
            extend_left, distance, node_left, node_right, delay_left
        )
        return extend_left, delay_left

    def _handle_boundary_conditions(
        self,
        extend_left: int,
        distance: int,
        node_left: TreeNode,
        node_right: TreeNode,
        delay_left: float,
    ) -> Tuple[int, float]:
        if extend_left < 0:
            node_left.wire_length = 0
            node_right.wire_length = distance
            extend_left = 0
            delay_left = node_left.delay
            node_right.need_elongation = True
        elif extend_left > distance:
            node_right.wire_length = 0
            node_left.wire_length = distance
            extend_left = distance
            delay_left = node_right.delay
            node_left.need_elongation = True
        else:
            node_left.wire_length = extend_left
            node_right.wire_length = distance - extend_left

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
        self,
        node_left: TreeNode,
        node_right: TreeNode,
        distance: int,
    ) -> Tuple[int, float]:
        """Calculate extra length based on skew"""
        if distance == 0:
            return 0, max(node_left.delay, node_right.delay)

        # Compute required delay balancing
        skew = node_right.delay - node_left.delay
        resistance = distance * self.unit_resistance
        capacitance = distance * self.unit_capacitance
        tapping_pt = (
            skew + resistance * (node_right.capacitance + capacitance / 2.0)
        ) / (
            resistance * (capacitance + node_right.capacitance + node_left.capacitance)
        )
        extend_left = round(tapping_pt * distance)
        res_left = extend_left * self.unit_resistance
        cap_left = extend_left * self.unit_capacitance
        delay_left = node_left.delay + res_left * (
            cap_left / 2.0 + node_left.capacitance
        )

        extend_left, delay_left = self._handle_boundary_conditions(
            extend_left, distance, node_left, node_right, delay_left
        )
        return extend_left, delay_left

    def _handle_boundary_conditions(
        self,
        extend_left: int,
        distance: int,
        node_left: TreeNode,
        node_right: TreeNode,
        delay_left: float,
    ) -> Tuple[int, float]:
        if extend_left < 0:
            node_left.wire_length = 0
            node_right.wire_length = distance
            extend_left = 0
            delay_left = node_left.delay
            node_right.need_elongation = True
            _logger.debug(
                "Warning: Right node needs elongation: extend_left < 0  => extend_left set to 0"
            )
        elif extend_left > distance:
            node_right.wire_length = 0
            node_left.wire_length = distance
            extend_left = distance
            delay_left = node_right.delay
            node_left.need_elongation = True
            _logger.debug(
                "Warning: Left node needs elongation: extend_left > distance => extend_left set to distance"
            )
        else:
            node_left.wire_length = extend_left
            node_right.wire_length = distance - extend_left

        return extend_left, delay_left


class DMEAlgorithm:
    """
    Deferred Merge Embedding (DME) Algorithm for Clock Tree Synthesis
    with configurable delay calculation strategy

    .. svgbob::
       :align: center

                . v
               .
              .
             .
            . L ______ R
           .          .
          .           .
         ._____________

    This diagram represents a single step in the **bottom-up merging phase** of the DME algorithm. Here's what each part signifies:

    *   **L and R**: These represent two **subtrees** that have already been constructed.
        They could be individual sinks (leaf nodes) or more complex subtrees that have
        been built in previous steps. In the context of the diagram, they are the
        "children" being merged.

    *   **The Boxes Around L and R**: These boxes represent the **merging segments** (MS)
        of the left and right subtrees, respectively. A merging segment is a set of
        all possible locations where a new parent node can be placed to connect the
        children while satisfying the prescribed-skew (not necessarily zero) constraint.

    *   **v**: This is the **new parent node** being created to merge the left and right subtrees. Its exact position is not yet determined; it will be chosen from the new merging segment.

    *   **The Dashed Lines**: These lines show the **projection** of the child merging segments
        to form the new merging segment for the parent node `v`. The new merging segment
        is the set of all points that are equidistant (in terms of delay) from the
        child merging segments.

    **How it Relates to the DME Algorithm**

    The DME algorithm works in two main phases:

    1.  **Bottom-Up Merging (Construction of Merging Segments)**:
        *   The algorithm starts with the individual sinks (leaf nodes) of the clock tree.
        *   It iteratively merges the two closest subtrees (initially, these are just sinks).
        *   For each merge, it computes a **new merging segment** for the parent node. This is
        where the `svgbob` diagram comes in. The new merging segment is calculated based
        on the merging segments of the two children being merged.
        *   This process continues until all subtrees have been merged into a single root node.

    2.  **Top-Down Embedding (Placement of Internal Nodes)**:
        *   Once the merging segments for all nodes have been computed, the algorithm works its way down from the root.
        *   It **chooses a specific physical location** for each internal node from its pre-computed merging segment.
        *   The choice of location is typically made to minimize wire length or other optimization objectives.

    **In the Context of the Code**

    *   `_build_merging_tree`: This function builds the initial tree structure by recursively partitioning the sinks.
    *   `_compute_merging_segments`: This is the core of the bottom-up phase. It traverses the
        tree from the leaves to the root, and for each internal node, it computes its
        merging segment based on its children's segments. This is where the logic represented
        by the `svgbob` diagram is implemented.
    *   `_embed_tree`: This function performs the top-down embedding, selecting the final positions for the internal nodes.

    By adding this `svgbob` diagram, the documentation provides a quick visual reference that helps
        users understand the fundamental concept of how merging segments are constructed in the
        DME algorithm, making the code easier to grasp.

    Examples:
        >>> from physdes.point import Point
        >>> from physdes.cts.dme_algorithm import Sink, DMEAlgorithm, LinearDelayCalculator
        >>> sinks = [Sink("s1", Point(0, 0), 1.0), Sink("s2", Point(10, 0), 1.0)]
        >>> calc = LinearDelayCalculator()
        >>> dme = DMEAlgorithm(sinks, delay_calculator=calc, source=Point(5,0))
        >>> tree = dme.build_clock_tree()
        >>> analysis = dme.analyze_skew(tree)
        >>> analysis['skew']
        0.0
        >>> analysis['total_wirelength']
        10
        >>> tree.position
        Point(5, 0)
        >>> tree.left.position
        Point(0, 0)
        >>> tree.right.position
        Point(10, 0)
        >>> round(tree.left.delay, 2)
        5.0
        >>> round(tree.right.delay, 2)
        5.0
    """

    MA_TYPE: Union[Type[ManhattanArc], Type[ManhattanArc3D]]

    def __init__(
        self,
        sinks: List[Sink],
        delay_calculator: DelayCalculator,
        source: Optional[Point] = None,
    ):
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
        if isinstance(sinks[0].position.xcoord, Point):  # 3D
            self.MA_TYPE = ManhattanArc3D
        else:
            self.MA_TYPE = ManhattanArc
        self.source = source

    def build_clock_tree(self) -> TreeNode:
        """
        Build a prescribed-skew (not necessarily zero) clock tree for the given sinks

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
        self._compute_merging_segments(merging_tree)

        # Step 4: Perform top-down embedding
        clock_tree = self._embed_tree(merging_tree)

        # Step 5: Compute delays and wire lengths
        self._compute_tree_parameters(clock_tree)

        return clock_tree

    def _build_merging_tree(
        self,
        nodes: List["TreeNode"],
        vertical: bool,
        lo: int = 0,
        hi: Optional[int] = None,
    ) -> "TreeNode":
        """
        Build a balanced merging tree using recursive bipartition

        Args:
            nodes: List of tree nodes to merge (pre-sorted externally)
            vertical: Sort axis toggle for balanced partition
            lo: Start index in the nodes list (default 0)
            hi: End index (exclusive) in the nodes list (default len(nodes))

        Returns:
            Root node of the merging tree
        """
        if hi is None:
            nodes.sort(
                key=lambda n: n.position.ycoord
            )  # initial sort by y
            hi = len(nodes)

        count = hi - lo
        if count == 1:
            return nodes[lo]
        if count == 0:
            raise ValueError("Empty node range")

        # Partition at midpoint for balanced tree
        mid = lo + count // 2

        # Reorder so left half < right half along the current axis
        key_fn = (lambda n: n.position.xcoord) if vertical else (lambda n: n.position.ycoord)
        nodes[lo:hi] = sorted(nodes[lo:hi], key=key_fn)

        left_child = self._build_merging_tree(nodes, not vertical, lo, mid)
        right_child = self._build_merging_tree(nodes, not vertical, mid, hi)

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

    def _compute_merging_segments(self, root: "TreeNode") -> None:
        """
        Compute merging segments for all nodes in bottom-up order,
        storing each segment directly on the node via ``.segment``.

        Args:
            root: Root node of the merging tree
        """

        def compute_segment(
            node: "TreeNode",
        ) -> "ManhattanArc[Any, Any] | ManhattanArc3D":
            if node.left is None and node.right is None:
                manhattan_segment = self.MA_TYPE.from_point(node.position)
                node.segment = manhattan_segment
                return manhattan_segment

            if node.left is None or node.right is None:
                raise ValueError("Internal node must have both left and right children")
            left_ms = compute_segment(node.left)
            right_ms = compute_segment(node.right)

            distance = left_ms.min_dist_with(right_ms)  # type: ignore[arg-type]

            (
                extend_left,
                delay_left,
            ) = self.delay_calculator.calculate_tapping_point(
                node.left, node.right, distance
            )
            node.delay = delay_left
            merged_segment = left_ms.merge_with(right_ms, extend_left)  # type: ignore[arg-type]
            node.segment = merged_segment

            wire_cap = self.delay_calculator.calculate_wire_capacitance(distance)
            node.capacitance = node.left.capacitance + node.right.capacitance + wire_cap
            return merged_segment

        compute_segment(root)

    def _embed_tree(self, merging_tree: "TreeNode") -> "TreeNode":
        """
        Embed the clock tree by selecting actual positions for internal nodes.
        Uses ``node.segment`` set during :meth:`_compute_merging_segments`.

        Args:
            merging_tree: The merging tree structure

        Returns:
            Embedded clock tree with actual positions
        """

        def embed_node(
            node: Optional["TreeNode"],
            parent_segment: Optional[Any] = None,
        ) -> None:
            if node is None:
                return

            if parent_segment is None:
                node_segment = node.segment
                if self.source is None:
                    node.position = node_segment.get_upper_corner()
                else:
                    node.position = node_segment.nearest_point_to(self.source)
            else:
                node_segment = node.segment
                if node.parent:
                    node.position = node_segment.nearest_point_to(node.parent.position)
                    node.wire_length = node.position.min_dist_with(node.parent.position)

            embed_node(node.left, node.segment)
            embed_node(node.right, node.segment)

        embed_node(merging_tree)
        return merging_tree

    def _compute_tree_parameters(self, root: "TreeNode") -> None:
        """
        Compute delays and other parameters for the entire tree

        Args:
            root: Root node of the clock tree
        """

        def compute_delays(
            node: Optional["TreeNode"], parent_delay: float = 0.0
        ) -> None:
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

    def analyze_skew(self, root: "TreeNode") -> Dict[str, Any]:
        """
        Analyze clock skew in the constructed tree

        Args:
            root: Root node of the clock tree

        Returns:
            Dictionary with skew analysis results
        """
        min_delay = float("inf")
        max_delay = float("-inf")
        sink_delays: List[float] = []

        def traverse(node: Optional["TreeNode"]) -> None:
            nonlocal min_delay, max_delay
            if node is None:
                return
            if node.left is None and node.right is None:
                d = node.delay
                sink_delays.append(d)
                if d < min_delay:
                    min_delay = d
                if d > max_delay:
                    max_delay = d
            if node.left:
                traverse(node.left)
            if node.right:
                traverse(node.right)

        traverse(root)
        if min_delay == float("inf"):
            min_delay = max_delay = 0.0
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

        def sum_wirelength(node: Optional["TreeNode"]) -> None:
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

    def traverse(
        node: Optional["TreeNode"], parent: Optional["TreeNode"] = None
    ) -> None:
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
def example_dme_usage() -> (
    Tuple["TreeNode", "TreeNode", Dict[str, Any], Dict[str, Any]]
):
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
