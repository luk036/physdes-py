//! Generic operations for physical design calculations
//!
//! This module provides generic operations that work with different types of objects,
//! including simple numbers and more complex geometric objects.

use std::ops::Sub;

/// Trait for objects that can check for overlap
pub trait Overlaps<Rhs = Self> {
    /// Check if this object overlaps with another object
    fn overlaps(&self, other: &Rhs) -> bool;
}

/// Trait for objects that can check containment
pub trait Contains<Rhs = Self> {
    /// Check if this object contains another object
    fn contains(&self, other: &Rhs) -> bool;
}

/// Trait for objects that can compute intersection
pub trait IntersectWith<Rhs = Self> {
    /// Type of the intersection result
    type Output;
    
    /// Compute the intersection with another object
    fn intersect_with(&self, other: &Rhs) -> Option<Self::Output>;
}

/// Trait for objects that can compute minimum distance
pub trait MinDistWith<Rhs = Self> {
    /// Type of the distance result
    type Output;
    
    /// Compute the minimum Manhattan distance to another object
    fn min_dist_with(&self, other: &Rhs) -> Self::Output;
}

/// Check if two objects overlap
pub fn overlap<L, R>(lhs: &L, rhs: &R) -> bool
where
    L: Overlaps<R>,
{
    lhs.overlaps(rhs)
}

/// Check if one object contains another
pub fn contain<L, R>(lhs: &L, rhs: &R) -> bool
where
    L: Contains<R>,
{
    lhs.contains(rhs)
}

/// Compute the intersection of two objects
pub fn intersection<L, R>(lhs: &L, rhs: &R) -> Option<<L as IntersectWith<R>>::Output>
where
    L: IntersectWith<R>,
{
    lhs.intersect_with(rhs)
}

/// Compute the minimum distance between two objects
pub fn min_dist<L, R>(lhs: &L, rhs: &R) -> <L as MinDistWith<R>>::Output
where
    L: MinDistWith<R>,
{
    lhs.min_dist_with(rhs)
}

/// Compute the displacement between two objects
pub fn displacement<T>(lhs: T, rhs: T) -> T
where
    T: Sub<Output = T>,
{
    lhs - rhs
}

/// Find the lower of two values
pub fn lower<T>(lhs: T, rhs: T) -> T
where
    T: PartialOrd,
{
    if lhs <= rhs { lhs } else { rhs }
}

/// Find the upper of two values
pub fn upper<T>(lhs: T, rhs: T) -> T
where
    T: PartialOrd,
{
    if lhs >= rhs { lhs } else { rhs }
}

/// Compute the measure (size) of an object
pub fn measure_of<T>(obj: &T) -> T::Output
where
    T: Measure,
{
    obj.measure()
}

/// Compute the center of an object
pub fn center<T>(obj: &T) -> T::Output
where
    T: Center,
{
    obj.center()
}

/// Trait for objects that have a measurable size
pub trait Measure {
    /// Type of the measurement result
    type Output;
    
    /// Compute the measure (size) of the object
    fn measure(&self) -> Self::Output;
}

/// Trait for objects that have a center
pub trait Center {
    /// Type of the center result
    type Output;
    
    /// Compute the center of the object
    fn center(&self) -> Self::Output;
}

// Implement traits for primitive numeric types
impl Overlaps for i32 {
    fn overlaps(&self, other: &i32) -> bool {
        self == other
    }
}

impl Overlaps for f64 {
    fn overlaps(&self, other: &f64) -> bool {
        (self - other).abs() < f64::EPSILON
    }
}

impl Contains for i32 {
    fn contains(&self, other: &i32) -> bool {
        self == other
    }
}

impl Contains for f64 {
    fn contains(&self, other: &f64) -> bool {
        (self - other).abs() < f64::EPSILON
    }
}

impl MinDistWith for i32 {
    type Output = i32;
    
    fn min_dist_with(&self, other: &i32) -> i32 {
        (self - other).abs()
    }
}

impl MinDistWith for f64 {
    type Output = f64;
    
    fn min_dist_with(&self, other: &f64) -> f64 {
        (self - other).abs()
    }
}