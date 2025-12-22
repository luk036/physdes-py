//! Rectangle and segment modules for geometric shapes
//!
//! This module provides types for rectangles and line segments in 2D space.

use std::fmt;
use num_traits::Num;
use approx::{AbsDiffEq, RelativeEq};

use crate::interval::Interval;
use crate::point::Point;
use crate::generic::{Overlaps, Contains, MinDistWith, Measure, Center};

/// An axis-aligned rectangle
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Rectangle<T> {
    x_interval: Interval<T>,
    y_interval: Interval<T>,
}

impl<T> Rectangle<T> {
    /// Create a new rectangle with given x and y intervals
    pub fn new(x_interval: Interval<T>, y_interval: Interval<T>) -> Self {
        Self { x_interval, y_interval }
    }
    
    /// Get the x-interval
    pub fn x_interval(&self) -> &Interval<T> {
        &self.x_interval
    }
    
    /// Get the y-interval
    pub fn y_interval(&self) -> &Interval<T> {
        &self.y_interval
    }
    
    /// Get the lower-left point of the rectangle
    pub fn ll(&self) -> Point<T>
    where
        T: Copy,
    {
        Point::new(*self.x_interval.lb(), *self.y_interval.lb())
    }
    
    /// Get the upper-right point of the rectangle
    pub fn ur(&self) -> Point<T>
    where
        T: Copy,
    {
        Point::new(*self.x_interval.ub(), *self.y_interval.ub())
    }
    
    /// Get the width of the rectangle
    pub fn width(&self) -> T
    where
        T: Copy + Sub<Output = T>,
    {
        self.x_interval.width()
    }
    
    /// Get the height of the rectangle
    pub fn height(&self) -> T
    where
        T: Copy + Sub<Output = T>,
    {
        self.y_interval.width()
    }
    
    /// Get the area of the rectangle
    pub fn area(&self) -> T
    where
        T: Copy + Sub<Output = T> + Mul<Output = T>,
    {
        self.width() * self.height()
    }
    
    /// Flip the rectangle (swap x and y coordinates)
    pub fn flip(&self) -> Self
    where
        T: Copy,
    {
        Self::new(self.y_interval, self.x_interval)
    }
}

impl<T: fmt::Display> fmt::Display for Rectangle<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {})", self.x_interval, self.y_interval)
    }
}

// Implement generic traits for Rectangle
impl<T> Overlaps for Rectangle<T>
where
    T: PartialOrd + Copy,
{
    fn overlaps(&self, other: &Self) -> bool {
        self.x_interval.overlaps(&other.x_interval) && 
        self.y_interval.overlaps(&other.y_interval)
    }
}

impl<T> Contains for Rectangle<T>
where
    T: PartialOrd + Copy,
{
    fn contains(&self, other: &Self) -> bool {
        self.x_interval.contains(&other.x_interval) && 
        self.y_interval.contains(&other.y_interval)
    }
}

impl<T> Contains<Point<T>> for Rectangle<T>
where
    T: PartialOrd + Copy,
{
    fn contains(&self, other: &Point<T>) -> bool {
        self.x_interval.contains(other.x()) && 
        self.y_interval.contains(other.y())
    }
}

impl<T> MinDistWith for Rectangle<T>
where
    T: Copy + PartialOrd + Sub<Output = T> + Signed,
{
    type Output = T;
    
    fn min_dist_with(&self, other: &Self) -> T {
        let dx = self.x_interval.min_dist_with(&other.x_interval);
        let dy = self.y_interval.min_dist_with(&other.y_interval);
        dx + dy  // Manhattan distance
    }
}

impl<T> MinDistWith<Point<T>> for Rectangle<T>
where
    T: Copy + PartialOrd + Sub<Output = T> + Signed,
{
    type Output = T;
    
    fn min_dist_with(&self, other: &Point<T>) -> T {
        let dx = self.x_interval.min_dist_with(other.x());
        let dy = self.y_interval.min_dist_with(other.y());
        dx + dy  // Manhattan distance
    }
}

impl<T> Measure for Rectangle<T>
where
    T: Copy + Sub<Output = T> + Mul<Output = T>,
{
    type Output = T;
    
    fn measure(&self) -> T {
        self.area()
    }
}

impl<T> Center for Rectangle<T>
where
    T: Copy + Add<Output = T> + Sub<Output = T> + Num + From<i32>,
{
    type Output = Point<T>;
    
    fn center(&self) -> Point<T> {
        Point::new(self.x_interval.center(), self.y_interval.center())
    }
}

