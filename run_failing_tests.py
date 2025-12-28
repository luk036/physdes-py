import pytest
import sys
sys.path.insert(0, 'src')

# Run the specific failing tests
result = pytest.main([
    'tests/test_geometric_hypothesis.py::TestPolygonGeometricInvariants::test_triangle_area_properties',
    'tests/test_geometric_hypothesis.py::TestNumericStability::test_interval_arithmetic_stability',
    '-v'
])

print(f"\nExit code: {result}")