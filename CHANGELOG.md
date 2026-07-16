# Changelog

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
