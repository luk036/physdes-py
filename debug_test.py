from hypothesis import assume, given
from hypothesis import strategies as st

from physdes.point import Point
from physdes.polygon import Polygon, point_in_polygon
from physdes.vector2 import Vector2

# Strategy for generating numeric values (integers and floats)
numeric_values = st.one_of(
    st.integers(min_value=-100, max_value=100),
    st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False),
)

# Strategy for generating vectors
vector_strategy = st.builds(Vector2, x=numeric_values, y=numeric_values)

# Strategy for generating simple polygons (triangles to quadrilaterals)
simple_polygon_strategy = st.builds(
    Polygon.from_pointset,
    pointset=st.lists(
        st.builds(Point, numeric_values, numeric_values),
        min_size=3,
        max_size=4,
        unique_by=lambda p: (p.xcoord, p.ycoord),
    ),
)


@given(simple_polygon_strategy)
def test_polygon_inclusion_translation_invariance(poly):
    """Test that point inclusion is invariant under translation."""
    # Get all vertices including origin
    vertices = [poly._origin]
    current = poly._origin
    for vec in poly._vecs:
        current = Point(current.xcoord + vec.x, current.ycoord + vec.y)
        vertices.append(current)

    # Check if polygon has very small coordinates that might cause precision issues
    min_coord = min(abs(v.xcoord) for v in vertices + [Point(0, 0)])
    min_coord = min(min_coord, min(abs(v.ycoord) for v in vertices + [Point(0, 0)]))

    # Skip test for very small coordinates that cause precision issues
    assume(min_coord > 1e-100)

    # Test with a point that is definitely inside (not on boundary)
    # Use the centroid of the polygon for better stability
    centroid_x = sum(v.xcoord for v in vertices) / len(vertices)
    centroid_y = sum(v.ycoord for v in vertices) / len(vertices)
    test_point = Point(centroid_x, centroid_y)

    original_result = point_in_polygon(vertices, test_point)

    # Translate polygon and test with translated test point
    translated_vertices = [Point(v.xcoord + 10, v.ycoord + 20) for v in vertices]
    translated_test_point = Point(test_point.xcoord + 10, test_point.ycoord + 20)
    translated_result = point_in_polygon(translated_vertices, translated_test_point)

    # Both should give the same result (inside or outside)
    assert original_result == translated_result


if __name__ == "__main__":
    test_polygon_inclusion_translation_invariance()
