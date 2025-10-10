from typing import List
from .routing_tree import GlobalRoutingTree
from physdes.point import Point

class GlobalRouter:
    def __init__(self, source_position: Point[int, int], terminal_positions: List[Point[int, int]]) -> None:
        self.source_position = source_position
        self.terminal_positions = sorted(terminal_positions, key = lambda pt: source_position.min_dist_with(pt), reverse = True)
        self.tree = GlobalRoutingTree(source_position)

    def route_simple(self) -> None:
        for t in self.terminal_positions:
            self.tree.insert_terminal_node(t)

    def route_with_steiners(self) -> None:
        for t in self.terminal_positions:
            self.tree.insert_terminal_with_steiner(t)
