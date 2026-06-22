"""
Global router with Steiner points
==================================

A routing tree built with the global router using Steiner-point
optimisation. Source is red, Steiner nodes are blue, terminals are green.
"""
import matplotlib.pyplot as plt
from physdes.point import Point
from physdes.router.global_router import GlobalRouter
from physdes.router.routing_tree import NodeType

source = Point(0, 0)
terminals = [
    Point(10, 5), Point(3, 8), Point(12, 12),
    Point(5, -4), Point(-4, 6), Point(8, -2),
]

router = GlobalRouter(source, terminals)
router.route_with_steiners()
tree = router.tree

def collect(node):
    """Flatten tree to (nodes, edges)."""
    nodes, edges = [node], []
    for child in node.children:
        edges.append((node, child))
        cn, ce = collect(child)
        nodes.extend(cn)
        edges.extend(ce)
    return nodes, edges

nodes, edges = collect(tree.source)

colors = {
    NodeType.SOURCE: "#F44336",
    NodeType.STEINER: "#2196F3",
    NodeType.TERMINAL: "#4CAF50",
}
sizes = {
    NodeType.SOURCE: 120,
    NodeType.STEINER: 60,
    NodeType.TERMINAL: 80,
}

fig, ax = plt.subplots(figsize=(7, 7))
for parent, child in edges:
    ax.plot(
        [parent.pt.xcoord, child.pt.xcoord],
        [parent.pt.ycoord, child.pt.ycoord],
        color="gray", linewidth=1.5, zorder=1,
    )

for node in nodes:
    x, y = node.pt.xcoord, node.pt.ycoord
    ax.scatter(x, y, c=colors[node.type], s=sizes[node.type],
               edgecolors="black", linewidths=0.8, zorder=2)

    if node.type == NodeType.SOURCE:
        ax.annotate("Source", (x, y), xytext=(5, 8),
                    textcoords="offset points", fontsize=9)

wl = tree.calculate_total_wirelength()
ax.set_title(f"Global Router (Steiner) — Total wirelength: {wl:.1f}")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, alpha=0.3)
ax.set_aspect("equal")
