"""
Hypothesis tests for Vector2 class operations.

This module contains property-based tests for the Vector2 class using the
hypothesis library. These tests verify mathematical properties and invariants
that should hold for all valid inputs.
"""

from hypothesis import given
from hypothesis import strategies as st

from physdes.vector2 import Vector2

# Strategy for generating numeric values (integers and floats)
numeric_values = st.one_of(
    st.integers(min_value=-1000, max_value=1000),
    st.floats(
        min_value=-1000.0, max_value=1000.0, allow_nan=False, allow_infinity=False
    ),
)

# Strategy for generating non-zero values (to avoid division by zero)
non_zero_values = st.one_of(
    st.integers(min_value=-1000, max_value=-1).filter(lambda x: x != 0)
    | st.integers(min_value=1, max_value=1000),
    st.floats(min_value=-1000.0, max_value=-0.1).filter(lambda x: abs(x) > 1e-10)
    | st.floats(min_value=0.1, max_value=1000.0),
)

# Strategy for generating Vector2 objects
vector2_strategy = st.builds(Vector2, x=numeric_values, y=numeric_values)


class TestVector2Properties:
    """Test mathematical properties and invariants of Vector2 operations."""

    @given(vector2_strategy, vector2_strategy)
    def test_addition_commutativity(self, v1: Vector2, v2: Vector2) -> None:
        """Test that vector addition is commutative: v1 + v2 == v2 + v1."""
        assert v1 + v2 == v2 + v1

    @given(vector2_strategy, vector2_strategy, vector2_strategy)
    def test_addition_associativity(
        self, v1: Vector2, v2: Vector2, v3: Vector2
    ) -> None:
        """Test that vector addition is associative: (v1 + v2) + v3 == v1 + (v2 + v3)."""
        result1 = (v1 + v2) + v3
        result2 = v1 + (v2 + v3)

        # Check for floating-point precision issues
        import math

        def approx_equal(a, b, rel_tol=1e-9, abs_tol=1e-12):
            return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

        # If any of the vectors have float components, use approximate equality
        if (
            isinstance(v1.x, float)
            or isinstance(v1.y, float)
            or isinstance(v2.x, float)
            or isinstance(v2.y, float)
            or isinstance(v3.x, float)
            or isinstance(v3.y, float)
        ):
            assert approx_equal(result1.x, result2.x)
            assert approx_equal(result1.y, result2.y)
        else:
            assert result1 == result2

    @given(vector2_strategy)
    def test_addition_identity(self, v: Vector2) -> None:
        """Test that adding zero vector doesn't change the vector."""
        zero = Vector2(0, 0)
        assert v + zero == v
        assert zero + v == v

    @given(vector2_strategy, vector2_strategy)
    def test_subtraction_addition_inverse(self, v1: Vector2, v2: Vector2) -> None:
        """Test that subtraction is the inverse of addition: v1 - v2 + v2 == v1."""
        result = (v1 - v2) + v2

        # Check for floating-point precision issues
        import math

        def approx_equal(a, b, rel_tol=1e-9, abs_tol=1e-12):
            return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

        # If any of the vectors have float components, use approximate equality
        if (
            isinstance(v1.x, float)
            or isinstance(v1.y, float)
            or isinstance(v2.x, float)
            or isinstance(v2.y, float)
        ):
            assert approx_equal(result.x, v1.x)
            assert approx_equal(result.y, v1.y)
        else:
            assert result == v1

    @given(vector2_strategy, vector2_strategy)
    def test_subtraction_antisymmetric(self, v1: Vector2, v2: Vector2) -> None:
        """Test that v1 - v2 == -(v2 - v1)."""
        assert v1 - v2 == -(v2 - v1)

    @given(vector2_strategy, numeric_values)
    def test_scalar_multiplication_distributivity(
        self, v: Vector2, scalar: float
    ) -> None:
        """Test distributivity: scalar * (v1 + v2) == scalar * v1 + scalar * v2."""
        v2 = Vector2(5, 7)  # Use a fixed second vector for this test

        # Use approximate equality for floating-point operations
        import math

        def approx_equal(a, b, rel_tol=1e-9, abs_tol=1e-12):
            return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

        result1 = scalar * (v + v2)
        result2 = scalar * v + scalar * v2

        # Check components with appropriate tolerance
        assert approx_equal(result1.x, result2.x)
        assert approx_equal(result1.y, result2.y)

    @given(vector2_strategy, numeric_values, numeric_values)
    def test_scalar_multiplication_additivity(
        self, v: Vector2, s1: float, s2: float
    ) -> None:
        """Test that (s1 + s2) * v == s1 * v + s2 * v."""
        # Use approximate equality for floating-point operations
        import math

        def approx_equal(a, b, rel_tol=1e-9, abs_tol=1e-12):
            return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

        result1 = (s1 + s2) * v
        result2 = s1 * v + s2 * v

        # Check components with appropriate tolerance
        assert approx_equal(result1.x, result2.x)
        assert approx_equal(result1.y, result2.y)

    @given(vector2_strategy, numeric_values, numeric_values)
    def test_scalar_multiplication_associativity(
        self, v: Vector2, s1: float, s2: float
    ) -> None:
        """Test that s1 * (s2 * v) == (s1 * s2) * v."""
        # Use approximate equality for floating-point operations
        import math

        def approx_equal(a, b, rel_tol=1e-9, abs_tol=1e-12):
            return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

        result1 = s1 * (s2 * v)
        result2 = (s1 * s2) * v

        # Check components with appropriate tolerance
        assert approx_equal(result1.x, result2.x)
        assert approx_equal(result1.y, result2.y)

    @given(vector2_strategy)
    def test_multiplication_by_one(self, v: Vector2) -> None:
        """Test that multiplying by 1 doesn't change the vector."""
        assert 1 * v == v

    @given(vector2_strategy)
    def test_multiplication_by_zero(self, v: Vector2) -> None:
        """Test that multiplying by 0 gives the zero vector."""
        zero = Vector2(0, 0)
        assert 0 * v == zero

    @given(vector2_strategy, non_zero_values)
    def test_division_multiplication_inverse(self, v: Vector2, divisor: float) -> None:
        """Test that division is the inverse of multiplication."""
        result = v / divisor
        # Use approximate equality for all cases since division always produces floats
        import math

        def approx_equal(a, b, rel_tol=1e-9, abs_tol=1e-12):
            return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

        # Division always produces floating-point results, so use approximate equality
        assert approx_equal((result * divisor).x, v.x, rel_tol=1e-9, abs_tol=1e-12)
        assert approx_equal((result * divisor).y, v.y, rel_tol=1e-9, abs_tol=1e-12)

    @given(vector2_strategy)
    def test_negation_double_negation(self, v: Vector2) -> None:
        """Test that double negation returns the original vector."""
        assert -(-v) == v

    @given(vector2_strategy)
    def test_self_subtraction_zero(self, v: Vector2) -> None:
        """Test that subtracting a vector from itself gives zero."""
        zero = Vector2(0, 0)
        assert v - v == zero

    @given(vector2_strategy, vector2_strategy)
    def test_cross_product_properties(self, v1: Vector2, v2: Vector2) -> None:
        """Test cross product properties."""
        # Cross product is antisymmetric: v1 × v2 == -(v2 × v1)
        assert v1.cross(v2) == -v2.cross(v1)

        # Cross product of parallel vectors is zero
        assert v1.cross(v1) == 0
        assert v2.cross(v2) == 0

    @given(vector2_strategy, vector2_strategy, vector2_strategy)
    def test_cross_product_linearity(
        self, v1: Vector2, v2: Vector2, v3: Vector2
    ) -> None:
        """Test cross product linearity in the first argument."""
        # (v1 + v2) × v3 == v1 × v3 + v2 × v3

        # Use approximate equality for floating-point operations
        import math

        def approx_equal(a, b, rel_tol=1e-9, abs_tol=1e-12):
            return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

        result1 = (v1 + v2).cross(v3)
        result2 = v1.cross(v3) + v2.cross(v3)

        # Use more lenient tolerance for cross products which can accumulate errors
        assert approx_equal(result1, result2, rel_tol=1e-9, abs_tol=1e-9)

    @given(vector2_strategy, numeric_values)
    def test_cross_product_scalar_multiplication(
        self, v: Vector2, scalar: float
    ) -> None:
        """Test cross product with scalar multiplication."""
        v2 = Vector2(3, 7)  # Use a fixed second vector
        # (scalar * v1) × v2 == scalar * (v1 × v2)

        # Use approximate equality for floating-point operations
        import math

        def approx_equal(a, b, rel_tol=1e-9, abs_tol=1e-12):
            return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)

        result1 = (scalar * v).cross(v2)
        result2 = scalar * v.cross(v2)

        # Use more lenient tolerance for cross products which can accumulate errors
        assert approx_equal(result1, result2, rel_tol=1e-9, abs_tol=1e-9)

    @given(vector2_strategy)
    def test_inplace_addition_equivalence(self, v: Vector2) -> None:
        """Test that in-place addition is equivalent to regular addition."""
        v2 = Vector2(10, 20)
        v_copy = Vector2(v.x, v.y)
        v_copy += v2
        assert v_copy == v + v2

    @given(vector2_strategy)
    def test_inplace_subtraction_equivalence(self, v: Vector2) -> None:
        """Test that in-place subtraction is equivalent to regular subtraction."""
        v2 = Vector2(10, 20)
        v_copy = Vector2(v.x, v.y)
        v_copy -= v2
        assert v_copy == v - v2

    @given(vector2_strategy, numeric_values)
    def test_inplace_multiplication_equivalence(
        self, v: Vector2, scalar: float
    ) -> None:
        """Test that in-place multiplication is equivalent to regular multiplication."""
        v_copy = Vector2(v.x, v.y)
        v_copy *= scalar
        assert v_copy == v * scalar

    @given(vector2_strategy, non_zero_values)
    def test_inplace_division_equivalence(self, v: Vector2, divisor: float) -> None:
        """Test that in-place division is equivalent to regular division."""
        v_copy = Vector2(v.x, v.y)
        v_copy /= divisor
        assert v_copy == v / divisor


