//! Point module for representing points in 2D space
//!
//! This module provides a `Point` type that represents a point in 2D space.

use std::fmt;
use std::ops::{Add, Sub};
use num_traits::{Num, Signed};
use approx::{AbsDiffEq, RelativeEq};

use crate::generic::{Overlaps, Contains, IntersectWith, MinDistWith, Measure, Center};
use crate::interval::Interval;
use crate::vector2::Vector2;

/// A point in 2D space
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    /// Create a new point with given x and y coordinates
    pub fn new(x: T, y: T) -> Self {
        Self { x, y }
    }

    /// Get the x-coordinate
    pub fn x(&self) -> &T {
        &self.x
    }

    /// Get the y-coordinate
    pub fn y(&self) -> &T {
        &self.y
    }

    /// Get the width of the point (always 1 for scalar coordinates)
    pub fn width(&self) -> T
    where
        T: Num + From<i32>,
    {
        T::one()
    }

    /// Get the height of the point (always 1 for scalar coordinates)
    pub fn height(&self) -> T
    where
        T: Num + From<i32>,
    {
        T::one()
    }

    /// Get the area of the point (always 1 for scalar coordinates)
    pub fn area(&self) -> T
    where
        T: Num + From<i32>,
    {
        T::one()
    }

    /// Create a hull (bounding box) that contains this point and another
    pub fn hull_with(&self, other: &Self) -> (Interval<T>, Interval<T>)
    where
        T: PartialOrd + Copy,
    {
        let x_interval = if self.x <= other.x {
            Interval::new(self.x, other.x)
        } else {
            Interval::new(other.x, self.x)
        };

        let y_interval = if self.y <= other.y {
            Interval::new(self.y, other.y)
        } else {
            Interval::new(other.y, self.y)
        };

        (x_interval, y_interval)
    }

    /// Enlarge the point by a given amount to create a rectangle
    pub fn enlarge(&self, amount: T) -> (Interval<T>, Interval<T>)
    where
        T: Add<Output = T> + Sub<Output = T> + Copy,
    {
        let x_interval = Interval::new(self.x - amount, self.x + amount);
        let y_interval = Interval::new(self.y - amount, self.y + amount);
        (x_interval, y_interval)
    }
}

impl<T: fmt::Display> fmt::Display for Point<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

// Implement generic traits for Point
impl<T> Overlaps for Point<T>
where
    T: PartialEq,
{
    fn overlaps(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y
    }
}

impl<T> Contains for Point<T>
where
    T: PartialEq,
{
    fn contains(&self, other: &Self) -> bool {
        self.overlaps(other)
    }
}

impl<T> Contains<T> for Point<T>
where
    T: PartialEq + Copy,
{
    fn contains(&self, other: &T) -> bool {
        self.x == *other && self.y == *other
    }
}

impl<T> IntersectWith for Point<T>
where
    T: PartialEq + Copy,
{
    type Output = Option<Self>;

    fn intersect_with(&self, other: &Self) -> Option<Self::Output> {
        if self.overlaps(other) {
            Some(Some(*self))
        } else {
            Some(None)
        }
    }
}

impl<T> MinDistWith for Point<T>
where
    T: Copy + Sub<Output = T> + Signed + PartialOrd,
{
    type Output = T;

    fn min_dist_with(&self, other: &Self) -> T {
        let dx = if self.x > other.x {
            self.x - other.x
        } else {
            other.x - self.x
        };

        let dy = if self.y > other.y {
            self.y - other.y
        } else {
            other.y - self.y
        };

        dx + dy  // Manhattan distance
    }
}

impl<T> Measure for Point<T>
where
    T: Num + From<i32>,
{
    type Output = T;

    fn measure(&self) -> T {
        self.area()
    }
}

impl<T> Center for Point<T>
where
    T: Copy,
{
    type Output = Self;

    fn center(&self) -> Self {
        *self
    }
}

// Arithmetic operations with Vector2
impl<T> Add<Vector2<T>> for Point<T>
where
    T: Add<Output = T> + Copy,
{
    type Output = Self;

    fn add(self, rhs: Vector2<T>) -> Self::Output {
        Self::new(self.x + *rhs.x(), self.y + *rhs.y())
    }
}

impl<T> Sub<Vector2<T>> for Point<T>
where
    T: Sub<Output = T> + Copy,
{
    type Output = Self;

    fn sub(self, rhs: Vector2<T>) -> Self::Output {
        Self::new(self.x - *rhs.x(), self.y - *rhs.y())
    }
}

impl<T> Sub for Point<T>
where
    T: Sub<Output = T> + Copy,
{
    type Output = Vector2<T>;

    fn sub(self, rhs: Self) -> Self::Output {
        Vector2::new(self.x - rhs.x, self.y - rhs.y)
    }
}

// Utility functions
/// Find the nearest point to a given point from a set of candidates
pub fn nearest_point_to<'a, T>(point: &Point<T>, candidates: &'a [Point<T>]) -> Option<&'a Point<T>>
where
    T: Copy + Sub<Output = T> + Signed + PartialOrd,
{
    candidates.iter().min_by(|a, b| {
        let dist_a = point.min_dist_with(a);
        let dist_b = point.min_dist_with(b);
        dist_a.partial_cmp(&dist_b).unwrap_or(std::cmp::Ordering::Equal)
    })
}

// Implement approximate equality for floating-point points
impl<T> AbsDiffEq for Point<T>
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

impl<T> RelativeEq for Point<T>
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
