# AGENTS.md - physdes-py

This file guides agentic coding agents working in the physdes-py repository.

## Build/Lint/Test Commands

### Testing
```bash
# Run all tests
pytest

# Run single test
pytest tests/test_module.py::test_function_name

# Run with coverage (already enabled by default)
pytest --cov physdes --cov-report term-missing

# Run tests in specific directory
pytest tests/test_point.py

# Run with verbose output (default)
pytest -v
```

### Linting/Formatting
```bash
# Run pre-commit hooks (includes isort, black, flake8)
pre-commit run --all-files

# Format code with black
black src/physdes tests/

# Sort imports with isort
isort src/physdes tests/

# Run flake8 linting
flake8 src/physdes tests/
```

### Build
```bash
# Build package
python -m build

# Or using tox
tox -e build
```

### Docs
```bash
# Build documentation
sphinx-build -b html docs/ docs/_build/html
```

## Code Style Guidelines

### Imports
- **Standard library imports first**, then third-party, then project imports
- Use explicit `from typing import` statements:
  ```python
  from typing import Any, Generic, TypeVar, Union, Optional, List, Tuple, Dict, Callable, TYPE_CHECKING
  ```
- Use relative imports for project modules:
  ```python
  from .generic import center, contain, displacement
  from .interval import enlarge, hull
  ```
- For Python version compatibility (supports 3.8+):
  ```python
  if sys.version_info[:2] >= (3, 8):
      from importlib.metadata import PackageNotFoundError, version
  else:
      from importlib_metadata import PackageNotFoundError, version
  ```
- Import debugging tools with `# type: ignore`:
  ```python
  from icecream import ic  # type: ignore
  ```

### Formatting
- **Line length**: 188 characters (configured in setup.cfg)
- **Formatter**: Black (version 23.7.0) with line length 188
- **Import sorter**: isort (version 5.12.0)
- **Linting**: flake8 with these exceptions: `E203, W503` (black-compatible)
- **Line endings**: Mixed line endings fixed automatically via pre-commit

### Type Hints
- **Required**: All functions and methods must have type hints
- **Generic types**: Use `TypeVar` and `Generic` for reusable classes:
  ```python
  T = TypeVar("T", int, float)
  class Interval(Generic[T]):
      def __init__(self, lb: T, ub: T) -> None: ...
  ```
- **Union types**: Use pipe syntax for Python 3.10+, `Union` for older:
  ```python
  def min_dist_with(self, obj: Union["Interval[T]", T]) -> T | int:
  ```
- **Forward references**: Use string quotes for types not yet defined:
  ```python
  def __lt__(self, other: "Point[T1, T2]") -> bool:
  ```
- **Ignore sparingly**: Use `# type: ignore` only when unavoidable (e.g., icecream, mywheel imports)

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `Point`, `Interval`, `Vector2`)
- **Functions/Methods**: `snake_case` (e.g., `hull_with`, `min_dist_with`, `get_center`)
- **Variables**: `snake_case` (e.g., `xcoord`, `ycoord`, `lower_bound`)
- **Constants**: `UPPER_SNAKE_CASE` (less common in this codebase)
- **Properties**: Use `@property` for computed attributes:
  ```python
  @property
  def lb(self) -> T:
      return self._lb
  ```
- **Private attributes**: Prefix with underscore (e.g., `_lb`, `_ub`)

### Operator Overloading
- Implement dunder methods for mathematical operations:
  ```python
  def __add__(self, rhs: Union["Interval[T]", T]) -> "Interval[T]":
  def __iadd__(self, rhs: Union["Interval[T]", T]) -> "Interval[T]":
  def __lt__(self, other: Union["Interval[T]", T]) -> bool:
  ```
- Return `NotImplemented` for unsupported type comparisons:
  ```python
  def __eq__(self, other: object) -> bool:
      if not isinstance(other, Point):
          return NotImplemented
      return (self.xcoord, self.ycoord) == (other.xcoord, other.ycoord)
  ```

