//! Physical Design Algorithms for VLSI in Rust
//!
//! This is a Rust implementation of the physdes-py Python library,
//! providing geometric primitives and algorithms for VLSI physical design.

pub mod generic;
pub mod interval;
pub mod point;
pub mod vector2;
pub mod recti;
pub mod polygon;
pub mod rpolygon;
pub mod manhattan_arc;
pub mod cts;
pub mod router;
pub mod steiner_forest;

// Re-export commonly used types
pub use interval::Interval;
pub use point::Point;
pub use vector2::Vector2;
pub use recti::{Rectangle, VSegment, HSegment};

#[cfg(test)]
mod tests;
