#pragma once

#include "generic.hpp"

#include <algorithm>  // import std::min, std::max
#include <cassert>
#include <cmath>      // for std::abs
#include <concepts>
#include <iostream>
#include <type_traits>

namespace recti {
    /**
     * @brief A class representing an interval [lb, ub].
     *
     * @tparam T The type of the interval bounds (must be arithmetic).
     */
    template <typename T>
    class Interval {
      public:
        /**
         * @brief Default constructor. Creates an invalid interval [1, 0].
         */
        constexpr Interval() : lb_{1}, ub_{0} {}

        /**
         * @brief Constructor with lower and upper bounds.
         *
         * @param lb The lower bound.
         * @param ub The upper bound.
         */
        constexpr Interval(T lb, T ub) : lb_{lb}, ub_{ub} {}

        /**
         * @brief Get the lower bound.
         *
         * @return The lower bound.
         */
        [[nodiscard]] constexpr auto lb() const -> T { return lb_; }

        /**
         * @brief Get the upper bound.
         *
         * @return The upper bound.
         */
        [[nodiscard]] constexpr auto ub() const -> T { return ub_; }

        /**
         * @brief Check if the interval is invalid (lb > ub).
         *
         * @return True if the interval is invalid, false otherwise.
         */
        [[nodiscard]] constexpr auto is_invalid() const -> bool { return lb_ > ub_; }

        /**
         * @brief Check if the interval is valid (lb <= ub).
         *
         * @return True if the interval is valid, false otherwise.
         */
        [[nodiscard]] constexpr auto is_valid() const -> bool { return lb_ <= ub_; }

        /**
         * @brief Get the width of the interval (ub - lb).
         *
         * @return The width of the interval.
         */
        [[nodiscard]] constexpr auto width() const -> T { return ub_ - lb_; }

        /**
         * @brief Check if the interval is empty (width == 0).
         *
         * @return True if the interval is empty, false otherwise.
         */
        [[nodiscard]] constexpr auto is_empty() const -> bool { return lb_ == ub_; }

        /**
         * @brief Check if this interval overlaps with another interval.
         *
         * @param other The other interval.
         * @return True if the intervals overlap, false otherwise.
         */
        [[nodiscard]] constexpr auto overlaps(const Interval& other) const -> bool {
            return lb_ <= other.ub_ && other.lb_ <= ub_;
        }

        /**
         * @brief Check if this interval overlaps with a scalar value.
         *
         * @param value The scalar value.
         * @return True if the interval contains the value, false otherwise.
         */
        [[nodiscard]] constexpr auto overlaps(T value) const -> bool {
            return lb_ <= value && value <= ub_;
        }

        /**
         * @brief Check if this interval contains another interval.
         *
         * @param other The other interval.
         * @return True if this interval contains the other, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(const Interval& other) const -> bool {
            return lb_ <= other.lb_ && other.ub_ <= ub_;
        }

        /**
         * @brief Check if this interval contains a scalar value.
         *
         * @param value The scalar value.
         * @return True if the interval contains the value, false otherwise.
         */
        [[nodiscard]] constexpr auto contains(T value) const -> bool {
            return lb_ <= value && value <= ub_;
        }

        /**
         * @brief Compute the intersection with another interval.
         *
         * @param other The other interval.
         * @return The intersection interval, or an invalid interval if they don't overlap.
         */
        [[nodiscard]] constexpr auto intersect_with(const Interval& other) const -> Interval {
            if (overlaps(other)) {
                return Interval{std::max(lb_, other.lb_), std::min(ub_, other.ub_)};
            }
            return Interval{};  // Invalid interval
        }

        /**
         * @brief Compute the minimum Manhattan distance to another interval.
         *
         * @param other The other interval.
         * @return The minimum distance.
         */
        [[nodiscard]] constexpr auto min_dist_with(const Interval& other) const -> T {
            if (overlaps(other)) {
                return T{0};
            }
            if (ub_ < other.lb_) {
                return other.lb_ - ub_;
            }
            return lb_ - other.ub_;
        }

        /**
         * @brief Compute the minimum Manhattan distance to a scalar value.
         *
         * @param value The scalar value.
         * @return The minimum distance.
         */
        [[nodiscard]] constexpr auto min_dist_with(T value) const -> T {
            if (contains(value)) {
                return T{0};
            }
            if (value < lb_) {
                return lb_ - value;
            }
            return value - ub_;
        }

        /**
         * @brief Get the center of the interval.
         *
         * @return The center point.
         */
        [[nodiscard]] constexpr auto get_center() const -> T { return (lb_ + ub_) / 2; }

