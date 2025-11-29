import collections
from typing import Any, Dict, List, Set, Tuple, Union, DefaultDict, Optional, cast


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent: List[int] = list(range(size))
        self.rank: List[int] = [0] * size

    def find(self, p: int) -> int:
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p: int, q: int) -> bool:
        pp = self.find(p)
        pq = self.find(q)
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


def steiner_forest_grid(h: int, w: int, pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Tuple[List[Tuple[int, int, float]], float, Set[int], Set[int], Set[int]]:
    r"""
    Solves the Steiner Forest Problem on a grid graph with diagonal edges.

    The algorithm is based on the primal-dual approach for the Steiner
    network problem. It iteratively pays for edges until all terminal
    pairs are connected.

    The following diagram illustrates the concept of a Steiner tree,
    where 'o' represents terminals and '*' represents Steiner points.
    Diagonal connections are also considered.

    .. svgbob::

         +--.----------o
         |   `.        |
         |     `.      |
         |       `.    |
         o---------`---+

    In our case, we are looking for a Steiner forest, which is a collection
    of Steiner trees connecting specified pairs of terminals on a grid,
    allowing for horizontal, vertical, and diagonal connections.

    .. svgbob::

          Grid (with diagonals)    Steiner Forest (with diagonals)
        .---.---.---.              .---.---.---.
        | S | \ | T |              | S o \ * o T |
        '---'---'---'              '---'---'---'---'
        | / | * | \ |              | / | * | \ |
        '---'---'---'              '---'---'---'---'
        | S | / | T |              | S o / * o T |
        '---'---'---'              '---'---'---'---'

    The algorithm works by "growing" paths from terminals. Each active
    component (a connected component containing at least one terminal
    that needs to be connected to a terminal in another component)
    contributes to the cost of edges.

    When the cost paid for an edge equals its weight, the edge is
    added to the forest.

    After the growing phase, a reverse-delete step is performed to
    remove redundant edges from the forest.

    """
    n = h * w
    uf = UnionFind(n)
    sources = set()
    terminals = set()
    pair_dict = collections.defaultdict(list)
    for (sx, sy), (tx, ty) in pairs:
        s = sx * w + sy
        t = tx * w + ty
        sources.add(s)
        terminals.add(t)
        pair_dict[s].append(t)
        pair_dict[t].append(s)

    all_term = sources | terminals

    # Generate all possible grid edges: horizontal, vertical, diagonal
    edges = []
    diag_cost = 1.0  # Unit cost for demonstration; alternatively use math.sqrt(2) for Euclidean distance
    for i in range(h):
        for j in range(w):
            node = i * w + j
            # Horizontal
            if j + 1 < w:
                edges.append((node, node + 1, 1.0))
            # Vertical
            if i + 1 < h:
                edges.append((node, node + w, 1.0))
            # Diagonal \
            if i + 1 < h and j + 1 < w:
                edges.append((node, node + w + 1, diag_cost))
            # Diagonal /
            if i + 1 < h and j - 1 >= 0:
                edges.append((node, node + w - 1, diag_cost))

    paid: DefaultDict[Tuple[int, int], float] = collections.defaultdict(float)
    F = []  # list of (u, v, c) added in order

    while True:
        # Compute term_root
        term_root = {t: uf.find(t) for t in all_term}
        # Check if feasible
        feasible = True
        for s in pair_dict:
            rs = term_root[s]
            for t in pair_dict[s]:
                if term_root[t] != rs:
                    feasible = False
                    break
            if not feasible:
                break
        if feasible:
            break

        # Compute comp_terms
        comp_terms = collections.defaultdict(set)
        for t in all_term:
            comp_terms[term_root[t]].add(t)

        # Compute active_comps
        active_comps = set()
        for root, terms in comp_terms.items():
            is_active = False
            for t in terms:
                for partner in pair_dict[t]:
                    if term_root[partner] != root:
                        is_active = True
                        break
                if is_active:
                    break
            if is_active:
                active_comps.add(root)

        # Find min_delta and chosen edge(s)
        min_delta = float("inf")
        candidate_es = []
        for u, v, c in edges:
            if uf.find(u) == uf.find(v):
                continue
            ru = uf.find(u)
            rv = uf.find(v)
            num = 0
            if ru in active_comps:
                num += 1
            if rv in active_comps:
                num += 1
            if num == 0:
                continue
            key = (min(u, v), max(u, v))
            paid_val = paid[key]
            if paid_val > c:
                continue
            delta_e = (c - paid_val) / num if num > 0 else float("inf")
            if delta_e < min_delta:
                min_delta = delta_e
                candidate_es = [(u, v, c, key)]
            elif delta_e == min_delta:
                candidate_es.append((u, v, c, key))

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
    F_pruned = F[:]
    for i in range(len(F) - 1, -1, -1):
        temp_uf = UnionFind(n)
        for j in range(len(F)):
            if j != i:
                u, v, _ = F[j]
                temp_uf.union(u, v)
        connected = True
        for s in sources:
            for t in pair_dict[s]:
                if temp_uf.find(s) != temp_uf.find(t):
                    connected = False
                    break
            if not connected:
                break
        if connected:
            del F_pruned[i]

    # Compute cost
    total_cost = sum(c for _, _, c in F_pruned)

    # Identify Steiner nodes
    used_nodes = set()
    for u, v, _ in F_pruned:
        used_nodes.add(u)
        used_nodes.add(v)
    steiner_nodes = used_nodes - all_term

    return F_pruned, total_cost, sources, terminals, steiner_nodes