/// A vertical line segment
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct VSegment<T> {
    x: T,
    y_interval: Interval<T>,
}

impl<T> VSegment<T> {
    /// Create a new vertical segment
    pub fn new(x: T, y_interval: Interval<T>) -> Self {
        Self { x, y_interval }
    }
    
    /// Get the x-coordinate
    pub fn x(&self) -> &T {
        &self.x
    }
    
    /// Get the y-interval
    pub fn y_interval(&self) -> &Interval<T> {
        &self.y_interval
    }
    
    /// Flip the segment (vertical to horizontal)
    pub fn flip(&self) -> HSegment<T>
    where
        T: Copy,
    {
        HSegment::new(self.y_interval, self.x)
    }
}

impl<T: fmt::Display> fmt::Display for VSegment<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "VSegment(x={}, y={})", self.x, self.y_interval)
    }
}

/// A horizontal line segment
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct HSegment<T> {
    x_interval: Interval<T>,
    y: T,
}

impl<T> HSegment<T> {
    /// Create a new horizontal segment
    pub fn new(x_interval: Interval<T>, y: T) -> Self {
        Self { x_interval, y }
    }
    
    /// Get the x-interval
    pub fn x_interval(&self) -> &Interval<T> {
        &self.x_interval
    }
    
    /// Get the y-coordinate
    pub fn y(&self) -> &T {
        &self.y
    }
    
    /// Flip the segment (horizontal to vertical)
    pub fn flip(&self) -> VSegment<T>
    where
        T: Copy,
    {
        VSegment::new(self.y, self.x_interval)
    }
}

impl<T: fmt::Display> fmt::Display for HSegment<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "HSegment(x={}, y={})", self.x_interval, self.y)
    }
}

// Implement generic traits for segments
impl<T> Overlaps for VSegment<T>
where
    T: PartialOrd + Copy,
{
    fn overlaps(&self, other: &Self) -> bool {
        self.x == other.x && self.y_interval.overlaps(&other.y_interval)
    }
}

impl<T> Contains for VSegment<T>
where
    T: PartialOrd + Copy,
{
    fn contains(&self, other: &Self) -> bool {
        self.x == other.x && self.y_interval.contains(&other.y_interval)
    }
}

impl<T> Contains<Point<T>> for VSegment<T>
where
    T: PartialOrd + Copy,
{
    fn contains(&self, other: &Point<T>) -> bool {
        self.x == *other.x() && self.y_interval.contains(other.y())
    }
}

impl<T> Overlaps for HSegment<T>
where
    T: PartialOrd + Copy,
{
    fn overlaps(&self, other: &Self) -> bool {
        self.y == other.y && self.x_interval.overlaps(&other.x_interval)
    }
}

impl<T> Contains for HSegment<T>
where
    T: PartialOrd + Copy,
{
    fn contains(&self, other: &Self) -> bool {
        self.y == other.y && self.x_interval.contains(&other.x_interval)
    }
}

impl<T> Contains<Point<T>> for HSegment<T>
where
    T: PartialOrd + Copy,
{
    fn contains(&self, other: &Point<T>) -> bool {
        self.y == *other.y() && self.x_interval.contains(other.x())
    }
}

// Implement approximate equality
impl<T> AbsDiffEq for Rectangle<T>
where
    T: AbsDiffEq<Epsilon = T> + Copy,
    T::Epsilon: Copy,
{
    type Epsilon = T::Epsilon;
    
    fn default_epsilon() -> Self::Epsilon {
        T::default_epsilon()
    }
    
    fn abs_diff_eq(&self, other: &Self, epsilon: Self::Epsilon) -> bool {
        self.x_interval.abs_diff_eq(&other.x_interval, epsilon) &&
        self.y_interval.abs_diff_eq(&other.y_interval, epsilon)
    }
}

impl<T> RelativeEq for Rectangle<T>
where
    T: RelativeEq<Epsilon = T> + Copy,
    T::Epsilon: Copy,
{
    fn default_max_relative() -> Self::Epsilon {
        T::default_max_relative()
    }
    
    fn relative_eq(&self, other: &Self, epsilon: Self::Epsilon, max_relative: Self::Epsilon) -> bool {
        self.x_interval.relative_eq(&other.x_interval, epsilon, max_relative) &&
        self.y_interval.relative_eq(&other.y_interval, epsilon, max_relative)
    }
}

// Need to import std::ops for the generic constraints
use std::ops::{Add, Sub, Mul};
use num_traits::Signed;