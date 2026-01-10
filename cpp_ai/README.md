# physdes-cpp: Physical Design Algorithms for VLSI in C++23

A C++23 implementation of geometric primitives and algorithms for VLSI physical design, converted from the Python `physdes-py` library.

## Features

- **Header-only library** - Easy integration into existing projects
- **C++23 standard** - Modern C++ features including concepts and constexpr
- **Geometric primitives**:
  - `Interval<T>`: Arithmetic intervals with hull/enlarge operations
  - `Point<T>`: 2D points with Manhattan distance calculations
  - `Vector2<T>`: 2D vectors with full arithmetic support
  - `Rectangle<T>`, `VSegment<T>`, `HSegment<T>`: Axis-aligned shapes
- **Generic operations**: `overlap()`, `contain()`, `intersection()`, `min_dist()`
- **Build systems**: CMake and xmake support
- **Testing**: Comprehensive doctest test suite

## Quick Start

### Prerequisites

- C++23 compatible compiler (GCC 12+, Clang 15+, MSVC 2022+)
- CMake 3.20+ (optional, for CMake builds)
- xmake (optional, for xmake builds)
- doctest (automatically downloaded by CMake)

### Using as Header-Only Library

Simply include the main header:

```cpp
#include "recti.hpp"

int main() {
    using namespace recti;

    Interval<int> interval{1, 5};
    Point<int> point{3, 4};

    // Use geometric operations
    bool contains = interval.contains(3);  // true
    auto dist = point.min_dist_with(Point{5, 6});  // 4

    return 0;
}
```

## Building and Testing

### Using CMake

```bash
# Configure
mkdir build && cd build
cmake .. -DBUILD_TESTS=ON -DBUILD_EXAMPLES=ON

# Build
make -j4

# Run tests
./physdes_tests

# Run example
./example_interval
```

### Using xmake

```bash
# Configure and build
xmake f -m debug
xmake

# Run tests (automatically runs after build in debug mode)
```

### Build Options

| Option | Description | Default |
|--------|-------------|---------|
| `BUILD_TESTS` | Build test executable | `ON` |
| `BUILD_EXAMPLES` | Build example programs | `OFF` |

## API Overview

### Interval Operations

```cpp
Interval<int> a{1, 5};
Interval<int> b{3, 7};

// Basic operations
bool overlaps = a.overlaps(b);           // true
bool contains = a.contains(3);           // true
auto intersection = a.intersect_with(b); // [3, 5]
auto distance = a.min_dist_with(b);      // 0 (overlap)

// Utility functions
auto hull = recti::hull(a, 10);          // [1, 10]
auto enlarged = a.enlarge(2);            // [-1, 7]
auto center = a.get_center();            // 3
```

### Point and Vector Operations

```cpp
Point<int> p1{3, 4};
Point<int> p2{5, 6};
Vector2<int> v{2, 2};

// Manhattan distance
auto dist = p1.min_dist_with(p2);  // 4

// Vector arithmetic
auto p3 = p1 + v;  // (5, 6)
auto v2 = p2 - p1; // (2, 2)

// Nearest point search
std::vector<Point<int>> candidates = { {1, 1}, {5, 5}, {3, 3} };
auto nearest = nearest_point_to(p1, candidates);  // &Point{3, 3}
```

### Rectangle and Segment Operations

```cpp
Rectangle<int> rect{ {1, 5}, {2, 6} };
VSegment<int> vseg{5, {1, 10} };
HSegment<int> hseg{ {1, 10}, 5};

// Rectangle properties
auto ll = rect.ll();      // (1, 2)
auto ur = rect.ur();      // (5, 6)
auto area = rect.area();  // 16

// Segment operations
bool on_segment = vseg.contains(Point{5, 3});  // true
auto flipped = vseg.flip();  // HSegment{ {1, 10}, 5}
```

## Project Structure

```
cpp_ai/
├── include/recti/          # Header files
│   ├── generic.hpp         # Generic geometric operations
│   ├── interval.hpp        # Interval class
│   ├── point.hpp           # Point class
│   ├── vector2.hpp         # Vector2 class
│   ├── recti.hpp           # Rectangle and segments
│   ├── polygon.hpp         # Polygon (placeholder)
│   └── ...                 # Other modules
├── src/                    # Example source files
├── tests/                  # Test suite
├── CMakeLists.txt          # CMake build configuration
├── xmake.lua              # xmake build configuration
└── .gitignore             # Git ignore patterns
```

## Dependencies

- **doctest**: Testing framework (automatically downloaded)
- **C++ Standard Library**: No external dependencies required

## Development

### Adding New Modules

1. Create header file in `include/recti/`
2. Implement C++23 concepts and constexpr where possible
3. Add tests in `tests/main.cpp`
4. Update `include/recti.hpp` to include new module

### Testing Guidelines

- Use doctest for unit tests
- Test both compile-time (constexpr) and runtime behavior
- Include edge cases and error conditions
- Follow existing test patterns

## License

Same as the original `physdes-py` project.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Acknowledgments

- Based on the Python `physdes-py` library
- Uses doctest for testing (https://github.com/doctest/doctest)
- Inspired by VLSI physical design algorithms
