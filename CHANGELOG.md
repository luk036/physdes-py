# Changelog

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
