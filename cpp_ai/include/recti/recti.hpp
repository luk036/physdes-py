#pragma once

#include "interval.hpp"
#include "point.hpp"
#include "vector2.hpp"

#include <algorithm>  // import std::min, std::max
#include <concepts>
#include <iostream>
#include <type_traits>

namespace recti {
    /**
     * @brief A class representing an axis-aligned rectangle.
     *
     * @tparam T The type of the rectangle coordinates (must be arithmetic).
     */
    template <typename T>
    class Rectangle {
      public:
        /**
         * @brief Default constructor. Creates an invalid rectangle.
         */
        constexpr Rectangle()
            : x_interval_{Interval<T>{1, 0}}, y_interval_{Interval<T>{1, 0}} {}

        /**
         * @brief Constructor with x and y intervals.
         *
         * @param x_interval The x-interval.
         * @param y_interval The y-interval.
         */
        constexpr Rectangle(const Interval<T>& x_interval, const Interval<T>& y_interval)
            : x_interval_{x_interval}, y_interval_{y_interval} {}

        /**
         * @brief Get the x-interval.
         *
         * @return The x-interval.
         */
        [[nodiscard]] constexpr auto x_interval() const -> const Interval<T>& {
            return x_interval_;
        }

        /**
         * @brief Get the y-interval.
         *
         * @return The y-interval.
         */
        [[nodiscard]] constexpr auto y_interval() const -> const Interval<T>& {
            return y_interval_;
        }

        /**
         * @brief Get the lower-left point of the rectangle.
         *
         * @return The lower-left point.
         */
        [[nodiscard]] constexpr auto ll() const -> Point<T> {
            return Point<T>{x_interval_.lb(), y_interval_.lb()};
        }

        /**
         * @brief Get the upper-right point of the rectangle.
         *
         * @return The upper-right point.
         */
        [[nodiscard]] constexpr auto ur() const -> Point<T> {
            return Point<T>{x_interval_.ub(), y_interval_.ub()};
        }

        /**
         * @brief Get the width of the rectangle.
         *
         * @return The width.
         */
        [[nodiscard]] constexpr auto width() const -> T { return x_interval_.width(); }

        /**
         * @brief Get the height of the rectangle.
         *
         * @return The height.
         */
        [[nodiscard]] constexpr auto height() const -> T { return y_interval_.width(); }

        /**
         * @brief Get the area of the rectangle.
         *
         * @return The area.
         */
        [[nodiscard]] constexpr auto area() const -> T { return width() * height(); }

        /**
         * @brief Flip the rectangle (swap x and y intervals).
         *
         * @return The flipped rectangle.
         */
        [[nodiscard]] constexpr auto flip() const -> Rectangle {
            return Rectangle{y_interval_, x_interval_};
        }

        /**
         * @brief Check if this rectangle overlaps with another rectangle.
         *
         * @param other The other rectangle.
         * @return True if rectangles overlap, false otherwise.
         */
        [[nodiscard]] constexpr auto overlaps(const Rectangle& other) const -> bool {
            return x_interval_.overlaps(other.x_interval_) &&
                   y_interval_.overlaps(other.y_interval_);
        }

        /**
         * @brief Check if this rectangle contains another rectangle.
         *
         * @param other The other rectangle.
         * @return True if this rectangle contains the other, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(const Rectangle& other) const -> bool {
            return x_interval_.contains(other.x_interval_) &&
                   y_interval_.contains(other.y_interval_);
        }

        /**
         * @brief Check if this rectangle contains a point.
         *
         * @param point The point.
         * @return True if rectangle contains the point, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(const Point<T>& point) const -> bool {
            return x_interval_.contains(point.x()) && y_interval_.contains(point.y());
        }

        /**
         * @brief Compute the minimum Manhattan distance to another rectangle.
         *
         * @param other The other rectangle.
         * @return The minimum Manhattan distance.
         */
        [[nodiscard]] constexpr auto min_dist_with(const Rectangle& other) const -> T {
            return x_interval_.min_dist_with(other.x_interval_) +
                   y_interval_.min_dist_with(other.y_interval_);
        }

