import heapq
import numpy as np
from typing import List, Tuple, Dict, Set
from collections import defaultdict, deque


class SteinerForest:
    """
    Solves the Steiner Forest Problem on a grid graph using the Primal-Dual algorithm.
    The Steiner Forest Problem: Given a graph and pairs of terminal nodes,
    find a minimum-cost subgraph that connects each terminal pair.

    .. svgbob::

          Grid               Steiner Forest
        .---.---.---.        .---.---.---.
        | S |   | T |        | S o---*---o T |
        '---'---'---'        '---'---|---'---'
        |   |   |   |        |   |   |   |
        '---'---'---'        '---'---'---'---'
        | S |   | T |        | S o---*---o T |
        '---'---'---'        '---'---'---'---'

    The algorithm works by iteratively finding shortest paths between active
    terminal components and adding edges to the forest until all pairs are connected.

    .. svgbob::

                +--<---o
                |
                *-------->---o
                |
         o--->--+

                     +-o
                     |
                     v       o
                     |       |
         o---<-------*--->---+

    """

    def __init__(
        self, grid_size: Tuple[int, int], obstacles: List[Tuple[int, int]] = None
    ):
        """
        Initialize the grid graph.

        Args:
            grid_size: (rows, cols) dimensions of the grid
            obstacles: List of (row, col) positions that are blocked
        """
        self.rows, self.cols = grid_size
        self.obstacles = set(obstacles) if obstacles else set()
        self.edges = []
        self.edge_costs = {}
        self.terminal_pairs = []

        # Build the grid graph
        self._build_grid_graph()

    def _build_grid_graph(self):
        """Build the grid graph with edges between adjacent cells."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) in self.obstacles:
                    continue

                current_node = i * self.cols + j

                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if (
                        0 <= ni < self.rows
                        and 0 <= nj < self.cols
                        and (ni, nj) not in self.obstacles
                    ):
                        neighbor_node = ni * self.cols + nj
                        if current_node < neighbor_node:  # Avoid duplicate edges
                            edge_id = len(self.edges)
                            self.edges.append((current_node, neighbor_node))
                            # Use Euclidean distance as cost (can be modified)
                            cost = np.sqrt((i - ni) ** 2 + (j - nj) ** 2)
                            self.edge_costs[edge_id] = cost

    def add_terminal_pair(self, start: Tuple[int, int], end: Tuple[int, int]):
        """
        Add a terminal pair that needs to be connected.

        Args:
            start: (row, col) of starting terminal
            end: (row, col) of ending terminal
        """
        start_node = start[0] * self.cols + start[1]
        end_node = end[0] * self.cols + end[1]
        self.terminal_pairs.append((start_node, end_node))

    def _dijkstra(
        self, source: int, component_mapping: Dict[int, int]
    ) -> Tuple[Dict[int, float], Dict[int, int]]:
        """
        Dijkstra's algorithm to find shortest paths from source to all nodes.

        Returns:
            dist: Dictionary of distances from source
            prev: Dictionary of previous nodes for path reconstruction
        """
        dist = {node: float("inf") for node in range(self.rows * self.cols)}
        prev = {node: -1 for node in range(self.rows * self.cols)}
        dist[source] = 0

        pq = [(0, source)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_dist > dist[current_node]:
                continue

            # Get neighbors
            i, j = current_node // self.cols, current_node % self.cols
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if (
                    0 <= ni < self.rows
                    and 0 <= nj < self.cols
                    and (ni, nj) not in self.obstacles
                ):
                    neighbor = ni * self.cols + nj

                    # Find edge cost
                    edge_cost = 1.0  # Default cost
                    for edge_id, (u, v) in enumerate(self.edges):
                        if (u == current_node and v == neighbor) or (
                            u == neighbor and v == current_node
                        ):
                            edge_cost = self.edge_costs[edge_id]
                            break

                    new_dist = current_dist + edge_cost

                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        prev[neighbor] = current_node
                        heapq.heappush(pq, (new_dist, neighbor))

        return dist, prev

    def primal_dual_algorithm(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Primal-Dual algorithm for Steiner Forest.

        Returns:
            total_cost: Total cost of the Steiner forest
            selected_edges: List of selected edges in (node1, node2) format
        """
        # Initialize
        F = set()  # Selected edges
        y = defaultdict(float)  # Dual variables for terminal pairs
        components = {}  # Component mapping for each node
        active_pairs = set(range(len(self.terminal_pairs)))

        # Initialize each node in its own component
        for node in range(self.rows * self.cols):
            if (node // self.cols, node % self.cols) not in self.obstacles:
                components[node] = node

        while active_pairs:
            # Find the minimum distance between components for each active pair
            min_distances = {}
            paths = {}

            for pair_idx in active_pairs:
                s, t = self.terminal_pairs[pair_idx]

                if components[s] == components[t]:
                    active_pairs.remove(pair_idx)
                    continue

                # Run Dijkstra from s
                dist, prev = self._dijkstra(s, components)

                if dist[t] < float("inf"):
                    min_distances[pair_idx] = dist[t]
                    paths[pair_idx] = prev

            if not min_distances:
                break

            # Find the pair with minimum distance
            min_pair = min(min_distances.keys(), key=lambda x: min_distances[x])
            epsilon = min_distances[min_pair]

            # Update dual variables
            for pair_idx in active_pairs:
                y[pair_idx] += epsilon

            # Add edges along the path to F
            s, t = self.terminal_pairs[min_pair]
            path_edges = self._get_path_edges(paths[min_pair], s, t)
            F.update(path_edges)

            # Update components (merge along the path)
            self._update_components(F, components)

            # Remove connected pairs from active set
            for pair_idx in list(active_pairs):
                s, t = self.terminal_pairs[pair_idx]
                if components[s] == components[t]:
                    active_pairs.remove(pair_idx)

        # Calculate total cost
        total_cost = sum(self.edge_costs[edge_id] for edge_id in F)

        # Convert edge IDs to node pairs
        selected_edges = [self.edges[edge_id] for edge_id in F]

        return total_cost, selected_edges

    def _get_path_edges(self, prev: Dict[int, int], start: int, end: int) -> Set[int]:
        """Get all edges along the path from start to end."""
        path_edges = set()
        current = end

        while current != start and prev[current] != -1:
            # Find the edge between current and prev[current]
            for edge_id, (u, v) in enumerate(self.edges):
                if (u == current and v == prev[current]) or (
                    u == prev[current] and v == current
                ):
                    path_edges.add(edge_id)
                    break
            current = prev[current]

        return path_edges

    def _update_components(self, selected_edges: Set[int], components: Dict[int, int]):
        """Update component mapping based on selected edges using BFS."""
        # Build graph from selected edges
        graph = defaultdict(list)
        for edge_id in selected_edges:
            u, v = self.edges[edge_id]
            graph[u].append(v)
            graph[v].append(u)

        # Find connected components
        visited = set()
        component_id = 0

        for node in graph:
            if node not in visited:
                # BFS to find all nodes in this component
                queue = deque([node])
                visited.add(node)
                components[node] = component_id

                while queue:
                    current = queue.popleft()
                    for neighbor in graph[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            components[neighbor] = component_id
                            queue.append(neighbor)

                component_id += 1

        # Update components for isolated nodes
        for node in range(self.rows * self.cols):
            if (node // self.cols, node % self.cols) not in self.obstacles:
                if node not in components:
                    components[node] = component_id
                    component_id += 1

    def visualize_solution(self, selected_edges: List[Tuple[int, int]]):
        """Visualize the grid with obstacles, terminals, and solution."""
        grid = [["." for _ in range(self.cols)] for _ in range(self.rows)]

        # Mark obstacles
        for i, j in self.obstacles:
            grid[i][j] = "#"

        # Mark terminals
        terminal_nodes = set()
        for s, t in self.terminal_pairs:
            si, sj = s // self.cols, s % self.cols
            ti, tj = t // self.cols, t % self.cols
            grid[si][sj] = "S"
            grid[ti][tj] = "T"
            terminal_nodes.add(s)
            terminal_nodes.add(t)

        # Mark edges in solution
        set(selected_edges)
        for u, v in selected_edges:
            ui, uj = u // self.cols, u % self.cols
            vi, vj = v // self.cols, v % self.cols

            # Mark horizontal edges
            if ui == vi:
                min_j, max_j = min(uj, vj), max(uj, vj)
                for j in range(min_j, max_j + 1):
                    if grid[ui][j] == ".":
                        grid[ui][j] = "-"
            # Mark vertical edges
            elif uj == vj:
                min_i, max_i = min(ui, vi), max(ui, vi)
                for i in range(min_i, max_i + 1):
                    if grid[i][uj] == ".":
                        grid[i][uj] = "|"

        # Print the grid
        print("Steiner Forest Solution:")
        for row in grid:
            print(" ".join(row))


# Example usage and test cases
def main():
    print("Steiner Forest Problem on Grid Graph")
    print("=" * 50)

    # Test Case 1: Simple 4x4 grid
    print("\nTest Case 1: 4x4 Grid")
    sf1 = SteinerForest((4, 4))
    sf1.add_terminal_pair((0, 0), (3, 3))
    sf1.add_terminal_pair((0, 3), (3, 0))

    cost1, edges1 = sf1.primal_dual_algorithm()
    print(f"Total cost: {cost1:.2f}")
    print(f"Number of edges in solution: {len(edges1)}")
    sf1.visualize_solution(edges1)

    # Test Case 2: Grid with obstacles
    print("\nTest Case 2: 5x5 Grid with Obstacles")
    obstacles = [(1, 1), (1, 2), (2, 1), (3, 3)]
    sf2 = SteinerForest((5, 5), obstacles)
    sf2.add_terminal_pair((0, 0), (4, 4))
    sf2.add_terminal_pair((0, 4), (4, 0))
    sf2.add_terminal_pair((2, 2), (2, 4))

    cost2, edges2 = sf2.primal_dual_algorithm()
    print(f"Total cost: {cost2:.2f}")
    print(f"Number of edges in solution: {len(edges2)}")
    sf2.visualize_solution(edges2)

    # Test Case 3: Larger grid with multiple pairs
    print("\nTest Case 3: 6x6 Grid with Multiple Terminal Pairs")
    sf3 = SteinerForest((6, 6))
    sf3.add_terminal_pair((0, 0), (5, 5))
    sf3.add_terminal_pair((0, 5), (5, 0))
    sf3.add_terminal_pair((2, 2), (3, 3))
    sf3.add_terminal_pair((1, 4), (4, 1))

    cost3, edges3 = sf3.primal_dual_algorithm()
    print(f"Total cost: {cost3:.2f}")
    print(f"Number of edges in solution: {len(edges3)}")
    sf3.visualize_solution(edges3)


if __name__ == "__main__":
    main()
