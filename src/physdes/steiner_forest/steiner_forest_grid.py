"""
Steiner-forest construction on grid graphs using a primal-dual approximation.

Provides ``UnionFind`` (disjoint-set) and ``steiner_forest_grid`` which grows
paths from active terminal components until all required pairs are connected,
then prunes redundant edges via reverse delete.
"""

import collections
from typing import Dict, List, Set, Tuple


class UnionFind:
    """
    A Union-Find (Disjoint Set Union) data structure with path compression and union by rank.

    This implementation supports efficient union and find operations for managing
    connected components, commonly used in graph algorithms like Kruskal's MST.

    Examples:
        >>> uf = UnionFind(10)
        >>> uf.union(1, 2)
        True
        >>> uf.union(2, 3)
        True
        >>> uf.find(1) == uf.find(3)
        True
        >>> uf.union(1, 3)
        False
    """

    def __init__(self, size: int):
        """
        Initialize the Union-Find structure.

        :param size: The number of elements in the set.
        :type size: int
        """
        self.parent: List[int] = list(range(size))
        self.rank: List[int] = [0] * size

    def find(self, idx: int) -> int:
        """
        Find the representative (root) of the set containing idx.

        Uses iterative path compression to flatten the tree structure for
        faster future lookups.

        :param idx: The index to find.
        :type idx: int
        :return: The representative (root) of the set.
        :rtype: int
        """
        parent = self.parent
        root = idx
        while parent[root] != root:
            root = parent[root]
        while parent[idx] != root:
            parent[idx], idx = root, parent[idx]
        return root

    def union(self, idx1: int, idx2: int) -> bool:
        """
        Unite the sets containing idx1 and idx2.

        Uses union by rank to keep the tree balanced.

        :param idx1: First index.
        :type idx1: int
        :param idx2: Second index.
        :type idx2: int
        :return: True if a union was performed, False if already in same set.
        :rtype: bool
        """
        pp = self.find(idx1)
        pq = self.find(idx2)
        if pp == pq:
            return False
        if self.rank[pp] < self.rank[pq]:
            self.parent[pp] = pq
        elif self.rank[pp] > self.rank[pq]:
            self.parent[pq] = pp
        else:
            self.parent[pq] = pp
            self.rank[pp] += 1
        return True


