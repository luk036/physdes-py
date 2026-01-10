//! Interval module for representing ranges of numbers
//!
//! This module provides an `Interval` type that represents a range of numbers
//! with a lower bound and an upper bound.

use std::fmt;
use std::ops::{Add, Sub, Mul};
use num_traits::{Num, Signed, Zero};
use approx::{AbsDiffEq, RelativeEq};

use crate::generic::{Overlaps, Contains, IntersectWith, MinDistWith, Measure, Center};

/// An interval representing a range [lb, ub] inclusive
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Interval<T> {
    lb: T,
    ub: T,
}

impl<T> Interval<T> {
    /// Create a new interval with given lower and upper bounds
    pub fn new(lb: T, ub: T) -> Self {
        Self { lb, ub }
    }

    /// Get the lower bound
    pub fn lb(&self) -> &T {
        &self.lb
    }

    /// Get the upper bound
    pub fn ub(&self) -> &T {
        &self.ub
    }

    /// Check if the interval is invalid (lower bound > upper bound)
    pub fn is_invalid(&self) -> bool
    where
        T: PartialOrd,
    {
        self.lb > self.ub
    }

    /// Check if the interval is valid (lower bound <= upper bound)
    pub fn is_valid(&self) -> bool
    where
        T: PartialOrd,
    {
        self.lb <= self.ub
    }

    /// Get the width of the interval
    pub fn width(&self) -> T
    where
        T: Copy + Sub<Output = T>,
    {
        self.ub - self.lb
    }

    /// Check if the interval is empty (zero width)
    pub fn is_empty(&self) -> bool
    where
        T: PartialEq + Zero,
    {
        self.lb == self.ub
    }
}

impl<T: fmt::Display> fmt::Display for Interval<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}, {}]", self.lb, self.ub)
    }
}

// Implement generic traits for Interval
impl<T> Overlaps for Interval<T>
where
    T: PartialOrd,
{
    fn overlaps(&self, other: &Self) -> bool {
        self.lb <= other.ub && other.lb <= self.ub
    }
}

impl<T> Overlaps<T> for Interval<T>
where
    T: PartialOrd + Copy,
{
    fn overlaps(&self, other: &T) -> bool {
        self.lb <= *other && *other <= self.ub
    }
}

impl<T> Contains for Interval<T>
where
    T: PartialOrd,
{
    fn contains(&self, other: &Self) -> bool {
        self.lb <= other.lb && other.ub <= self.ub
    }
}

impl<T> Contains<T> for Interval<T>
where
    T: PartialOrd + Copy,
{
    fn contains(&self, other: &T) -> bool {
        self.lb <= *other && *other <= self.ub
    }
}

impl<T> IntersectWith for Interval<T>
where
    T: PartialOrd + Copy,
{
    type Output = Self;

    fn intersect_with(&self, other: &Self) -> Option<Self> {
        if self.overlaps(other) {
            let lb = if self.lb > other.lb { self.lb } else { other.lb };
            let ub = if self.ub < other.ub { self.ub } else { other.ub };
            Some(Self::new(lb, ub))
        } else {
            None
        }
    }
}

impl<T> MinDistWith for Interval<T>
where
    T: Copy + PartialOrd + Sub<Output = T> + Signed,
{
    type Output = T;

    fn min_dist_with(&self, other: &Self) -> T {
        if self.overlaps(other) {
            T::zero()
        } else if self.ub < other.lb {
            other.lb - self.ub
        } else {
            self.lb - other.ub
        }
    }
}

impl<T> MinDistWith<T> for Interval<T>
where
    T: Copy + PartialOrd + Sub<Output = T> + Signed,
{
    type Output = T;

    fn min_dist_with(&self, other: &T) -> T {
        if self.contains(other) {
            T::zero()
        } else if *other < self.lb {
            self.lb - *other
        } else {
            *other - self.ub
        }
    }
}

impl<T> Measure for Interval<T>
where
    T: Copy + Sub<Output = T>,
{
    type Output = T;

    fn measure(&self) -> T {
        self.width()
    }
}

impl<T> Center for Interval<T>
where
    T: Copy + Add<Output = T> + Sub<Output = T> + Num + From<i32>,
{
    type Output = T;

    fn center(&self) -> T {
        (self.lb + self.ub) / T::from(2)
    }
}

// Arithmetic operations
impl<T> Add<T> for Interval<T>
where
    T: Add<Output = T> + Copy,
{
    type Output = Self;

    fn add(self, rhs: T) -> Self::Output {
        Self::new(self.lb + rhs, self.ub + rhs)
    }
}

impl<T> Sub<T> for Interval<T>
where
    T: Sub<Output = T> + Copy,
{
    type Output = Self;

    fn sub(self, rhs: T) -> Self::Output {
        Self::new(self.lb - rhs, self.ub - rhs)
    }
}

impl<T> Mul<T> for Interval<T>
where
    T: Mul<Output = T> + Copy,
{
    type Output = Self;

    fn mul(self, rhs: T) -> Self::Output {
        Self::new(self.lb * rhs, self.ub * rhs)
    }
}

// Utility functions
/// Create the hull (smallest containing interval) of two intervals or values
pub fn hull<T>(a: T, b: T) -> Interval<T>
where
    T: PartialOrd + Copy,
{
    let lb = if a <= b { a } else { b };
    let ub = if a >= b { a } else { b };
    Interval::new(lb, ub)
}

/// Enlarge an interval by a given amount on both sides
pub fn enlarge<T>(interval: Interval<T>, amount: T) -> Interval<T>
where
    T: Add<Output = T> + Sub<Output = T> + Copy,
{
    Interval::new(interval.lb - amount, interval.ub + amount)
}

// Implement approximate equality for floating-point intervals
impl<T> AbsDiffEq for Interval<T>
where
    T: AbsDiffEq<Epsilon = T> + Copy,
    T::Epsilon: Copy,
{
    type Epsilon = T::Epsilon;

    fn default_epsilon() -> Self::Epsilon {
        T::default_epsilon()
    }

    fn abs_diff_eq(&self, other: &Self, epsilon: Self::Epsilon) -> bool {
        self.lb.abs_diff_eq(&other.lb, epsilon) && self.ub.abs_diff_eq(&other.ub, epsilon)
    }
}

impl<T> RelativeEq for Interval<T>
where
    T: RelativeEq<Epsilon = T> + Copy,
    T::Epsilon: Copy,
{
    fn default_max_relative() -> Self::Epsilon {
        T::default_max_relative()
    }

    fn relative_eq(&self, other: &Self, epsilon: Self::Epsilon, max_relative: Self::Epsilon) -> bool {
        self.lb.relative_eq(&other.lb, epsilon, max_relative) &&
        self.ub.relative_eq(&other.ub, epsilon, max_relative)
    }
}
