import collections


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p, q):
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


def steiner_forest_grid(h, w, pairs):
    n = h * w
    uf = UnionFind(n)
    terminals = set()
    pair_dict = collections.defaultdict(list)
    for (sx, sy), (tx, ty) in pairs:
        s = sx * w + sy
        t = tx * w + ty
        terminals.add(s)
        terminals.add(t)
        pair_dict[s].append(t)
        pair_dict[t].append(s)

    # Generate all possible grid edges: (u, v, c)
    edges = []
    for i in range(h):
        for j in range(w):
            node = i * w + j
            if j + 1 < w:
                edges.append((node, node + 1, 1))
            if i + 1 < h:
                edges.append((node, node + w, 1))

    paid = collections.defaultdict(float)
    F = []  # list of (u, v, c) added in order

    while True:
        # Compute term_root
        term_root = {t: uf.find(t) for t in terminals}
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
        for t in terminals:
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
            delta_e = (c - paid_val) / num
            if delta_e < min_delta:
                min_delta = delta_e
                candidate_es = [(u, v, c, key)]
            elif delta_e == min_delta:
                candidate_es.append((u, v, c, key))

        if min_delta == float("inf"):
            raise ValueError("Graph is not connected or cannot connect pairs")

        # Pick first candidate
        chosen_u, chosen_v, chosen_c, chosen_key = candidate_es[0]

        # Update paid for all candidate edges
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

        # Add chosen edge
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
        for (sx, sy), (tx, ty) in pairs:
            s = sx * w + sy
            t = tx * w + ty
            if temp_uf.find(s) != temp_uf.find(t):
                connected = False
                break
        if connected:
            del F_pruned[i]

    # Compute cost
    total_cost = sum(c for _, _, c in F_pruned)

    return F_pruned, total_cost


# Example parameters (modify as needed)
h = 8  # Height
w = 8  # Width
pairs = [
    ((0, 2), (7, 0)),
    ((0, 0), (7, 2)),
    ((5, 5), (7, 6)),
    ((5, 5), (6, 7)),
]  # Terminal pairs

F_pruned, total_cost = steiner_forest_grid(h, w, pairs)

# Generate SVG and write to file
cell_size = 50
margin = 20
width = w * cell_size + 2 * margin
height = h * cell_size + 2 * margin
svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'

# Grid lines horizontal
for i in range(h + 1):
    y = margin + i * cell_size
    svg += f'<line x1="{margin}" y1="{y}" x2="{width - margin}" y2="{y}" stroke="gray" stroke-width="1"/>'

# Vertical
for j in range(w + 1):
    x = margin + j * cell_size
    svg += f'<line x1="{x}" y1="{margin}" x2="{x}" y2="{height - margin}" stroke="gray" stroke-width="1"/>'

# Nodes
terminals = set()
for (sx, sy), (tx, ty) in pairs:
    terminals.add(sx * w + sy)
    terminals.add(tx * w + ty)

for i in range(h):
    for j in range(w):
        cx = margin + j * cell_size + cell_size / 2
        cy = margin + i * cell_size + cell_size / 2
        node = i * w + j
        r = 10 if node in terminals else 5
        fill = "red" if node in terminals else "black"
        svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
        svg += f'<text x="{cx}" y="{cy + 4}" font-size="10" text-anchor="middle">{node}</text>'

# Selected edges
for u, v, c in F_pruned:
    ui, uj = divmod(u, w)
    vi, vj = divmod(v, w)
    ux = margin + uj * cell_size + cell_size / 2
    uy = margin + ui * cell_size + cell_size / 2
    vx = margin + vj * cell_size + cell_size / 2
    vy = margin + vi * cell_size + cell_size / 2
    svg += f'<line x1="{ux}" y1="{uy}" x2="{vx}" y2="{vy}" stroke="blue" stroke-width="5"/>'

svg += "</svg>"

# Write to SVG file
with open("steiner_forest.svg", "w") as f:
    f.write(svg)

print("SVG file 'steiner_forest.svg' generated successfully.")
print(f"Total cost: {total_cost}")
print(f"Edges: {F_pruned}")
