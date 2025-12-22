#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <doctest/doctest.h>

#include "recti.hpp"
#include <vector>

TEST_CASE("Interval basic operations") {
    using namespace recti;
    
    Interval<int> interval1{1, 5};
    Interval<int> interval2{3, 7};
    Interval<int> interval3{6, 8};
    
    CHECK(interval1.overlaps(interval2));
    CHECK(!interval1.overlaps(interval3));
    CHECK(interval1.width() == 4);
    CHECK(interval2.width() == 4);
    CHECK(interval1.contains(3));
    CHECK(!interval1.contains(6));
    CHECK(interval1.min_dist_with(interval2) == 0);
    CHECK(interval1.min_dist_with(interval3) == 1);  // 6 - 5 = 1
    CHECK(interval1.get_center() == 3);
    CHECK(interval1.measure() == 4);
}

TEST_CASE("Point basic operations") {
    using namespace recti;
    
    Point<int> point1{3, 4};
    Point<int> point2{3, 4};
    Point<int> point3{5, 6};
    
    CHECK(point1.overlaps(point2));
    CHECK(!point1.overlaps(point3));
    CHECK(point1.x() == 3);
    CHECK(point1.y() == 4);
    CHECK(point1.width() == 1);
    CHECK(point1.height() == 1);
    CHECK(point1.area() == 1);
    CHECK(point1.min_dist_with(point3) == 4);  // |5-3| + |6-4| = 2 + 2 = 4
    CHECK(point1.get_center() == point1);
}

TEST_CASE("Vector2 basic operations") {
    using namespace recti;
    
    Vector2<int> v1{1, 2};
    Vector2<int> v2{3, 4};
    Vector2<int> v3 = v1 + v2;
    
    CHECK(v3.x() == 4);
    CHECK(v3.y() == 6);
    
    Vector2<int> v4 = v2 - v1;
    CHECK(v4.x() == 2);
    CHECK(v4.y() == 2);
    
    Vector2<int> v5 = v1 * 2;
    CHECK(v5.x() == 2);
    CHECK(v5.y() == 4);
    
    Vector2<int> v6 = 2 * v1;
    CHECK(v6.x() == 2);
    CHECK(v6.y() == 4);
    
    CHECK(v1.dot(v2) == 11);  // 1*3 + 2*4 = 3 + 8 = 11
    CHECK(v1.cross(v2) == -2);  // 1*4 - 2*3 = 4 - 6 = -2
    CHECK(v1.manhattan_length() == 3);  // |1| + |2| = 3
    CHECK(v1.length_squared() == 5);  // 1*1 + 2*2 = 5
}

TEST_CASE("Rectangle basic operations") {
    using namespace recti;
    
    Rectangle<int> rect1{Interval<int>{1, 5}, Interval<int>{2, 6}};
    Rectangle<int> rect2{Interval<int>{3, 7}, Interval<int>{4, 8}};
    Rectangle<int> rect3{Interval<int>{10, 15}, Interval<int>{10, 15}};
    
    CHECK(rect1.overlaps(rect2));
    CHECK(!rect1.overlaps(rect3));
    
    auto ll = rect1.ll();
    CHECK(ll.x() == 1);
    CHECK(ll.y() == 2);
    
    auto ur = rect1.ur();
    CHECK(ur.x() == 5);
    CHECK(ur.y() == 6);
    
    CHECK(rect1.width() == 4);
    CHECK(rect1.height() == 4);
    CHECK(rect1.area() == 16);
    
    auto center = rect1.get_center();
    CHECK(center.x() == 3);
    CHECK(center.y() == 4);
}

TEST_CASE("Generic functions") {
    using namespace recti;
    
    Interval<int> interval1{1, 5};
    Interval<int> interval2{3, 7};
    
    CHECK(overlap(interval1, interval2));
    CHECK(!contain(interval1, interval2));
    
    auto dist = min_dist(interval1, interval2);
    CHECK(dist == 0);  // They overlap
    
    Interval<int> interval3{10, 15};
    auto dist2 = min_dist(interval1, interval3);
    CHECK(dist2 == 5);  // 10 - 5 = 5
    
    CHECK(measure_of(interval1) == 4);
    CHECK(center(interval1) == 3);
    CHECK(lower(interval1) == 1);
    CHECK(upper(interval1) == 5);
}

TEST_CASE("Segments") {
    using namespace recti;
    
    VSegment<int> vseg{5, Interval<int>{1, 10}};
    HSegment<int> hseg{Interval<int>{1, 10}, 5};
    
    Point<int> point_on_vseg{5, 3};
    Point<int> point_on_hseg{3, 5};
    
    CHECK(vseg.contains(point_on_vseg));
    CHECK(hseg.contains(point_on_hseg));
    
    auto flipped_vseg = vseg.flip();
    CHECK(flipped_vseg.x_interval() == vseg.y_interval());
    CHECK(flipped_vseg.y() == vseg.x());
    
    auto flipped_hseg = hseg.flip();
    CHECK(flipped_hseg.x() == hseg.y());
    CHECK(flipped_hseg.y_interval() == hseg.x_interval());
}

TEST_CASE("Nearest point search") {
    using namespace recti;
    
    Point<int> reference{3, 4};
    std::vector<Point<int>> candidates = {
        Point<int>{1, 1},
        Point<int>{5, 5},
        Point<int>{3, 3},
        Point<int>{10, 10}
    };
    
    auto nearest = nearest_point_to(reference, candidates);
    REQUIRE(nearest != nullptr);
    CHECK(*nearest == Point<int>{3, 3});  // Closest point
    
    // Test with empty candidates
    std::vector<Point<int>> empty;
    CHECK(nearest_point_to(reference, empty) == nullptr);
}

TEST_CASE("Hull and enlarge operations") {
    using namespace recti;
    
    Interval<int> interval{3, 7};
    auto enlarged = enlarge(interval, 2);
    CHECK(enlarged.lb() == 1);
    CHECK(enlarged.ub() == 9);
    
    auto hull_interval = hull(interval, 10);
    CHECK(hull_interval.lb() == 3);
    CHECK(hull_interval.ub() == 10);
    
    Point<int> point1{3, 4};
    Point<int> point2{5, 6};
    auto [x_hull, y_hull] = point1.hull_with(point2);
    CHECK(x_hull.lb() == 3);
    CHECK(x_hull.ub() == 5);
    CHECK(y_hull.lb() == 4);
    CHECK(y_hull.ub() == 6);
    
    auto [x_enlarged, y_enlarged] = point1.enlarge(2);
    CHECK(x_enlarged.lb() == 1);
    CHECK(x_enlarged.ub() == 5);
    CHECK(y_enlarged.lb() == 2);
    CHECK(y_enlarged.ub() == 6);
}