        /**
         * @brief Get the measure (width) of the interval.
         *
         * @return The width.
         */
        [[nodiscard]] constexpr auto measure() const -> T { return width(); }

        /**
         * @brief Get the lower corner (same as lb).
         *
         * @return The lower bound.
         */
        [[nodiscard]] constexpr auto lower_corner() const -> T { return lb_; }

        /**
         * @brief Get the upper corner (same as ub).
         *
         * @return The upper bound.
         */
        [[nodiscard]] constexpr auto upper_corner() const -> T { return ub_; }

        /**
         * @brief Create a hull (smallest containing interval) with another interval.
         *
         * @param other The other interval.
         * @return The hull interval.
         */
        [[nodiscard]] constexpr auto hull_with(const Interval& other) const -> Interval {
            return Interval{std::min(lb_, other.lb_), std::max(ub_, other.ub_)};
        }

        /**
         * @brief Create a hull with a scalar value.
         *
         * @param value The scalar value.
         * @return The hull interval.
         */
        [[nodiscard]] constexpr auto hull_with(T value) const -> Interval {
            return Interval{std::min(lb_, value), std::max(ub_, value)};
        }

        /**
         * @brief Enlarge the interval by a given amount on both sides.
         *
         * @param amount The amount to enlarge by.
         * @return The enlarged interval.
         */
        [[nodiscard]] constexpr auto enlarge(T amount) const -> Interval {
            return Interval{lb_ - amount, ub_ + amount};
        }

        /**
         * @brief Equality operator.
         *
         * @param other The other interval.
         * @return True if intervals are equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator==(const Interval& other) const -> bool {
            return lb_ == other.lb_ && ub_ == other.ub_;
        }

        /**
         * @brief Inequality operator.
         *
         * @param other The other interval.
         * @return True if intervals are not equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator!=(const Interval& other) const -> bool {
            return !(*this == other);
        }

        /**
         * @brief Add a scalar to the interval (translation).
         *
         * @param value The scalar to add.
         * @return The translated interval.
         */
        [[nodiscard]] constexpr auto operator+(T value) const -> Interval {
            return Interval{lb_ + value, ub_ + value};
        }

        /**
         * @brief Subtract a scalar from the interval (translation).
         *
         * @param value The scalar to subtract.
         * @return The translated interval.
         */
        [[nodiscard]] constexpr auto operator-(T value) const -> Interval {
            return Interval{lb_ - value, ub_ - value};
        }

        /**
         * @brief Multiply the interval by a scalar (scaling).
         *
         * @param value The scalar to multiply by.
         * @return The scaled interval.
         */
        [[nodiscard]] constexpr auto operator*(T value) const -> Interval {
            return Interval{lb_ * value, ub_ * value};
        }

        /**
         * @brief Output stream operator.
         *
         * @param os The output stream.
         * @param interval The interval to output.
         * @return The output stream.
         */
        friend auto operator<<(std::ostream& os, const Interval& interval) -> std::ostream& {
            return os << '[' << interval.lb_ << ", " << interval.ub_ << ']';
        }

      private:
        T lb_;  ///< Lower bound
        T ub_;  ///< Upper bound
    };

    /**
     * @brief Create the hull (smallest containing interval) of two values.
     *
     * @tparam T The type of the values.
     * @param a First value.
     * @param b Second value.
     * @return The hull interval.
     */
    template <typename T>
    [[nodiscard]] constexpr auto hull(T a, T b) -> Interval<T> {
        return a < b ? Interval<T>{a, b} : Interval<T>{b, a};
    }

    /**
     * @brief Create the hull of an interval and a value.
     *
     * @tparam T The type of the values.
     * @param interval The interval.
     * @param value The value.
     * @return The hull interval.
     */
    template <typename T>
    [[nodiscard]] constexpr auto hull(const Interval<T>& interval, T value) -> Interval<T> {
        return interval.hull_with(value);
    }

    /**
     * @brief Create the hull of a value and an interval.
     *
     * @tparam T The type of the values.
     * @param value The value.
     * @param interval The interval.
     * @return The hull interval.
     */
    template <typename T>
    [[nodiscard]] constexpr auto hull(T value, const Interval<T>& interval) -> Interval<T> {
        return interval.hull_with(value);
    }

    /**
     * @brief Enlarge an interval by a given amount on both sides.
     *
     * @tparam T The type of the values.
     * @param interval The interval to enlarge.
     * @param amount The amount to enlarge by.
     * @return The enlarged interval.
     */
    template <typename T>
    [[nodiscard]] constexpr auto enlarge(const Interval<T>& interval, T amount) -> Interval<T> {
        return interval.enlarge(amount);
    }

}  // namespace recti