def steiner_forest_grid(
    height: int, width: int, pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]]
) -> Tuple[List[Tuple[int, int, float]], float, Set[int], Set[int], Set[int]]:
    """
    Computes an approximate Steiner forest on a grid graph.

    The algorithm is based on the primal-dual approach for the Steiner
    network problem. It iteratively pays for edges until all terminal
    pairs are connected.

    The following diagram illustrates the concept of a Steiner tree,
    where 'o' represents terminals and '*' represents Steiner points.

    .. svgbob::

         +--.----------o
         |   `.        |
         |     `.      |
         |       `.    |
         o---------`---+

    In our case, we are looking for a Steiner forest, which is a collection
    of Steiner trees connecting specified pairs of terminals.

    .. svgbob::

          Grid               Steiner Forest
        .---.---.---.        .---.---.---.
        | S |   | T |        | S o---*---o T |
        '---'---'---'        '---'---|---'---'
        |   |   |   |        |   |   |   |
        '---'---'---'        '---'---'---'---'
        | S |   | T |        | S o---*---o T |
        '---'---'---'        '---'---'---'---'

    The algorithm works by "growing" paths from terminals. Each active
    component (a connected component containing at least one terminal
    that needs to be connected to a terminal in another component)
    contributes to the cost of edges.

    .. svgbob::

                +--<---o
                |
                *-------->---o
                |
         o--->--+

    When the cost paid for an edge equals its weight, the edge is
    added to the forest.

    .. svgbob::

                     +-o
                     |
                     v       o
                     |       |
         o---<-------*--->---+

    The following diagrams illustrate the concept in 3D as well.

    .. svgbob::

        +z
          ^
          |
          |
          +-----> +x
         /
        v
      +y

    .. svgbob::

                              +
                             /|           b
                            * +----<------o
                           /|
                          + +---------->--------o c
              a           |
              o-----<-----+

    After the growing phase, a reverse-delete step is performed to
    remove redundant edges from the forest.

    >>> h = 2
    >>> w = 2
    >>> pairs = [((0, 0), (1, 1))]
    >>> F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(h, w, pairs)
    >>> sorted(F_pruned)
    [(0, 1, 1.0), (1, 3, 1.0)]
    >>> total_cost
    2.0
    >>> sources
    {0}
    >>> terminals
    {3}
    >>> steiner_nodes
    {1}
    """
    n: int = height * width
    uf: UnionFind = UnionFind(n)
    sources: Set[int] = set()
    terminals: Set[int] = set()
    pair_dict: Dict[int, List[int]] = collections.defaultdict(list)
    for (sx, sy), (tx, ty) in pairs:
        source_idx = sx * width + sy
        target_idx = tx * width + ty
        sources.add(source_idx)
        terminals.add(target_idx)
        pair_dict[source_idx].append(target_idx)
        pair_dict[target_idx].append(source_idx)

    all_term: Set[int] = sources | terminals

    # Generate all possible grid edges: horizontal, vertical, diagonal
    edges: List[Tuple[int, int, float]] = []
    for row_idx in range(height):
        for col_idx in range(width):
            node = row_idx * width + col_idx
            # Horizontal
            if col_idx + 1 < width:
                edges.append((node, node + 1, 1.0))
            # Vertical
            if row_idx + 1 < height:
                edges.append((node, node + width, 1.0))

    paid: List[float] = [0.0] * len(edges)
    F: List[Tuple[int, int, float]] = []  # list of (u, v, c) added in order

    while True:
        find = uf.find
        term_root: Dict[int, int] = {term: find(term) for term in all_term}
        feasible = True
        for source in pair_dict:
            root_source = term_root[source]
            for target in pair_dict[source]:
                if term_root[target] != root_source:
                    feasible = False
                    break
            if not feasible:
                break
        if feasible:
            break

        comp_terms: Dict[int, Set[int]] = collections.defaultdict(set)
        for terminal in all_term:
            comp_terms[term_root[terminal]].add(terminal)

        active_comps: Set[int] = set()
        for root, terms in comp_terms.items():
            is_active = False
            for terminal in terms:
                for partner in pair_dict[terminal]:
                    if term_root[partner] != root:
                        is_active = True
                        break
                if is_active:
                    break
            if is_active:
                active_comps.add(root)

        min_delta = float("inf")
        chosen_idx = -1
        chosen_u = chosen_v = 0
        chosen_c = 0.0
        for edge_idx, (node_u, node_v, cost) in enumerate(edges):
            root_u = find(node_u)
            root_v = find(node_v)
            if root_u == root_v:
                continue
            num = 0
            if root_u in active_comps:
                num += 1
            if root_v in active_comps:
                num += 1
            if num == 0:
                continue
            paid_val = paid[edge_idx]
            if paid_val > cost:
                continue
            delta_e = (cost - paid_val) / num
            if delta_e < min_delta:
                min_delta = delta_e
                chosen_idx = edge_idx
                chosen_u, chosen_v, chosen_c = node_u, node_v, cost

        if min_delta == float("inf"):
            raise ValueError("Graph is not connected or cannot connect pairs")

        for edge_idx, (u2, v2, c2) in enumerate(edges):
            ru2 = find(u2)
            rv2 = find(v2)
            if ru2 == rv2:
                continue
            num2 = 0
            if ru2 in active_comps:
                num2 += 1
            if rv2 in active_comps:
                num2 += 1
            if num2 == 0:
                continue
            new_paid = paid[edge_idx] + min_delta * num2
            if new_paid > c2 + 1e-6:  # tolerance
                new_paid = c2
            paid[edge_idx] = new_paid

        if paid[chosen_idx] >= chosen_c - 1e-6:
            F.append((chosen_u, chosen_v, chosen_c))
            uf.union(chosen_u, chosen_v)

    # ``F`` is a forest: every added edge merges two distinct components. The
    # minimal sub-forest preserving all required pair connections is therefore
    # the union of the unique paths between each pair, so mark those paths
    # directly instead of running O(|F|^2) reverse-delete passes that rebuild a
    # UnionFind per candidate edge.
    adjacency: Dict[int, List[Tuple[int, int]]] = collections.defaultdict(list)
    for edge_idx, (node_u, node_v, _cost) in enumerate(F):
        adjacency[node_u].append((node_v, edge_idx))
        adjacency[node_v].append((node_u, edge_idx))

    needed: List[bool] = [False] * len(F)
    for source in sources:
        parent_edge: Dict[int, int] = {}
        parent_node: Dict[int, int] = {}
        visited: Set[int] = {source}
        stack: List[int] = [source]
        while stack:
            node = stack.pop()
            for neighbor, edge_idx in adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent_edge[neighbor] = edge_idx
                    parent_node[neighbor] = node
                    stack.append(neighbor)
        for target in pair_dict[source]:
            current = target
            while current != source:
                edge_idx = parent_edge[current]
                needed[edge_idx] = True
                current = parent_node[current]

    F_pruned: List[Tuple[int, int, float]] = [
        edge for edge_idx, edge in enumerate(F) if needed[edge_idx]
    ]

    total_cost: float = sum(cost for _, _, cost in F_pruned)

    used_nodes: Set[int] = set()
    for node_u, node_v, _ in F_pruned:
        used_nodes.add(node_u)
        used_nodes.add(node_v)
    steiner_nodes: Set[int] = used_nodes - all_term

    return F_pruned, total_cost, sources, terminals, steiner_nodes


