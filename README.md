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
information on PyScaffold see <https://pyscaffold.org/>

## 🤖 For AI Agents

If you're an AI agent working on this repository, please see [AGENTS.md](AGENTS.md)
for comprehensive guidelines on:
- Build/lint/test commands
- Code style and conventions
- Testing practices
- Development workflow

## Output Examples

### Clock Tree Synthesis Examples

**Elmore Delay Model Clock Tree**

![Elmore Delay Model Clock Tree](./outputs/elmore_model_clock_tree.svg)

**Linear Delay Model Clock Tree**

![Linear Delay Model Clock Tree](./outputs/linear_model_clock_tree.svg)

**Delay Model Comparison**

![Delay Model Comparison](./outputs/delay_model_comparison.svg)

**3D Elmore Model Clock Tree**

![3D Elmore Model Clock Tree](./outputs/elmore_model_clock_tree3d.svg)

**3D Linear Model Clock Tree**

![3D Linear Model Clock Tree](./outputs/linear_model_clock_tree3d.svg)

### Global Routing Examples

**Routing with Steiner Points**

![Routing with Steiner Points](./outputs/example_route_with_steiner.svg)

**Routing with Constraints**

![Routing with Constraints](./outputs/example_route_with_constraint.svg)

**Routing with Keepouts**

![Routing with Keepouts](./outputs/example_route_with_keepouts.svg)

**Routing with Steiner Points and Keepouts**

![Routing with Steiner Points and Keepouts](./outputs/example_route_with_steiner_and_keepouts.svg)

**3D Routing with Steiner Points**

![3D Routing with Steiner Points](./outputs/example_route3d_with_steiner.svg)

**3D Routing with Constraints and Keepouts**

![3D Routing with Constraints and Keepouts](./outputs/example_route3d_with_constraint_and_keepouts.svg)

### Rectilinear Polygon Examples

**Rectilinear Polygon Convex Hull**

![Rectilinear Polygon Convex Hull](./outputs/rpolyon_convex_hull.svg)

**Rectilinear Polygon Convex Cut**

![Rectilinear Polygon Convex Cut](./outputs/rpolygon_convex_cut.svg)

**X-Monotone Hull**

![X-Monotone Hull](./outputs/rpolyon_xmono_hull.svg)

**Y-Monotone Hull**

![Y-Monotone Hull](./outputs/rpolyon_ymono_hull.svg)

### Steiner Forest

**Steiner Forest**

![Steiner Forest](./outputs/steiner_forest.svg)
