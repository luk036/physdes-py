[![codecov](https://codecov.io/gh/luk036/physdes-py/branch/main/graph/badge.svg?token=EIv4D8NlYj)](https://codecov.io/gh/luk036/physdes-py)
[![Documentation Status](https://readthedocs.org/projects/physdes-py/badge/?version=latest)](https://physdes-py.readthedocs.io/en/latest/?badge=latest)

<p align="center">
  <img src="./rectilinear-shapes-for-vlsi-physical-desgin.svg"/>
</p>

# 🧱 physdes-py

> Physical Design Python Code

## ✨ Features

- Rectilinear Polygon support

## 🚀 Recent Developments

- **Deferred Merge Embedding (DME) Algorithm:** Implemented the DME algorithm for clock tree synthesis, featuring a strategy pattern for delay calculation. This allows for flexible delay modeling, with both `LinearDelayCalculator` and `ElmoreDelayCalculator` provided as options. The algorithm is designed to build a zero-skew clock tree and includes functionalities for analyzing clock skew, total wirelength, and other tree statistics.
- **Global Router Enhancements:** The global router now offers multiple routing strategies to accommodate different design needs:
  - `route_simple()`: Connects terminals directly to the nearest node in the tree for quick and straightforward routing.
  - `route_with_steiners()`: Inserts Steiner points to optimize wire length, resulting in more efficient routing.
  - `route_with_constraints()`: A performance-driven approach that also uses Steiner points to reduce wire length.

## Dependencies

- [luk036/mywheel](https://github.com/luk036/mywheel)
- [luk036/lds-gen](https://github.com/luk036/lds-gen) (for testing only)

## 👀 See also

- [physdes-cpp](https://github.com/luk036/physdes-cpp)
- [physdes-rs](https://github.com/luk036/physdes-rs)

## 👉 Note

This project has been set up using PyScaffold 3.2.1. For details and usage
information on PyScaffold see <https://pyscaffold.org/>.

## Output Examples

### Basic Clock Tree

![Basic Clock Tree](./outputs/basic_clock_tree.svg)

### Convex Hull

![Convex Hull](./outputs/convex_hull.svg)

### Example Route Simple

![Example Route Simple](./outputs/example_route_simple.svg)

### Polygon Convex Hull

![Polygon Convex Hull](./outputs/polygon_convex_hull.svg)