def generate_svg(
    height: int,
    width: int,
    F_pruned: List[Tuple[int, int, float]],
    sources: Set[int],
    terminals: Set[int],
    steiner_nodes: Set[int],
    cell_size: int,
    margin: int,
    filename: str,
) -> None:
    """
    Generate an SVG visualization of a Steiner forest on a grid.

    This function creates an SVG image showing the grid with nodes (sources in red,
    terminals in green, Steiner nodes in blue) and selected edges highlighted.

    :param height: Grid height.
    :type height: int
    :param width: Grid width.
    :type width: int
    :param F_pruned: List of edges in the Steiner forest as (u, v, cost) tuples.
    :type F_pruned: List[Tuple[int, int, float]]
    :param sources: Set of source node indices.
    :type sources: Set[int]
    :param terminals: Set of terminal node indices.
    :type terminals: Set[int]
    :param steiner_nodes: Set of Steiner node indices.
    :type steiner_nodes: Set[int]
    :param cell_size: Size of each grid cell in pixels.
    :type cell_size: int
    :param margin: Margin around the grid in pixels.
    :type margin: int
    :param filename: Output SVG filename.
    :type filename: str
    """
    svg_width = width * cell_size + 2 * margin
    svg_height = height * cell_size + 2 * margin
    svg = f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">'

    # Grid lines horizontal
    for row_idx in range(height + 1):
        y_pos = margin + row_idx * cell_size
        svg += f'<line x1="{margin}" y1="{y_pos}" x2="{svg_width - margin}" y2="{y_pos}" stroke="gray" stroke-width="1"/>'

    # Vertical
    for col_idx in range(width + 1):
        x_pos = margin + col_idx * cell_size
        svg += f'<line x1="{x_pos}" y1="{margin}" x2="{x_pos}" y2="{svg_height - margin}" stroke="gray" stroke-width="1"/>'

    # Nodes
    for row_idx in range(height):
        for col_idx in range(width):
            cx = margin + col_idx * cell_size + cell_size / 2
            cy = margin + row_idx * cell_size + cell_size / 2
            node = row_idx * width + col_idx
            if node in sources:
                radius = 10
                fill = "red"
            elif node in terminals:
                radius = 10
                fill = "green"
            elif node in steiner_nodes:
                radius = 7
                fill = "blue"
            else:
                radius = 5
                fill = "black"
            svg += f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}"/>'
            svg += f'<text x="{cx}" y="{cy + 4}" font-size="10" text-anchor="middle">{node}</text>'

    # Selected edges
    for node_u, node_v, _cost in F_pruned:
        ui, uj = divmod(node_u, width)
        vi, vj = divmod(node_v, width)
        ux = margin + uj * cell_size + cell_size / 2
        uy = margin + ui * cell_size + cell_size / 2
        vx = margin + vj * cell_size + cell_size / 2
        vy = margin + vi * cell_size + cell_size / 2
        svg += f'<line x1="{ux}" y1="{uy}" x2="{vx}" y2="{vy}" stroke="orange" stroke-width="5" opacity="0.5"/>'

    svg += "</svg>"

    # Write to SVG file
    with open(filename, "w") as f:
        f.write(svg)
    print(f"SVG file '{filename}' generated successfully.")


def main() -> None:
    """Main function to run the example."""
    # Example parameters (modify as needed)
    height: int = 8  # Height
    width: int = 8  # Width
    pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = [
        ((0, 0), (3, 2)),
        ((0, 0), (0, 5)),
        ((4, 4), (7, 5)),
        ((4, 4), (5, 7)),
        ((0, 1), (4, 1)),
    ]  # Terminal pairs

    F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(
        height, width, pairs
    )

    print(f"Total cost: {total_cost}")
    print(f"Edges: {F_pruned}")

    generate_svg(
        height,
        width,
        F_pruned,
        sources,
        terminals,
        steiner_nodes,
        cell_size=50,
        margin=20,
        filename="steiner_forest.svg",
    )


if __name__ == "__main__":
    main()