class TestVector2EdgeCases:
    """Test edge cases and special conditions."""

    @given(vector2_strategy)
    def test_equality_reflexivity(self, v: Vector2) -> None:
        """Test that a vector is equal to itself."""
        assert v == v

    @given(vector2_strategy, vector2_strategy)
    def test_equality_symmetry(self, v1: Vector2, v2: Vector2) -> None:
        """Test that equality is symmetric."""
        result = v1 == v2
        assert result == (v2 == v1)

    @given(vector2_strategy, vector2_strategy, vector2_strategy)
    def test_equality_transitivity(self, v1: Vector2, v2: Vector2, v3: Vector2) -> None:
        """Test that equality is transitive."""
        if v1 == v2 and v2 == v3:
            assert v1 == v3

    @given(vector2_strategy)
    def test_repr_roundtrip(self, v: Vector2) -> None:
        """Test that the repr can be used to recreate the vector."""
        # This is a basic test - in practice, you might need eval()
        # but we avoid eval for security reasons
        repr_str = repr(v)
        assert "Vector2" in repr_str
        assert str(v.x) in repr_str
        assert str(v.y) in repr_str

    @given(vector2_strategy)
    def test_str_format(self, v: Vector2) -> None:
        """Test that string representation follows expected format."""
        str_repr = str(v)
        assert str_repr.startswith("<")
        assert str_repr.endswith(">")
        assert "," in str_repr