### Documentation
- **Docstrings required** for all public classes and methods
- **Style**: Google-style or similar (examples show detailed parameter descriptions)
- **Include**: Parameters, return types, and examples:
  ```python
  def hull_with(self, other: "Point[T1, T2]") -> "Point[Any, Any]":
      """
      The `hull_with` function takes another object and returns a new object
      with the hull of the x and y coordinates of both objects.

      :param other: The `other` parameter is an object of the same type as `self`.
      :return: an instance of the same class as `self`.
      """
  ```
- **Examples**: Use doctest format when appropriate:
  ```python
  Examples:
      >>> a = Point(3, 5)
      >>> print(a.hull_with(b))
      ([3, 5], [4, 6])
  ```
- **ASCII art**: Use `svgbob` for geometric diagrams:
  ```python
  .. svgbob::
     :align: center

      .-----------.------.
      | self      |      |
      '-----------'      |
  ```

### Error Handling
- **Minimal explicit error handling** - rely on Python's natural exceptions
- **Use assertions** for preconditions:
  ```python
  assert lhs == rhs
  ```
- **Return invalid objects** when appropriate (e.g., `Interval` with `lb > ub`):
  ```python
  def is_invalid(self) -> bool:
      return self.lb > self.ub
  ```
- Avoid empty catch blocks (`except: pass`)

### Testing
- **Framework**: pytest with doctest support enabled
- **Coverage**: Required (--cov physdes --cov-report term-missing)
- **Property-based testing**: Use hypothesis for complex algorithms
- **Test naming**: `test_` prefix with descriptive names:
  ```python
  def test_point() -> None:
  def test_displacement() -> None:
  def test_hull() -> None:
  ```
- **Assertions**: Use plain `assert` statements
- **Fixtures**: Use `conftest.py` for shared test data (random point generation)

### Code Organization
- **Structure**: `src/physdes/` for source, `tests/` for tests
- **Namespace package**: Use `__init__.py` for version info
- **Separation of concerns**: Core algorithms in dedicated modules (e.g., `dme_algorithm.py`, `global_router.py`)
- **Utility functions**: Generic operations in `generic.py` that work with multiple types via `hasattr()` checks:
  ```python
  def overlap(lhs: Any, rhs: Any) -> bool:
      if hasattr(lhs, "overlaps"):
          result = lhs.overlaps(rhs)
      elif hasattr(rhs, "overlaps"):
          result = rhs.overlaps(lhs)
      else:  # assume scalar
          result = lhs == rhs
      return bool(result)
  ```

### Pre-commit Hooks
- **Required**: All code must pass pre-commit checks before committing
- **Hooks configured**:
  - `trailing-whitespace`
  - `check-added-large-files`
  - `check-ast`
  - `check-merge-conflict`
  - `isort`
  - `black`
  - `flake8`

### Development Guidelines
- **Python version**: Support 3.8+ (based on version checks in `__init__.py`)
- **Dependencies**: Minimal external deps (mywheel, icecream, lds_gen for testing)
- **Backward compatibility**: Use conditional imports for Python < 3.9
- **Documentation**: Docstrings with parameter descriptions and examples
- **Type safety**: Use type hints throughout, avoid `as any` or `@ts-ignore` equivalent

### Example Class Template
```python
from typing import Any, Generic, TypeVar, Union

T = TypeVar("T", int, float)


class ClassName(Generic[T]):
    """
    Brief description of the class.

    This code defines...
    """

    __slots__ = ("_attr1", "_attr2")

    def __init__(self, attr1: T, attr2: T) -> None:
        """
        Initialize the object.

        :param attr1: Description of attr1
        :param attr2: Description of attr2
        """
        self._attr1: T = attr1
        self._attr2: T = attr2

    @property
    def attr1(self) -> T:
        """Return attr1 value."""
        return self._attr1

    def method_name(self, other: Any) -> Any:
        """
        Method description.

        :param other: Description of parameter
        :return: Description of return value
        """
        # Implementation
        pass
```

## Key Project Context

physdes-py implements VLSI physical design algorithms:
- **Rectilinear polygons**: 2D/3D geometric operations
- **Clock tree synthesis**: DME (Deferred Merge Embedding) algorithm
- **Global routing**: Multiple strategies with constraints
- **Steiner forests**: Grid-based routing algorithms
- **Key dependencies**: `mywheel` (dllist), `lds_gen` (Halton sequences), `icecream` (debugging)
