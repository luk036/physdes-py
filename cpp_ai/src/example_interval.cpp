#include "recti.hpp"
#include <iostream>

int main() {
    using namespace recti;

    std::cout << "=== Interval Example ===\n";

    // Create intervals
    Interval<int> interval1{1, 5};
    Interval<int> interval2{3, 7};
    Interval<int> interval3{10, 15};

    std::cout << "interval1 = " << interval1 << '\n';
    std::cout << "interval2 = " << interval2 << '\n';
    std::cout << "interval3 = " << interval3 << '\n';

    // Check overlap
    std::cout << "\nOverlap checks:\n";
    std::cout << "interval1 overlaps interval2: "
              << (interval1.overlaps(interval2) ? "true" : "false") << '\n';
    std::cout << "interval1 overlaps interval3: "
              << (interval1.overlaps(interval3) ? "true" : "false") << '\n';

    // Check containment
    std::cout << "\nContainment checks:\n";
    std::cout << "interval1 contains 3: "
              << (interval1.contains(3) ? "true" : "false") << '\n';
    std::cout << "interval1 contains interval2: "
              << (interval1.contains(interval2) ? "true" : "false") << '\n';

    // Compute distances
    std::cout << "\nDistance calculations:\n";
    std::cout << "min_dist(interval1, interval2) = "
              << min_dist(interval1, interval2) << '\n';
    std::cout << "min_dist(interval1, interval3) = "
              << min_dist(interval1, interval3) << '\n';

    // Compute intersection
    std::cout << "\nIntersection:\n";
    auto intersection = interval1.intersect_with(interval2);
    std::cout << "interval1 ∩ interval2 = " << intersection << '\n';

    // Create hull with scalar values
    std::cout << "\nHull operations:\n";
    auto hull_scalar = hull(1, 10);
    std::cout << "hull(1, 10) = " << hull_scalar << '\n';
    auto hull_with_interval = hull(interval1, 10);
    std::cout << "hull(interval1, 10) = " << hull_with_interval << '\n';

    // Enlarge interval
    std::cout << "\nEnlarge operation:\n";
    auto enlarged = enlarge(interval1, 2);
    std::cout << "enlarge(interval1, 2) = " << enlarged << '\n';

    // Generic functions
    std::cout << "\nGeneric function usage:\n";
    std::cout << "overlap(interval1, interval2) = "
              << (overlap(interval1, interval2) ? "true" : "false") << '\n';
    std::cout << "contain(interval1, 3) = "
              << (contain(interval1, 3) ? "true" : "false") << '\n';
    std::cout << "center(interval1) = " << center(interval1) << '\n';
    std::cout << "measure_of(interval1) = " << measure_of(interval1) << '\n';

    return 0;
}
