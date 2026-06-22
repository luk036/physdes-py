"""
Rectangle overlap detection
============================

Several rectangles visualized with overlapping pairs highlighted in red,
using the sweep-line algorithm from ``detect_overlap_gen``.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from physdes.interval import Interval
from physdes.recti import Rectangle, detect_overlap_gen

rects = [
    Rectangle(Interval(1, 5), Interval(1, 4)),
    Rectangle(Interval(3, 7), Interval(2, 6)),
    Rectangle(Interval(8, 10), Interval(3, 5)),
    Rectangle(Interval(2, 4), Interval(5, 8)),
    Rectangle(Interval(6, 9), Interval(4, 7)),
]

fig, ax = plt.subplots(figsize=(7, 5))
overlap_pairs = list(detect_overlap_gen(rects))
overlap_ids = set()
for r1, r2 in overlap_pairs:
    for i, r in enumerate(rects):
        if r is r1 or r is r2:
            overlap_ids.add(i)

colors = ["salmon" if i in overlap_ids else "lightblue" for i in range(len(rects))]

for i, r in enumerate(rects):
    rect = mpatches.Rectangle(
        (r.xcoord.lb, r.ycoord.lb),
        r.xcoord.ub - r.xcoord.lb,
        r.ycoord.ub - r.ycoord.lb,
        facecolor=colors[i],
        edgecolor="black",
        linewidth=1.5,
        alpha=0.7,
    )
    ax.add_patch(rect)
    label = f"R{i}" + (" (overlap)" if i in overlap_ids else "")
    ax.text(
        (r.xcoord.lb + r.xcoord.ub) / 2,
        (r.ycoord.lb + r.ycoord.ub) / 2,
        label,
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
    )

ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.set_aspect("equal")
ax.set_title(f"Rectangle overlap detection ({len(overlap_pairs)} overlapping pair(s))")
ax.grid(True, alpha=0.3)