        /**
         * @brief Compute the minimum Manhattan distance to a point.
         *
         * @param point The point.
         * @return The minimum Manhattan distance.
         */
        [[nodiscard]] constexpr auto min_dist_with(const Point<T>& point) const -> T {
            return x_interval_.min_dist_with(point.x()) +
                   y_interval_.min_dist_with(point.y());
        }

        /**
         * @brief Get the center of the rectangle.
         *
         * @return The center point.
         */
        [[nodiscard]] constexpr auto get_center() const -> Point<T> {
            return Point<T>{x_interval_.get_center(), y_interval_.get_center()};
        }

        /**
         * @brief Get the measure (area) of the rectangle.
         *
         * @return The area.
         */
        [[nodiscard]] constexpr auto measure() const -> T { return area(); }

        /**
         * @brief Get the lower corner (lower-left point).
         *
         * @return The lower-left point.
         */
        [[nodiscard]] constexpr auto lower_corner() const -> Point<T> { return ll(); }

        /**
         * @brief Get the upper corner (upper-right point).
         *
         * @return The upper-right point.
         */
        [[nodiscard]] constexpr auto upper_corner() const -> Point<T> { return ur(); }

        /**
         * @brief Equality operator.
         *
         * @param other The other rectangle.
         * @return True if rectangles are equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator==(const Rectangle& other) const -> bool {
            return x_interval_ == other.x_interval_ && y_interval_ == other.y_interval_;
        }

        /**
         * @brief Inequality operator.
         *
         * @param other The other rectangle.
         * @return True if rectangles are not equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator!=(const Rectangle& other) const -> bool {
            return !(*this == other);
        }

        /**
         * @brief Output stream operator.
         *
         * @param os The output stream.
         * @param rect The rectangle to output.
         * @return The output stream.
         */
        friend auto operator<<(std::ostream& os, const Rectangle& rect) -> std::ostream& {
            return os << '(' << rect.x_interval_ << ", " << rect.y_interval_ << ')';
        }

      private:
        Interval<T> x_interval_;  ///< x-interval
        Interval<T> y_interval_;  ///< y-interval
    };

    // Forward declaration of HSegment for VSegment
    template <typename T>
    class HSegment;

    /**
     * @brief A class representing a vertical line segment.
     *
     * @tparam T The type of the segment coordinates (must be arithmetic).
     */
    template <typename T>
    class VSegment {
      public:
        /**
         * @brief Constructor with x-coordinate and y-interval.
         *
         * @param x The x-coordinate.
         * @param y_interval The y-interval.
         */
        constexpr VSegment(T x, const Interval<T>& y_interval)
            : x_{x}, y_interval_{y_interval} {}

        /**
         * @brief Get the x-coordinate.
         *
         * @return The x-coordinate.
         */
        [[nodiscard]] constexpr auto x() const -> T { return x_; }

        /**
         * @brief Get the y-interval.
         *
         * @return The y-interval.
         */
        [[nodiscard]] constexpr auto y_interval() const -> const Interval<T>& {
            return y_interval_;
        }

        /**
         * @brief Flip the segment (vertical to horizontal).
         *
         * @return The flipped segment as an HSegment.
         */
        [[nodiscard]] constexpr auto flip() const -> HSegment<T>;

        /**
         * @brief Check if this segment overlaps with another vertical segment.
         *
         * @param other The other segment.
         * @return True if segments overlap, false otherwise.
         */
        [[nodiscard]] constexpr auto overlaps(const VSegment& other) const -> bool {
            return x_ == other.x_ && y_interval_.overlaps(other.y_interval_);
        }