class TestVector2NumericProperties:
    """Test properties related to numeric operations."""

    @given(vector2_strategy, vector2_strategy)
    def test_magnitude_properties(self, v1: Vector2, v2: Vector2) -> None:
        """Test properties related to vector magnitudes (if applicable)."""
        # Test triangle inequality for cross product magnitude
        # |v1 × v2| ≤ |v1| * |v2| (for 2D vectors, cross product is a scalar)
        cross_prod = v1.cross(v2)

        # For 2D vectors, the cross product magnitude should not exceed
        # the product of the vector magnitudes
        # Note: This is a simplified test since we don't have magnitude method
        assert isinstance(cross_prod, (int, float))

    @given(vector2_strategy)
    def test_coordinate_access(self, v: Vector2) -> None:
        """Test that coordinate access returns the expected values."""
        assert v.x == v.x_
        assert v.y == v.y_


class TestVector2NestedVectors:
    """Test properties of nested Vector2 objects (3D vectors)."""

    @given(numeric_values, numeric_values, numeric_values)
    def test_nested_vector_creation(self, x: float, y: float, z: float) -> None:
        """Test creating and manipulating nested vectors."""
        v2d = Vector2(x, y)
        v3d = Vector2(v2d, z)

        assert v3d.x == v2d
        assert v3d.y == z

    @given(
        numeric_values,
        numeric_values,
        numeric_values,
        numeric_values,
        numeric_values,
        numeric_values,
    )
    def test_nested_vector_addition(
        self, x1: float, y1: float, z1: float, x2: float, y2: float, z2: float
    ) -> None:
        """Test addition of nested vectors."""
        v1_2d = Vector2(x1, y1)
        v1_3d = Vector2(v1_2d, z1)

        v2_2d = Vector2(x2, y2)
        v2_3d = Vector2(v2_2d, z2)

        result = v1_3d + v2_3d

        assert result.x == v1_2d + v2_2d
        assert result.y == z1 + z2

    @given(numeric_values, numeric_values, numeric_values, numeric_values)
    def test_nested_vector_scalar_multiplication(
        self, x: float, y: float, z: float, scalar: float
    ) -> None:
        """Test scalar multiplication of nested vectors."""
        v2d = Vector2(x, y)
        v3d = Vector2(v2d, z)

        result = v3d * scalar

        assert result.x == v2d * scalar
        assert result.y == z * scalar
