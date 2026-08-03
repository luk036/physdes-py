"""
Demo: Visualize Rectangle Overlap Detection

This demo shows rectangles graphically and highlights any overlapping pairs
using the line sweep algorithm.
"""

from typing import Generator

from lds_gen.ilds import Halton

from physdes.point import Point
from physdes.recti import detect_overlap_gen


def visualize_overlap_svg(
    rectangles: list,
    overlapping_pair_gen: Generator[tuple, None, None],
    width: int = 800,
    height: int = 600,
    margin: int = 50,
) -> str:
    if not rectangles:
        return "<svg></svg>"

    min_x = min(r.xcoord.lb for r in rectangles)
    max_x = max(r.xcoord.ub for r in rectangles)
    min_y = min(r.ycoord.lb for r in rectangles)
    max_y = max(r.ycoord.ub for r in rectangles)

    content_w = max_x - min_x
    content_h = max_y - min_y
    if content_w == 0:
        content_w = 1
    if content_h == 0:
        content_h = 1

    scale_x = (width - 2 * margin) / content_w
    scale_y = (height - 2 * margin) / content_h
    scale = min(scale_x, scale_y)

    def to_svg_x(x: int) -> float:
        return margin + (x - min_x) * scale

    def to_svg_y(y: int) -> float:
        return height - margin - (y - min_y) * scale

    overlap_indices = set()
    for overlapping_pair in overlapping_pair_gen:
        r1, r2 = overlapping_pair
        for idx, r in enumerate(rectangles):
            if (r.xcoord == r1.xcoord and r.ycoord == r1.ycoord) or (
                r.xcoord == r2.xcoord and r.ycoord == r2.ycoord
            ):
                overlap_indices.add(idx)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="background-color:#f8f9fa;">',
    ]

    for idx, r in enumerate(rectangles):
        x1 = to_svg_x(r.xcoord.lb)
        y1 = to_svg_y(r.ycoord.ub)
        w = (r.xcoord.ub - r.xcoord.lb) * scale
        h = (r.ycoord.ub - r.ycoord.lb) * scale

        if idx in overlap_indices:
            fill = "#e74c3c"
            stroke = "#c0392b"
            opacity = "0.7"
        else:
            fill = "#4a90d9"
            stroke = "#357abd"
            opacity = "0.5"

        svg_parts.append(
            f'<rect x="{x1}" y="{y1}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2" opacity="{opacity}"/>'
        )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def demo() -> None:
    print("=== Rectangle Overlap Detection Demo ===\n")
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(600)
    coords = [hgen.pop() for _ in range(500)]
    svg_rects = [Point(coord[0], coord[1]).enlarge_with(10) for coord in coords]

    print()
    print("=" * 50)
    print("Overlap Detection Result")
    print("=" * 50)
    overlap_result_gen = detect_overlap_gen(svg_rects)

    svg = visualize_overlap_svg(svg_rects, overlap_result_gen)

    with open("demo_overlap.svg", "w") as f:
        f.write(svg)
    print("\nGenerated demo_overlap.svg")
    print("Open the SVG file in a browser to see the visualization.")


if __name__ == "__main__":
    demo()
