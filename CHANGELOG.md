# Changelog

## Version 0.9 (2026-10-09)

### Performance
- **Hot-path allocation & debug-I/O cuts**: `manhattan_arc` drops live `ic()` calls from the DME embedding path (and removes `icecream` from the runtime deps); `congestion_map` guards its demo behind `__main__`; `steiner_forest_grid` uses an iterative `UnionFind.find`, hoists finds 4→2 per edge, indexes `paid` by edge, and replaces O(|F|²) reverse-delete with union-of-paths pruning (~1.7×); `routing_tree` gets a scalar 2D fast path in `_find_insertion_point` and list-join `get_tree_structure` (~4× insertion); `dme_algorithm` precomputes keys and does a single-pass stable partition in `_build_merging_tree` (1.2–1.5×). Output-identical, verified by differential tests. (#10a4e9f)

### Bug Fixes
- **Unbounded wirelength sentinel**: `insert_terminal_with_steiner` previously ignored the tree's `worst_wirelength` by passing a literal `10**12`; the default is now `float('inf')` and Steiner insertion passes it through, so the unconstrained variant honors any caller-set bound. (#0947827)

### Testing & Code Quality
- **Temp-cwd isolation for tests**: Added an autouse `_isolate_cwd` fixture so visualization tests' relative-path SVG writes land in pytest's temporary directory instead of the repository root. (#409d422)
- **New benchmarks**: Added `test_benchmarks.py` (5 benchmarks). (#10a4e9f)

### Code Cleanup
- **SVG EOF newlines**: Added trailing newlines to the example SVGs and formatted the sources. (#0c698e0)

### Build & CI
- **Dropped `icecream` runtime dep**: Removed it from `setup.cfg` and `requirements/default.txt`. (#10a4e9f)

## Version 0.8 (2026-09-04)

### Features
- **Builder pattern for ClockTreeVisualizer**: Added fluent `ClockTreeVisualizerBuilder` (`builder().margin(..).node_radius(..)...build()`) mirroring the C++/Rust siblings; `create_interactive_svg` and `create_comparison_visualization` now use it. (#311848a)

### Refactoring
- **Template Method in rpolygon cut decomposition**: Collapsed the duplicated convex/explicit recursive decomposers into one `rpolygon_cut_recur` Template Method plus shared `rpolygon_cut_impl`; public entry points unchanged. (#3666c82)
- **Factory Method in global routing tree**: Concentrated 5 duplicated ID-generation/registration sites behind a single `_create_node` factory, preserving the `insert_node_on_branch` ValueError contract and ordering constraints. (#2e03732)
- **Module-level logging**: Replaced `skeleton._logger` with standard module-level `logging`. (#6c863fd)

### Testing & Code Quality
- **Builder tests**: Added tests for builder output, default-equivalence and fluent reuse, plus a doctest on the builder class. (#311848a)
- **mypy fixes**: Resolved None checks and type annotations. (#2a5f7b2)

### Code Cleanup
- **Removed AI slop**: Stripped boilerplate from docstrings and comments. (#587ad95)
- **Deduped route3d legends**: Removed duplicated legend entries in example SVGs. (#678aa21)
- **Stripped empty `entry_points`**: Removed dead section from setup.cfg. (#fd06baf)
- **EOF newlines in example SVGs**: Added trailing newlines to 15 figures and formatted sources. (#23aaf16)

### Build & CI
- **RTD doc build**: Added matplotlib and numpy to `docs/requirements.txt`. (#41cad71)

## Version 0.7 (2026-07-16)

### Performance
- **`__slots__` on core geometry classes**: Added `__slots__` to `Point`, `ManhattanArc`, `Polygon`, `RPolygon`, `TreeNode`, `Sink` — saving ~176 bytes per instance. Most impactful on `Point` which is used everywhere in the codebase. (#64242a6)

### Bug Fixes
- **DME alignment with Rust**: Fixed elongation calculation with `raw_extend_left` to match Rust/C++. Replaced `sorted()` with median-partition in `build_merging_tree` (matches Rust `nth_element`). (#0267be3)
- **NodeType rename**: Changed `ALL_CAPS` enum values to `PascalCase` to align with Rust naming conventions. (#0267be3)

### Documentation
- **Doc build scripts**: Updated remark and slide build scripts. Updated example plot scripts for RPolygon, CTS, and global router. (#0a613b3)

### Code Cleanup
- **Removed PyScaffold boilerplate**: Deleted `skeleton.py`/`test_skeleton.py`, removed Python < 3.9 compat, unused mypy ignores, stale files. (#e594991)
