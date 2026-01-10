import collections
from typing import Dict, List, Set, Tuple


class UnionFind:
    """
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
        self.parent: List[int] = list(range(size))
        self.rank: List[int] = [0] * size

    def find(self, idx: int) -> int:
        if self.parent[idx] != idx:
            self.parent[idx] = self.find(self.parent[idx])
        return self.parent[idx]

    def union(self, idx1: int, idx2: int) -> bool:
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
    # diag_cost = 1.0  # Unit cost for demonstration; alternatively use math.sqrt(2) for Euclidean distance
    # diag_cost = 1.4142
    for row_idx in range(height):
        for col_idx in range(width):
            node = row_idx * width + col_idx
            # Horizontal
            if col_idx + 1 < width:
                edges.append((node, node + 1, 1.0))
            # Vertical
            if row_idx + 1 < height:
                edges.append((node, node + width, 1.0))
            # # Diagonal \
            # if row_idx + 1 < h and col_idx + 1 < w:
            #     edges.append((node, node + w + 1, diag_cost))
            # # Diagonal /
            # if row_idx + 1 < h and col_idx - 1 >= 0:
            #     edges.append((node, node + w - 1, diag_cost))

    paid: Dict[Tuple[int, int], float] = collections.defaultdict(float)
    F: List[Tuple[int, int, float]] = []  # list of (u, v, c) added in order

    while True:
        # Compute term_root
        term_root: Dict[int, int] = {term: uf.find(term) for term in all_term}
        # Check if feasible
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

        # Compute comp_terms
        comp_terms: Dict[int, Set[int]] = collections.defaultdict(set)
        for terminal in all_term:
            comp_terms[term_root[terminal]].add(terminal)

        # Compute active_comps
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

        # Find min_delta and chosen edge(s)
        min_delta = float("inf")
        candidate_es: List[Tuple[int, int, float, Tuple[int, int]]] = []
        for node_u, node_v, cost in edges:
            if uf.find(node_u) == uf.find(node_v):
                continue
            root_u = uf.find(node_u)
            root_v = uf.find(node_v)
            num = 0
            if root_u in active_comps:
                num += 1
            if root_v in active_comps:
                num += 1
            if num == 0:
                continue
            key = (min(node_u, node_v), max(node_u, node_v))
            paid_val = paid[key]
            if paid_val > cost:
                continue
            delta_e = (cost - paid_val) / num if num > 0 else float("inf")
            if delta_e < min_delta:
                min_delta = delta_e
                candidate_es = [(node_u, node_v, cost, key)]
            elif delta_e == min_delta:
                candidate_es.append((node_u, node_v, cost, key))

        if min_delta == float("inf"):
            raise ValueError("Graph is not connected or cannot connect pairs")

        # Pick first candidate
        chosen_u, chosen_v, chosen_c, chosen_key = candidate_es[0]

        # Update paid for all eligible edges
        for u2, v2, c2 in edges:
            if uf.find(u2) == uf.find(v2):
                continue
            ru2 = uf.find(u2)
            rv2 = uf.find(v2)
            num2 = 0
            if ru2 in active_comps:
                num2 += 1
            if rv2 in active_comps:
                num2 += 1
            if num2 == 0:
                continue
            key2 = (min(u2, v2), max(u2, v2))
            paid[key2] += min_delta * num2
            if paid[key2] > c2 + 1e-6:  # tolerance
                paid[key2] = c2

        # Add chosen edge if not overpaid
        if paid[chosen_key] >= chosen_c - 1e-6:
            F.append((chosen_u, chosen_v, chosen_c))
            uf.union(chosen_u, chosen_v)

    # Reverse delete
    F_pruned: List[Tuple[int, int, float]] = F[:]
    for idx in range(len(F) - 1, -1, -1):
        temp_uf = UnionFind(n)
        for jdx in range(len(F)):
            if jdx != idx:
                node_u, node_v, _ = F[jdx]
                temp_uf.union(node_u, node_v)
        connected = True
        for source in sources:
            for target in pair_dict[source]:
                if temp_uf.find(source) != temp_uf.find(target):
                    connected = False
                    break
            if not connected:
                break
        if connected:
            del F_pruned[idx]

    # Compute cost
    total_cost: float = sum(cost for _, _, cost in F_pruned)

    # Identify Steiner nodes
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
    """Generates an SVG visualization of the Steiner forest."""
    svg_width = width * cell_size + 2 * margin
    svg_height = height * cell_size + 2 * margin
    svg = f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">'
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'

    # Grid lines horizontal
    for row_idx in range(height + 1):
        y_pos = margin + row_idx * cell_size
        svg += f'<line x1="{margin}" y1="{y_pos}" x2="{svg_width - margin}" y2="{y_pos}" stroke="gray" stroke-width="1"/>'

    # Vertical
    for col_idx in range(width + 1):
        x_pos = margin + col_idx * cell_size
        svg += f'<line x1="{x_pos}" y1="{margin}" x2="{x_pos}" y2="{svg_height - margin}" stroke="gray" stroke-width="1"/>'

    # Nodes
    sources | terminals
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
    for node_u, node_v, cost in F_pruned:
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
