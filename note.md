# Geometry shapes

python: shapely

# Rectilinear shapes

Applications: VLSI

- Billion of objects N

- Mainly Integer Coordinate

  - faster than floating point. More importantly, more accurate.
  - Objects are small, but coordinates could be very large
    - Concept of affine space:
      - point + vector = point
      - point - point = vector
      - arithmetics for vector only

- Rectilinear polygon

  - the number of vertices of each polygon is small
    (say within 100)
  - Consider special cases
  - Testing
  - Visualization
  - Accept O(n^2)

- Rectilinear Steiner tree
