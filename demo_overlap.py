"""
Demo: Visualize Rectangle Overlap Detection

This demo shows rectangles graphically and highlights any overlapping pairs
using the line sweep algorithm.
"""

from typing import Generator

from lds_gen.ilds import Halton

# from physdes.interval import Interval
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

    # legend_y = 30
    # svg_parts.append(f'<text x="{margin}" y="{legend_y}" font-size="14" fill="#333">Rectangles</text>')
    # legend_y += 20
    # svg_parts.append(f'<rect x="{margin}" y="{legend_y - 12}" width="16" height="12" fill="#4a90d9" stroke="#333"/>')
    # svg_parts.append(f'<text x="{margin + 20}" y="{legend_y}" font-size="12" fill="#333">Non-overlapping</text>')
    # legend_y += 20
    # svg_parts.append(f'<rect x="{margin}" y="{legend_y - 12}" width="16" height="12" fill="#e74c3c" stroke="#c0392b"/>')
    # svg_parts.append(f'<text x="{margin + 20}" y="{legend_y}" font-size="12" fill="#333">Overlapping</text>')
    # if overlapping_pair:
    #     legend_y += 20
    #     svg_parts.append(f'<text x="{margin + 20}" y="{legend_y}" font-size="12" fill="#e74c3c">Overlap detected!</text>')
    #     legend_y += 20
    #     pair1_str = f"({overlapping_pair[0].xcoord}, {overlapping_pair[0].ycoord})"
    #     svg_parts.append(f'<text x="{margin + 20}" y="{legend_y}" font-size="11" fill="#666">{pair1_str}</text>')
    #     legend_y += 15
    #     pair2_str = f"({overlapping_pair[1].xcoord}, {overlapping_pair[1].ycoord})"
    #     svg_parts.append(f'<text x="{margin + 20}" y="{legend_y}" font-size="11" fill="#666">{pair2_str}</text>')

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

        # cx = x1 + w / 2
        # cy = y1 + h / 2
        # svg_parts.append(f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="11" fill="white" font-weight="bold">{idx + 1}</text>')

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def demo() -> None:
    print("=== Rectangle Overlap Detection Demo ===\n")
    hgen = Halton([3, 2], [7, 11])
    hgen.reseed(600)
    coords = [hgen.pop() for _ in range(500)]
    svg_rects = [Point(coord[0], coord[1]).enlarge_with(10) for coord in coords]

    # svg_rects = [
    #     Rectangle(Interval(0, 4), Interval(0, 4)),
    #     Rectangle(Interval(2, 6), Interval(2, 6)),
    #     Rectangle(Interval(5, 9), Interval(5, 9)),
    #     Rectangle(Interval(8, 12), Interval(8, 12)),
    #     Rectangle(Interval(11, 15), Interval(11, 15)),
    #     Rectangle(Interval(3, 7), Interval(10, 14)),
    #     Rectangle(Interval(14, 18), Interval(14, 18)),
    #     Rectangle(Interval(16, 20), Interval(4, 8)),
    #     Rectangle(Interval(6, 10), Interval(6, 10)),
    #     Rectangle(Interval(9, 13), Interval(12, 16)),
    #     Rectangle(Interval(0, 3), Interval(8, 11)),
    # ]

    # print(f"Testing with {len(svg_rects)} rectangles:")
    # for i, r in enumerate(svg_rects):
    #     print(f"  {i + 1}: ({r.xcoord}, {r.ycoord})")

    print()
    print("=" * 50)
    print("Overlap Detection Result")
    print("=" * 50)
    overlap_result_gen = detect_overlap_gen(svg_rects)

    # for overlap_result in overlap_result_gen:
    #     r1, r2 = overlap_result
    #     print("OVERLAP DETECTED between:")
    #     print(f"  Rect A: ({r1.xcoord}, {r1.ycoord})")
    #     print(f"  Rect B: ({r2.xcoord}, {r2.ycoord})")
    # else:
    #     print("No overlap found")

    svg = visualize_overlap_svg(svg_rects, overlap_result_gen)

    with open("demo_overlap.svg", "w") as f:
        f.write(svg)
    print("\nGenerated demo_overlap.svg")
    print("Open the SVG file in a browser to see the visualization.")


if __name__ == "__main__":
    demo()
