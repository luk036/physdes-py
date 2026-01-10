#pragma once

#include "interval.hpp"

#include <algorithm>  // import std::min, std::max
#include <cmath>      // for std::abs
#include <concepts>
#include <iostream>
#include <type_traits>
#include <vector>

namespace recti {
    /**
     * @brief A class representing a point in 2D space.
     *
     * @tparam T The type of the point coordinates (must be arithmetic).
     */
    template <typename T>
    class Point {
      public:
        /**
         * @brief Default constructor. Creates point at (0, 0).
         */
        constexpr Point() : x_{0}, y_{0} {}

        /**
         * @brief Constructor with x and y coordinates.
         *
         * @param x The x-coordinate.
         * @param y The y-coordinate.
         */
        constexpr Point(T x, T y) : x_{x}, y_{y} {}

        /**
         * @brief Get the x-coordinate.
         *
         * @return The x-coordinate.
         */
        [[nodiscard]] constexpr auto x() const -> T { return x_; }

        /**
         * @brief Get the y-coordinate.
         *
         * @return The y-coordinate.
         */
        [[nodiscard]] constexpr auto y() const -> T { return y_; }

        /**
         * @brief Get the width of the point (always 1).
         *
         * @return 1.
         */
        [[nodiscard]] constexpr auto width() const -> T { return T{1}; }

        /**
         * @brief Get the height of the point (always 1).
         *
         * @return 1.
         */
        [[nodiscard]] constexpr auto height() const -> T { return T{1}; }

        /**
         * @brief Get the area of the point (always 1).
         *
         * @return 1.
         */
        [[nodiscard]] constexpr auto area() const -> T { return T{1}; }

        /**
         * @brief Check if this point overlaps with another point.
         *
         * @param other The other point.
         * @return True if points are equal, false otherwise.
         */
        [[nodiscard]] constexpr auto overlaps(const Point& other) const -> bool {
            return x_ == other.x_ && y_ == other.y_;
        }

        /**
         * @brief Check if this point contains another point.
         *
         * @param other The other point.
         * @return True if points are equal, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(const Point& other) const -> bool {
            return overlaps(other);
        }

        /**
         * @brief Check if this point contains a scalar value.
         *
         * @param value The scalar value.
         * @return True if both coordinates equal the value, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(T value) const -> bool {
            return x_ == value && y_ == value;
        }

        /**
         * @brief Compute the minimum Manhattan distance to another point.
         *
         * @param other The other point.
         * @return The Manhattan distance.
         */
        [[nodiscard]] constexpr auto min_dist_with(const Point& other) const -> T {
            return std::abs(x_ - other.x_) + std::abs(y_ - other.y_);
        }

        /**
         * @brief Get the center of the point (the point itself).
         *
         * @return This point.
         */
        [[nodiscard]] constexpr auto get_center() const -> Point { return *this; }

        /**
         * @brief Get the measure (area) of the point.
         *
         * @return 1.
         */
        [[nodiscard]] constexpr auto measure() const -> T { return area(); }

        /**
         * @brief Get the lower corner (the point itself).
         *
         * @return This point.
         */
        [[nodiscard]] constexpr auto lower_corner() const -> Point { return *this; }

        /**
         * @brief Get the upper corner (the point itself).
         *
         * @return This point.
         */
        [[nodiscard]] constexpr auto upper_corner() const -> Point { return *this; }

        /**
         * @brief Create a hull (bounding box) with another point.
         *
         * @param other The other point.
         * @return A pair of intervals representing the bounding box.
         */
        [[nodiscard]] constexpr auto hull_with(const Point& other) const
            -> std::pair<Interval<T>, Interval<T>> {
            return {Interval<T>{std::min(x_, other.x_), std::max(x_, other.x_)},
                    Interval<T>{std::min(y_, other.y_), std::max(y_, other.y_)}};
        }

        /**
         * @brief Enlarge the point by a given amount to create a rectangle.
         *
         * @param amount The amount to enlarge by.
         * @return A pair of intervals representing the enlarged rectangle.
         */
        [[nodiscard]] constexpr auto enlarge(T amount) const
            -> std::pair<Interval<T>, Interval<T>> {
            return {Interval<T>{x_ - amount, x_ + amount},
                    Interval<T>{y_ - amount, y_ + amount}};
        }

        /**
         * @brief Equality operator.
         *
         * @param other The other point.
         * @return True if points are equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator==(const Point& other) const -> bool {
            return x_ == other.x_ && y_ == other.y_;
        }

        /**
         * @brief Inequality operator.
         *
         * @param other The other point.
         * @return True if points are not equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator!=(const Point& other) const -> bool {
            return !(*this == other);
        }

        /**
         * @brief Add a vector to the point.
         *
         * @param vec The vector to add.
         * @return The translated point.
         */
        template <typename U>
        [[nodiscard]] constexpr auto operator+(const Point<U>& vec) const -> Point {
            return Point{x_ + vec.x(), y_ + vec.y()};
        }

        /**
         * @brief Subtract a vector from the point.
         *
         * @param vec The vector to subtract.
         * @return The translated point.
         */
        template <typename U>
        [[nodiscard]] constexpr auto operator-(const Point<U>& vec) const -> Point {
            return Point{x_ - vec.x(), y_ - vec.y()};
        }

        /**
         * @brief Subtract another point to get a vector.
         *
         * @param other The other point.
         * @return The vector from other to this point.
         */
        [[nodiscard]] constexpr auto operator-(const Point& other) const -> Point {
            return Point{x_ - other.x_, y_ - other.y_};
        }

        /**
         * @brief Output stream operator.
         *
         * @param os The output stream.
         * @param point The point to output.
         * @return The output stream.
         */
        friend auto operator<<(std::ostream& os, const Point& point) -> std::ostream& {
            return os << '(' << point.x_ << ", " << point.y_ << ')';
        }

      private:
        T x_;  ///< x-coordinate
        T y_;  ///< y-coordinate
    };

    /**
     * @brief Find the nearest point to a given point from a set of candidates.
     *
     * @tparam T The type of the point coordinates.
     * @param point The reference point.
     * @param candidates The list of candidate points.
     * @return Pointer to the nearest point, or nullptr if candidates is empty.
     */
    template <typename T>
    [[nodiscard]] constexpr auto nearest_point_to(const Point<T>& point,
                                                  const std::vector<Point<T>>& candidates)
        -> const Point<T>* {
        if (candidates.empty()) {
            return nullptr;
        }

        const Point<T>* nearest = &candidates[0];
        T min_dist = point.min_dist_with(*nearest);

        for (size_t i = 1; i < candidates.size(); ++i) {
            T dist = point.min_dist_with(candidates[i]);
            if (dist < min_dist) {
                min_dist = dist;
                nearest = &candidates[i];
            }
        }

        return nearest;
    }

}  // namespace recti
