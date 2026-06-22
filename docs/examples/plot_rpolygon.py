"""
Rectilinear polygon
===================

A rectilinear polygon is converted to a general ``Polygon`` via
``to_polygon()``, which inserts intermediate vertices so all edges
are axis-aligned, then plotted.
"""
import matplotlib.pyplot as plt
from physdes.point import Point
from physdes.rpolygon import RPolygon
from physdes.to_polygon import to_polygon

coords = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
S = [Point(x, y) for x, y in coords]
rpoly = RPolygon.from_pointset(S)
poly = to_polygon(rpoly)

# _vecs are absolute positions relative to origin (NOT edge vectors)
ox, oy = poly._origin.xcoord, poly._origin.ycoord
pts = [poly._origin] + [Point(ox + v.x_, oy + v.y_) for v in poly._vecs]
# Close back to origin
pts.append(poly._origin)

xs = [p.xcoord for p in pts]
ys = [p.ycoord for p in pts]

plt.figure(figsize=(6, 6))
plt.plot(xs, ys, "b-o", linewidth=2, markersize=8)
plt.fill(xs, ys, alpha=0.15, color="skyblue")
for i, (x, y) in enumerate(zip(xs[:-1], ys[:-1])):
    plt.text(x, y, f"  P{i}", fontsize=10, verticalalignment="bottom")
plt.axhline(0, color="gray", linewidth=0.5)
plt.axvline(0, color="gray", linewidth=0.5)
plt.gca().set_aspect("equal")
plt.title("Rectilinear polygon (via to_polygon)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, alpha=0.3)
