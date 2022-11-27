# Geometry shapes

python: shapely

# Rectilinear shapes

Applications: VLSI

- Billions of objects
- Mainly Integer Coordinate

- Faster than floating Point. No round-off error.
- Rectangle = Point<Interval, Interval>

---

## Rectilinear Polygon

- The number of vertices of each Polygon is small
    (say within 100)
- Consider special cases
- Testing
  - Visualization
  - Accept O(n^2)
- x-monotone, y-monotone
- [ ] Rectilinearly convex hull
  (Steiner points only exists inside the convex hull of given points)

## Merging segment (45 degree line segment)

## 3D Extension

## Possible contribution

- Testing
- Port to C++

