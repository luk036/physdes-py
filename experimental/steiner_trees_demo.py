import hashlib

import matplotlib.pyplot as plt


# --- (Standard DSU and Hanan Logic from previous steps) ---
class DSU:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}

    def find(self, i):
        if self.parent[i] == i:
            return i
        return self.find(self.parent[i])

    def union(self, i, j):
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False


def prune_tree(edges, terminals):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    changed = True
    while changed:
        changed = False
        for node in list(adj.keys()):
            if len(adj[node]) == 1 and node not in terminals:
                neighbor = adj[node].pop()
                adj[neighbor].remove(node)
                del adj[node]
                changed = True
    return [(u, v) for u in adj for v in adj[u] if u < v]


def plot_tree(edges, terminals, title, ax):
    # Draw Hanan grid background
    xs = sorted(set(p[0] for p in terminals))
    ys = sorted(set(p[1] for p in terminals))
    for x in xs:
        ax.axvline(x, color="lightgray", linestyle="--", linewidth=0.5)
    for y in ys:
        ax.axhline(y, color="lightgray", linestyle="--", linewidth=0.5)

    # Draw tree edges
    for u, v in edges:
        ax.plot([u[0], v[0]], [u[1], v[1]], "blue", lw=3, alpha=0.7)

    # Draw terminals
    t_x, t_y = zip(*terminals)
    ax.scatter(t_x, t_y, color="red", s=100, zorder=5, label="Terminals")
    ax.set_title(title)
    ax.set_aspect("equal")


# --- ENUMERATION & PLOTTING ---
def run_visual_demo():
    source = (0, 0)
    sinks = [(1, 2), (2, 1)]
    terminals = set([source] + sinks)

    xs, ys = (
        sorted(set(p[0] for p in terminals)),
        sorted(set(p[1] for p in terminals)),
    )
    nodes = [(x, y) for x in xs for y in ys]

    # Generate Hanan Edges
    h_edges = []
    for y in ys:
        for i in range(len(xs) - 1):
            h_edges.append(((xs[i], y), (xs[i + 1], y)))
    for x in xs:
        for j in range(len(ys) - 1):
            h_edges.append(((x, ys[j]), (x, ys[j + 1])))

    found_trees = []
    seen_hashes = set()

    def backtrack(idx, current_edges, dsu):
        root = dsu.find(source)
        if all(dsu.find(s) == root for s in sinks):
            clean = prune_tree(current_edges, terminals)
            # Create a simple hash for this specific geometry using sha256
            h = hashlib.sha256(str(sorted(clean)).encode()).hexdigest()
            if h not in seen_hashes:
                seen_hashes.add(h)
                found_trees.append(clean)
            return

        if idx >= len(h_edges):
            return

        # Include/Exclude logic
        u, v = h_edges[idx]
        prev_dsu = dsu.parent.copy()
        if dsu.union(u, v):
            current_edges.append((u, v))
            backtrack(idx + 1, current_edges, dsu)
            current_edges.pop()
            dsu.parent = prev_dsu
        backtrack(idx + 1, current_edges, dsu)

    backtrack(0, [], DSU(nodes))

    # Plot results
    n_plot = min(len(found_trees), 6)  # Plot up to 6 unique trees
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for i in range(n_plot):
        plot_tree(found_trees[i], terminals, f"Topology {i + 1}", axes[i])

    plt.tight_layout()
    plt.show()


run_visual_demo()
