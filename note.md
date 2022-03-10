# Geometry shapes

python: shapely

# Rectilinear shapes

Applications: VLSI

- Billion of objects N

- Mainly Integer Coordinate

  - faster than floating Point. More importantly, more accurate.
  - Objects are small, but coordinates could be very large
    - Concept of affine space:
      - Point + vector = Point
      - Point - Point = vector
      - arithmetics for vector only

- Rectilinear Polygon

  - the number of vertices of each Polygon is small
    (say within 100)
  - Consider special cases
  - Testing
  - Visualization
  - Accept O(n^2)

- Rectilinear Steiner tree