        /**
         * @brief Check if this segment contains another vertical segment.
         *
         * @param other The other segment.
         * @return True if this segment contains the other, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(const VSegment& other) const -> bool {
            return x_ == other.x_ && y_interval_.contains(other.y_interval_);
        }

        /**
         * @brief Check if this segment contains a point.
         *
         * @param point The point.
         * @return True if segment contains the point, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(const Point<T>& point) const -> bool {
            return x_ == point.x() && y_interval_.contains(point.y());
        }

        /**
         * @brief Equality operator.
         *
         * @param other The other segment.
         * @return True if segments are equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator==(const VSegment& other) const -> bool {
            return x_ == other.x_ && y_interval_ == other.y_interval_;
        }

        /**
         * @brief Inequality operator.
         *
         * @param other The other segment.
         * @return True if segments are not equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator!=(const VSegment& other) const -> bool {
            return !(*this == other);
        }

        /**
         * @brief Output stream operator.
         *
         * @param os The output stream.
         * @param seg The segment to output.
         * @return The output stream.
         */
        friend auto operator<<(std::ostream& os, const VSegment& seg) -> std::ostream& {
            return os << "VSegment(x=" << seg.x_ << ", y=" << seg.y_interval_ << ')';
        }

      private:
        T x_;                     ///< x-coordinate
        Interval<T> y_interval_;  ///< y-interval
    };

    /**
     * @brief A class representing a horizontal line segment.
     *
     * @tparam T The type of the segment coordinates (must be arithmetic).
     */
    template <typename T>
    class HSegment {
      public:
        /**
         * @brief Constructor with x-interval and y-coordinate.
         *
         * @param x_interval The x-interval.
         * @param y The y-coordinate.
         */
        constexpr HSegment(const Interval<T>& x_interval, T y)
            : x_interval_{x_interval}, y_{y} {}

        /**
         * @brief Get the x-interval.
         *
         * @return The x-interval.
         */
        [[nodiscard]] constexpr auto x_interval() const -> const Interval<T>& {
            return x_interval_;
        }

        /**
         * @brief Get the y-coordinate.
         *
         * @return The y-coordinate.
         */
        [[nodiscard]] constexpr auto y() const -> T { return y_; }

        /**
         * @brief Flip the segment (horizontal to vertical).
         *
         * @return The flipped segment as a VSegment.
         */
        [[nodiscard]] constexpr auto flip() const -> VSegment<T> {
            return VSegment<T>{y_, x_interval_};
        }

        /**
         * @brief Check if this segment overlaps with another horizontal segment.
         *
         * @param other The other segment.
         * @return True if segments overlap, false otherwise.
         */
        [[nodiscard]] constexpr auto overlaps(const HSegment& other) const -> bool {
            return y_ == other.y_ && x_interval_.overlaps(other.x_interval_);
        }

        /**
         * @brief Check if this segment contains another horizontal segment.
         *
         * @param other The other segment.
         * @return True if this segment contains the other, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(const HSegment& other) const -> bool {
            return y_ == other.y_ && x_interval_.contains(other.x_interval_);
        }

        /**
         * @brief Check if this segment contains a point.
         *
         * @param point The point.
         * @return True if segment contains the point, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(const Point<T>& point) const -> bool {
            return y_ == point.y() && x_interval_.contains(point.x());
        }

        /**
         * @brief Equality operator.
         *
         * @param other The other segment.
         * @return True if segments are equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator==(const HSegment& other) const -> bool {
            return x_interval_ == other.x_interval_ && y_ == other.y_;
        }

        /**
         * @brief Inequality operator.
         *
         * @param other The other segment.
         * @return True if segments are not equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator!=(const HSegment& other) const -> bool {
            return !(*this == other);
        }

        /**
         * @brief Output stream operator.
         *
         * @param os The output stream.
         * @param seg The segment to output.
         * @return The output stream.
         */
        friend auto operator<<(std::ostream& os, const HSegment& seg) -> std::ostream& {
            return os << "HSegment(x=" << seg.x_interval_ << ", y=" << seg.y_ << ')';
        }

      private:
        Interval<T> x_interval_;  ///< x-interval
        T y_;                     ///< y-coordinate
    };

    // Implement VSegment::flip after HSegment is defined
    template <typename T>
    [[nodiscard]] constexpr auto VSegment<T>::flip() const -> HSegment<T> {
        return HSegment<T>{y_interval_, x_};
    }

}  // namespace recti