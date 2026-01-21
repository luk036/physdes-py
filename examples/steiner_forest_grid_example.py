from typing import List, Tuple

from physdes.steiner_forest.steiner_forest_grid import steiner_forest_grid

if __name__ == "__main__":
    # Example parameters (modify as needed)
    h: int = 8  # Height
    w: int = 8  # Width
    pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = [
        ((0, 0), (3, 2)),
        ((0, 0), (0, 5)),
        ((5, 5), (7, 6)),
        ((5, 5), (6, 7)),
    ]  # Terminal pairs

    F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(h, w, pairs)

    # Generate SVG and write to file
    cell_size = 50
    margin = 20
    width = w * cell_size + 2 * margin
    height = h * cell_size + 2 * margin
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'

    # Grid lines horizontal
    for i in range(h + 1):
        y = margin + i * cell_size
        svg += f'<line x1="{margin}" y1="{y}" x2="{width - margin}" y2="{y}" stroke="gray" stroke-width="1"/>'

    # Vertical
    for j in range(w + 1):
        x = margin + j * cell_size
        svg += f'<line x1="{x}" y1="{margin}" x2="{x}" y2="{height - margin}" stroke="gray" stroke-width="1"/>'

    # Nodes
    all_term = sources | terminals
    for i in range(h):
        for j in range(w):
            cx = margin + j * cell_size + cell_size / 2
            cy = margin + i * cell_size + cell_size / 2
            node = i * w + j
            if node in sources:
                r = 10
                fill = "blue"
            elif node in terminals:
                r = 10
                fill = "red"
            elif node in steiner_nodes:
                r = 7
                fill = "green"
            else:
                r = 5
                fill = "black"
            svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            svg += f'<text x="{cx}" y="{cy + 4}" font-size="10" text-anchor="middle">{node}</text>'

    # Selected edges
    for u, v, _c in F_pruned:
        ui, uj = divmod(u, w)
        vi, vj = divmod(v, w)
        ux = margin + uj * cell_size + cell_size / 2
        uy = margin + ui * cell_size + cell_size / 2
        vx = margin + vj * cell_size + cell_size / 2
        vy = margin + vi * cell_size + cell_size / 2
        svg += f'<line x1="{ux}" y1="{uy}" x2="{vx}" y2="{vy}" stroke="blue" stroke-width="5"/>'

    svg += "</svg>"

    # Write to SVG file
    with open("steiner_forest_diagonal.svg", "w") as f:
        f.write(svg)

    print("SVG file 'steiner_forest.svg' generated successfully.")
    print(f"Total cost: {total_cost}")
    print(f"Edges: {F_pruned}")
