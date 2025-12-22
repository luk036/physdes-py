#pragma once

#include <cmath>      // for std::abs, std::sqrt
#include <concepts>
#include <iostream>
#include <type_traits>

namespace recti {
    /**
     * @brief A class representing a 2D vector.
     *
     * @tparam T The type of the vector components (must be arithmetic).
     */
    template <typename T>
    class Vector2 {
      public:
        /**
         * @brief Default constructor. Creates zero vector (0, 0).
         */
        constexpr Vector2() : x_{0}, y_{0} {}

        /**
         * @brief Constructor with x and y components.
         *
         * @param x The x-component.
         * @param y The y-component.
         */
        constexpr Vector2(T x, T y) : x_{x}, y_{y} {}

        /**
         * @brief Get the x-component.
         *
         * @return The x-component.
         */
        [[nodiscard]] constexpr auto x() const -> T { return x_; }

        /**
         * @brief Get the y-component.
         *
         * @return The y-component.
         */
        [[nodiscard]] constexpr auto y() const -> T { return y_; }

        /**
         * @brief Compute the cross product with another vector.
         *
         * @param other The other vector.
         * @return The cross product (scalar in 2D).
         */
        [[nodiscard]] constexpr auto cross(const Vector2& other) const -> T {
            return x_ * other.y_ - y_ * other.x_;
        }

        /**
         * @brief Compute the dot product with another vector.
         *
         * @param other The other vector.
         * @return The dot product.
         */
        [[nodiscard]] constexpr auto dot(const Vector2& other) const -> T {
            return x_ * other.x_ + y_ * other.y_;
        }

        /**
         * @brief Compute the Manhattan length (L1 norm) of the vector.
         *
         * @return The Manhattan length.
         */
        [[nodiscard]] constexpr auto manhattan_length() const -> T {
            return std::abs(x_) + std::abs(y_);
        }

        /**
         * @brief Compute the squared Euclidean length of the vector.
         *
         * @return The squared length.
         */
        [[nodiscard]] constexpr auto length_squared() const -> T {
            return x_ * x_ + y_ * y_;
        }

        /**
         * @brief Compute the Euclidean length of the vector.
         *
         * @return The length.
         */
        [[nodiscard]] auto length() const -> double {
            return std::sqrt(static_cast<double>(length_squared()));
        }

        /**
         * @brief Equality operator.
         *
         * @param other The other vector.
         * @return True if vectors are equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator==(const Vector2& other) const -> bool {
            return x_ == other.x_ && y_ == other.y_;
        }

        /**
         * @brief Inequality operator.
         *
         * @param other The other vector.
         * @return True if vectors are not equal, false otherwise.
         */
        [[nodiscard]] constexpr auto operator!=(const Vector2& other) const -> bool {
            return !(*this == other);
        }

        /**
         * @brief Equality with scalar (both components must equal the scalar).
         *
         * @param value The scalar value.
         * @return True if both components equal the scalar, false otherwise.
         */
        [[nodiscard]] constexpr auto operator==(T value) const -> bool {
            return x_ == value && y_ == value;
        }

        /**
         * @brief Inequality with scalar.
         *
         * @param value The scalar value.
         * @return True if not both components equal the scalar, false otherwise.
         */
        [[nodiscard]] constexpr auto operator!=(T value) const -> bool {
            return !(*this == value);
        }

        /**
         * @brief Add another vector.
         *
         * @param other The other vector.
         * @return The sum vector.
         */
        [[nodiscard]] constexpr auto operator+(const Vector2& other) const -> Vector2 {
            return Vector2{x_ + other.x_, y_ + other.y_};
        }

        /**
         * @brief Subtract another vector.
         *
         * @param other The other vector.
         * @return The difference vector.
         */
        [[nodiscard]] constexpr auto operator-(const Vector2& other) const -> Vector2 {
            return Vector2{x_ - other.x_, y_ - other.y_};
        }

        /**
         * @brief Multiply by a scalar.
         *
         * @param scalar The scalar.
         * @return The scaled vector.
         */
        [[nodiscard]] constexpr auto operator*(T scalar) const -> Vector2 {
            return Vector2{x_ * scalar, y_ * scalar};
        }

        /**
         * @brief Divide by a scalar.
         *
         * @param scalar The scalar.
         * @return The scaled vector.
         */
        [[nodiscard]] constexpr auto operator/(T scalar) const -> Vector2 {
            return Vector2{x_ / scalar, y_ / scalar};
        }

        /**
         * @brief Negate the vector.
         *
         * @return The negated vector.
         */
        [[nodiscard]] constexpr auto operator-() const -> Vector2 {
            return Vector2{-x_, -y_};
        }

        /**
         * @brief Add and assign another vector.
         *
         * @param other The other vector.
         * @return Reference to this vector.
         */
        constexpr auto operator+=(const Vector2& other) -> Vector2& {
            x_ += other.x_;
            y_ += other.y_;
            return *this;
        }

        /**
         * @brief Subtract and assign another vector.
         *
         * @param other The other vector.
         * @return Reference to this vector.
         */
        constexpr auto operator-=(const Vector2& other) -> Vector2& {
            x_ -= other.x_;
            y_ -= other.y_;
            return *this;
        }

        /**
         * @brief Multiply and assign by a scalar.
         *
         * @param scalar The scalar.
         * @return Reference to this vector.
         */
        constexpr auto operator*=(T scalar) -> Vector2& {
            x_ *= scalar;
            y_ *= scalar;
            return *this;
        }

        /**
         * @brief Divide and assign by a scalar.
         *
         * @param scalar The scalar.
         * @return Reference to this vector.
         */
        constexpr auto operator/=(T scalar) -> Vector2& {
            x_ /= scalar;
            y_ /= scalar;
            return *this;
        }

        /**
         * @brief Output stream operator.
         *
         * @param os The output stream.
         * @param vec The vector to output.
         * @return The output stream.
         */
        friend auto operator<<(std::ostream& os, const Vector2& vec) -> std::ostream& {
            return os << '<' << vec.x_ << ", " << vec.y_ << '>';
        }

      private:
        T x_;  ///< x-component
        T y_;  ///< y-component
    };

    /**
     * @brief Multiply a scalar by a vector.
     *
     * @tparam T The type of the scalar and vector components.
     * @param scalar The scalar.
     * @param vec The vector.
     * @return The scaled vector.
     */
    template <typename T>
    [[nodiscard]] constexpr auto operator*(T scalar, const Vector2<T>& vec) -> Vector2<T> {
        return vec * scalar;
    }

    /**
     * @brief Create a zero vector.
     *
     * @tparam T The type of the vector components.
     * @return Zero vector (0, 0).
     */
    template <typename T>
    [[nodiscard]] constexpr auto zero_vector() -> Vector2<T> {
        return Vector2<T>{0, 0};
    }

    /**
     * @brief Create a unit vector in the x-direction.
     *
     * @tparam T The type of the vector components.
     * @return Unit vector (1, 0).
     */
    template <typename T>
    [[nodiscard]] constexpr auto unit_x() -> Vector2<T> {
        return Vector2<T>{1, 0};
    }

    /**
     * @brief Create a unit vector in the y-direction.
     *
     * @tparam T The type of the vector components.
     * @return Unit vector (0, 1).
     */
    template <typename T>
    [[nodiscard]] constexpr auto unit_y() -> Vector2<T> {
        return Vector2<T>{0, 1};
    }

}  // namespace recti