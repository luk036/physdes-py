#pragma once

/**
 * @mainpage Physical Design Algorithms for VLSI in C++23
 *
 * This is a C++23 implementation of the physdes-py Python library,
 * providing geometric primitives and algorithms for VLSI physical design.
 *
 * The library includes:
 * - Generic geometric operations (overlap, contain, intersection, min_dist)
 * - Interval arithmetic
 * - 2D points and vectors
 * - Axis-aligned rectangles and line segments
 * - Polygons and rectilinear polygons
 * - Manhattan arcs
 * - Clock tree synthesis algorithms
 * - Routing algorithms
 * - Steiner forest algorithms
 */

#include "recti/generic.hpp"
#include "recti/interval.hpp"
#include "recti/point.hpp"
#include "recti/vector2.hpp"
#include "recti/recti.hpp"
#include "recti/polygon.hpp"
#include "recti/rpolygon.hpp"
#include "recti/manhattan_arc.hpp"
#include "recti/cts.hpp"
#include "recti/router.hpp"
#include "recti/steiner_forest.hpp"
