//! Vector2 module for representing 2D vectors
//!
//! This module provides a `Vector2` type that represents a 2D vector.

use std::fmt;
use std::ops::{Add, Sub, Mul, Div, Neg};
use num_traits::{Signed, Zero, One};
use approx::{AbsDiffEq, RelativeEq};

/// A 2D vector
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Vector2<T> {
    x: T,
    y: T,
}

impl<T> Vector2<T> {
    /// Create a new vector with given x and y components
    pub fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
    
    /// Get the x-component
    pub fn x(&self) -> &T {
        &self.x
    }
    
    /// Get the y-component
    pub fn y(&self) -> &T {
        &self.y
    }
    
    /// Compute the cross product with another vector
    pub fn cross(&self, other: &Self) -> T
    where
        T: Copy + Mul<Output = T> + Sub<Output = T>,
    {
        self.x * other.y - self.y * other.x
    }
    
    /// Compute the dot product with another vector
    pub fn dot(&self, other: &Self) -> T
    where
        T: Copy + Mul<Output = T> + Add<Output = T>,
    {
        self.x * other.x + self.y * other.y
    }
    
    /// Compute the Manhattan length (L1 norm) of the vector
    pub fn manhattan_length(&self) -> T
    where
        T: Copy + Signed,
    {
        self.x.abs() + self.y.abs()
    }
    
    /// Compute the squared Euclidean length of the vector
    pub fn length_squared(&self) -> T
    where
        T: Copy + Mul<Output = T> + Add<Output = T>,
    {
        self.x * self.x + self.y * self.y
    }
}

impl<T: fmt::Display> fmt::Display for Vector2<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "<{}, {}>", self.x, self.y)
    }
}

// Arithmetic operations
impl<T> Add for Vector2<T>
where
    T: Add<Output = T> + Copy,
{
    type Output = Self;
    
    fn add(self, rhs: Self) -> Self::Output {
        Self::new(self.x + rhs.x, self.y + rhs.y)
    }
}

impl<T> Sub for Vector2<T>
where
    T: Sub<Output = T> + Copy,
{
    type Output = Self;
    
    fn sub(self, rhs: Self) -> Self::Output {
        Self::new(self.x - rhs.x, self.y - rhs.y)
    }
}

impl<T> Mul<T> for Vector2<T>
where
    T: Mul<Output = T> + Copy,
{
    type Output = Self;
    
    fn mul(self, rhs: T) -> Self::Output {
        Self::new(self.x * rhs, self.y * rhs)
    }
}

impl<T> Div<T> for Vector2<T>
where
    T: Div<Output = T> + Copy,
{
    type Output = Self;
    
    fn div(self, rhs: T) -> Self::Output {
        Self::new(self.x / rhs, self.y / rhs)
    }
}

impl<T> Neg for Vector2<T>
where
    T: Neg<Output = T> + Copy,
{
    type Output = Self;
    
    fn neg(self) -> Self::Output {
        Self::new(-self.x, -self.y)
    }
}



// Equality operations
impl<T> PartialEq<T> for Vector2<T>
where
    T: PartialEq + Copy,
{
    fn eq(&self, other: &T) -> bool {
        self.x == *other && self.y == *other
    }
}

// Implement approximate equality for floating-point vectors
impl<T> AbsDiffEq for Vector2<T>
where
    T: AbsDiffEq<Epsilon = T> + Copy,
    T::Epsilon: Copy,
{
    type Epsilon = T::Epsilon;
    
    fn default_epsilon() -> Self::Epsilon {
        T::default_epsilon()
    }
    
    fn abs_diff_eq(&self, other: &Self, epsilon: Self::Epsilon) -> bool {
        self.x.abs_diff_eq(&other.x, epsilon) && self.y.abs_diff_eq(&other.y, epsilon)
    }
}

impl<T> RelativeEq for Vector2<T>
where
    T: RelativeEq<Epsilon = T> + Copy,
    T::Epsilon: Copy,
{
    fn default_max_relative() -> Self::Epsilon {
        T::default_max_relative()
    }
    
    fn relative_eq(&self, other: &Self, epsilon: Self::Epsilon, max_relative: Self::Epsilon) -> bool {
        self.x.relative_eq(&other.x, epsilon, max_relative) &&
        self.y.relative_eq(&other.y, epsilon, max_relative)
    }
}

// Utility functions
/// Create a zero vector
pub fn zero_vector<T>() -> Vector2<T>
where
    T: Zero,
{
    Vector2::new(T::zero(), T::zero())
}

/// Create a unit vector in the x-direction
pub fn unit_x<T>() -> Vector2<T>
where
    T: Zero + One,
{
    Vector2::new(T::one(), T::zero())
}

/// Create a unit vector in the y-direction
pub fn unit_y<T>() -> Vector2<T>
where
    T: Zero + One,
{
    Vector2::new(T::zero(), T::one())
}