"""
Global Router for VLSI Physical Design.

This module provides a global router that offers multiple strategies for routing between a
source and multiple terminals. The global router is a key component in the VLSI physical
design flow, responsible for finding paths for interconnects while considering various
constraints such as wirelength and timing.

The `GlobalRouter` class implements several routing algorithms, each tailored for different
optimization goals:
- `route_simple()`: A basic approach that connects terminals directly to the nearest
  point in the routing tree.
- `route_with_steiners()`: A more advanced technique that inserts Steiner points to
  minimize wirelength.
- `route_with_constraints()`: A performance-driven strategy that considers both wirelength
  and timing constraints.

This modular design allows users to choose the most appropriate routing strategy for their
specific needs, providing a flexible and powerful tool for global routing tasks.
"""

from typing import List, Optional

from physdes.point import Point
from physdes.router.routing_tree import GlobalRoutingTree


class GlobalRouter:
    """
    A global router for routing between a source and multiple terminals.
    """

    def __init__(
        self,
        source_position: Point,
        terminal_positions: List[Point],
        keepouts: Optional[List[Point]] = None,
    ) -> None:
        """
        Initializes the GlobalRouter.

        Args:
            source_position: The starting point for the routing.
            terminal_positions: A list of terminal points to be routed to.
            keepouts: A list of rectangular regions to avoid during routing.

        Examples:
            >>> from physdes.point import Point
            >>> source = Point(0, 0)
            >>> terminals = [Point(10, 0), Point(1, 0), Point(5, 0)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.terminal_positions
            [Point(10, 0), Point(5, 0), Point(1, 0)]
            >>> source = Point(Point(0, 0), 0)
            >>> terminals = [Point(Point(10, 1), 0), Point(Point(1, 2), 0), Point(Point(5, 0), 0)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.terminal_positions
            [Point(Point(10, 1), 0), Point(Point(5, 0), 0), Point(Point(1, 2), 0)]
            >>> from physdes.interval import Interval
            >>> keepouts = [Point(Interval(2, 4), Interval(2, 4))]
            >>> router = GlobalRouter(source, terminals, keepouts)
            >>> router.keepouts
            [Point(Interval(2, 4), Interval(2, 4))]
        """
        self.source_position = source_position
        """The starting point for the routing."""
        self.terminal_positions = sorted(
            terminal_positions,
            key=lambda t: (
                -source_position.min_dist_with(t),  # Negative for descending order
                source_position.hull_with(t).measure(),  # Negative for descending order
            ),
        )
        """A list of terminal points to be routed to, sorted by distance from the source."""
        self.tree = GlobalRoutingTree(source_position)
        """The routing tree, which is built up as the routing progresses."""
        self.worst_wirelength = source_position.min_dist_with(
            self.terminal_positions[0]
        )
        """The wirelength of the longest connection from the source to a terminal."""
        self.keepouts = keepouts

    def route_simple(self) -> None:
        """
        Performs a simple routing by connecting terminals directly to the nearest node in the tree.

        Examples:
            >>> from physdes.point import Point
            >>> source = Point(0, 0)
            >>> terminals = [Point(1, 1), Point(2, 2)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.route_simple()
            >>> router.tree.calculate_wirelength()
            6
            >>> source = Point(Point(0, 0), 0)
            >>> terminals = [Point(Point(1, 1), 1), Point(Point(2, 0), 2)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.route_simple()
            >>> router.tree.calculate_wirelength()
            7
        """
        for t in self.terminal_positions:
            self.tree.insert_terminal_node(t)

    def route_with_steiners(self) -> None:
        """
        Performs wirelength-driven routing by inserting Steiner points to reduce wire length.

        Examples:
            >>> from physdes.point import Point
            >>> source = Point(0, 0)
            >>> terminals = [Point(1, 1), Point(2, 2)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.route_with_steiners()
            >>> router.tree.calculate_wirelength()
            4
            >>> source = Point(Point(0, 0), 0)
            >>> terminals = [Point(Point(1, 1), 1), Point(Point(2, 0), 2)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.route_with_steiners()
            >>> router.tree.calculate_wirelength()
            5
        """
        for t in self.terminal_positions:
            self.tree.insert_terminal_with_steiner(t, self.keepouts)

    def route_with_constraints(self, alpha: float = 1.0) -> None:
        """
        Performance-driven routing by inserting Steiner points to reduce wire length.

        Examples:
            >>> from physdes.point import Point
            >>> source = Point(0, 0)
            >>> terminals = [Point(1, 1), Point(2, 2)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.route_with_constraints()
            >>> router.tree.calculate_wirelength()
            4
            >>> source = Point(Point(0, 0), 0)
            >>> terminals = [Point(Point(1, 1), 1), Point(Point(2, 0), 2)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.route_with_constraints()
            >>> router.tree.calculate_wirelength()
            5
        """
        allowed_wirelength = round(self.worst_wirelength * alpha)
        for t in self.terminal_positions:
            self.tree.insert_terminal_with_constraints(
                t, allowed_wirelength, self.keepouts
            )
