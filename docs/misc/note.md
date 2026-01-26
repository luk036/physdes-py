# Geometry shapes

c.f. python: shapely

# 𓊍 Rectilinear shape

- Also known as L-shape, orthogonal shape

Applications: VLSI

- Billions of objects
- Restrict integer coordinate ✨🚀
  - In C++/Rust, faster than floating Point. No round-off error.
  - In Python, arbitrary precision.
- Usually Simpler than general shapes
- Rectangle = Point<Interval, Interval>

Additional metric consideration, different story.

- L1 metric vs. L2 metric

---

## Rectilinear Polygon

- Use canonical form to simplify algorithms ✨🚀
- Assume the number of vertices of each Polygon is small
  (say within 100)
- Accept O(n^2) algorithms
- x-monotone, y-monotone
- Orthogonal convex hull
  (Steiner points only exists inside the convex hull of given points)

---

## Computational Geometry

- Art Gallery problem
- Minimum Spanning Tree (easy)
- Steiner Tree, RST
- Traveling Sale Person
- Voronoi diagram (with integer coordinates)

## Merging segment (45° line segment)

- Tap point in Clock tree synthesis (with integer coordinates)
- Analogue to "Circle" in L2-metric (unit-ball in 2D)

## 3D Extension

- Path (x -> z -> y)

## Possible contribution

- Testing
- Porting to C++
- Documentation
