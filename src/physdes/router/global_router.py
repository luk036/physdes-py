from typing import List
from physdes.router.routing_tree import GlobalRoutingTree
from physdes.point import Point


class GlobalRouter:
    """
    A global router for routing between a source and multiple terminals.
    """

    def __init__(
        self,
        source_position: Point[int, int],
        terminal_positions: List[Point[int, int]],
    ) -> None:
        """
        Initializes the GlobalRouter.

        Args:
            source_position: The starting point for the routing.
            terminal_positions: A list of terminal points to be routed to.

        Examples:
            >>> from physdes.point import Point
            >>> source = Point(0, 0)
            >>> terminals = [Point(10, 0), Point(1, 0), Point(5, 0)]
            >>> router = GlobalRouter(source, terminals)
            >>> router.terminal_positions
            [Point(10, 0), Point(5, 0), Point(1, 0)]
        """
        self.source_position = source_position
        self.terminal_positions = sorted(
            terminal_positions,
            key=lambda pt: source_position.min_dist_with(pt),
            reverse=True,
        )
        self.tree = GlobalRoutingTree(source_position)
        self.worst_wirelength = source_position.min_dist_with(terminal_positions[0])

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
        """
        for t in self.terminal_positions:
            self.tree.insert_terminal_with_steiner(t)

    def route_with_constraints(self, alpha=1.0) -> None:
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
        """
        allowed_wirelength = round(self.worst_wirelength * alpha)
        for t in self.terminal_positions:
            self.tree.insert_terminal_with_constraints(t, allowed_wirelength)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
