"""
Clock tree synthesis (DME)
===========================

Clock tree built with the DME algorithm using a linear delay model.
Sinks are green, internal nodes are blue, source is red.
"""
import matplotlib.pyplot as plt
from physdes.point import Point
from physdes.cts.dme_algorithm import DMEAlgorithm, Sink, LinearDelayCalculator

sinks = [
    Sink("s1", Point(-100, 40), 1.0),
    Sink("s2", Point(-60, 60), 1.0),
    Sink("s3", Point(0, 40), 1.0),
    Sink("s4", Point(20, 20), 1.0),
    Sink("s5", Point(-20, -20), 1.0),
    Sink("s6", Point(-30, -50), 1.0),
    Sink("s7", Point(-100, -40), 1.0),
    Sink("s8", Point(-100, 0), 1.0),
]
source = Point(4, -1)

calc = LinearDelayCalculator(delay_per_unit=0.5, capacitance_per_unit=0.2)
dme = DMEAlgorithm(sinks, calc, source)
tree = dme.build_clock_tree()

sink_positions = {(s.position.xcoord, s.position.ycoord) for s in sinks}

def walk(node, depth=0):
    """Collect nodes recursively."""
    if node is None:
        return [], []
    nodes, edges = [(node, depth)], []
    for child in (node.left, node.right):
        if child is not None:
            edges.append((node, child))
            cn, ce = walk(child, depth + 1)
            nodes.extend(cn)
            edges.extend(ce)
    return nodes, edges

nodes, edges = walk(tree)

fig, ax = plt.subplots(figsize=(8, 7))
for parent, child in edges:
    ax.plot(
        [parent.position.xcoord, child.position.xcoord],
        [parent.position.ycoord, child.position.ycoord],
        color="gray", linewidth=1.5, zorder=1,
    )

for node, _depth in nodes:
    x, y = node.position.xcoord, node.position.ycoord
    is_sink = (x, y) in sink_positions
    is_root = node.parent is None
    if is_root:
        color, size, label = "#F44336", 120, "Source"
    elif is_sink:
        color, size, label = "#4CAF50", 80, None
    else:
        color, size, label = "#2196F3", 60, None
    ax.scatter(x, y, c=color, s=size, edgecolors="black", linewidths=0.8, zorder=2)
    if is_root:
        ax.annotate(label, (x, y), xytext=(5, 8),
                    textcoords="offset points", fontsize=9)

ax.set_title("DME Clock Tree (Linear Delay Model)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, alpha=0.3)
ax.set_aspect("equal")
