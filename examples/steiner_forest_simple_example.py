from typing import List, Tuple

from physdes.steiner_forest.steiner_forest_grid import steiner_forest_grid

if __name__ == "__main__":
    # Simple example for presentation
    h: int = 4
    w: int = 4
    pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = [
        ((0, 0), (3, 3)),  # Diagonal
        ((0, 3), (3, 0)),  # Anti-diagonal
    ]

    F_pruned, total_cost, sources, terminals, steiner_nodes = steiner_forest_grid(h, w, pairs)

    cell_size = 80
    margin = 40
    width = w * cell_size + 2 * margin
    height = h * cell_size + 2 * margin

    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .source {{ fill: #2563eb; stroke: #1e40af; stroke-width: 2; }}
    .terminal {{ fill: #dc2626; stroke: #991b1b; stroke-width: 2; }}
    .steiner {{ fill: #16a34a; stroke: #166534; stroke-width: 2; }}
    .grid {{ stroke: #e5e7eb; stroke-width: 1; }}
    .edge {{ stroke: #2563eb; stroke-width: 4; stroke-linecap: round; }}
    .label {{ font-family: monospace; font-size: 14px; fill: #374151; text-anchor: middle; }}
  </style>
  <!-- Grid background -->
  <rect x="{margin}" y="{margin}" width="{width - 2 * margin}" height="{height - 2 * margin}" fill="#f9fafb"/>
'''

    # Grid lines
    for i in range(h + 1):
        y = margin + i * cell_size
        svg += f'<line x1="{margin}" y1="{y}" x2="{width - margin}" y2="{y}" class="grid"/>'
    for j in range(w + 1):
        x = margin + j * cell_size
        svg += f'<line x1="{x}" y1="{margin}" x2="{x}" y2="{height - margin}" class="grid"/>'

    # Nodes
    for i in range(h):
        for j in range(w):
            cx = margin + j * cell_size + cell_size / 2
            cy = margin + i * cell_size + cell_size / 2
            node = i * w + j
            if node in sources:
                cls = "source"
            elif node in terminals:
                cls = "terminal"
            elif node in steiner_nodes:
                cls = "steiner"
            else:
                continue
            svg += f'<circle cx="{cx}" cy="{cy}" r="12" class="{cls}"/>'
            svg += f'<text x="{cx}" y="{cy + 5}" class="label">{node}</text>'

    # Edges (draw first for layering)
    for u, v, _c in F_pruned:
        ui, uj = divmod(u, w)
        vi, vj = divmod(v, w)
        ux = margin + uj * cell_size + cell_size / 2
        uy = margin + ui * cell_size + cell_size / 2
        vx = margin + vj * cell_size + cell_size / 2
        vy = margin + vi * cell_size + cell_size / 2
        svg += f'<line x1="{ux}" y1="{uy}" x2="{vx}" y2="{vy}" class="edge"/>'

    svg += "</svg>"

    with open("steiner_forest_simple.svg", "w") as f:
        f.write(svg)

    print("SVG generated: steiner_forest_simple.svg")
    print(f"Total cost: {total_cost}")
    print(f"Sources: {sources}")
    print(f"Terminals: {terminals}")
    print(f"Steiner nodes: {steiner_nodes}")
    print(f"Edges: {F_pruned}")
