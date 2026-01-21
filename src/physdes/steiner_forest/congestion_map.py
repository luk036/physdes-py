def draw_congestion_map(grid: list[list[int]], filename: str = "congestion_map.svg") -> None:
    if not grid or not grid[0]:
        raise ValueError("Grid must not be empty")

    rows = len(grid)
    cols = len(grid[0])
    cell_size = 50
    padding = 20
    legend_width = 100
    title_height = 60

    width = cols * cell_size + 2 * padding + legend_width
    height = rows * cell_size + 2 * padding + title_height

    def interpolate_color(value: int) -> str:
        """Interpolate from green (0) -> yellow (50) -> red (100)"""
        if value <= 50:
            # Green to Yellow
            red_val = int(255 * (value / 50))
            green_val = 255
            blue_val = 0
        else:
            # Yellow to Red
            red_val = 255
            green_val = int(255 * ((50 - (value - 50)) / 50))
            blue_val = 0
        return f"#{red_val:02x}{green_val:02x}{blue_val:02x}"

    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append("<defs>")
    svg.append('<linearGradient id="grad" x1="0%" y1="0%" x2="0%" y2="100%">')
    svg.append('<stop offset="0%" style="stop-color:#00ff00"/>')
    svg.append('<stop offset="50%" style="stop-color:#ffff00"/>')
    svg.append('<stop offset="100%" style="stop-color:#ff0000"/>')
    svg.append("</linearGradient>")
    svg.append("</defs>")

    # Background
    svg.append(f'<rect width="{width}" height="{height}" fill="#ffffff"/>')

    # Title
    svg.append(f'<text x="{width // 2}" y="{padding + 20}" font-size="24" text-anchor="middle" font-family="Arial">Network Congestion Map</text>')

    # Draw grid cells
    for row_idx in range(rows):
        for col_idx in range(cols):
            value = grid[row_idx][col_idx]
            if not (0 <= value <= 100):
                raise ValueError(f"Congestion value {value} out of range [0,100]")

            x_pos = padding + col_idx * cell_size
            y_pos = title_height + padding + row_idx * cell_size
            color = interpolate_color(value)

            svg.append(f'<rect x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" fill="{color}" stroke="#cccccc" stroke-width="1"/>')
            # Optional: show value in center
            svg.append(f'<text x="{x_pos + cell_size // 2}" y="{y_pos + cell_size // 2 + 5}" font-size="14" text-anchor="middle" fill="black" font-family="Arial">{value}</text>')

    # Legend
    legend_x = padding + cols * cell_size + 30
    legend_y = title_height + padding + 50

    svg.append(f'<text x="{legend_x}" y="{legend_y - 20}" font-size="16" font-family="Arial">Congestion %</text>')
    svg.append(f'<rect x="{legend_x}" y="{legend_y}" width="30" height="{rows * cell_size}" fill="url(#grad)"/>')

    # Legend labels
    for label_val in range(0, 101, 25):
        y_pos = legend_y + (100 - label_val) / 100 * (rows * cell_size)
        svg.append(f'<text x="{legend_x + 40}" y="{y_pos + 5}" font-size="12" font-family="Arial">{label_val}</text>')
        svg.append(f'<line x1="{legend_x - 5}" y1="{y_pos}" x2="{legend_x}" y2="{y_pos}" stroke="black" stroke-width="1"/>')

    svg.append("</svg>")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Congestion map saved to {filename}")


grid = [
    [0, 20, 40, 80, 100],
    [10, 30, 60, 90, 70],
    [25, 50, 75, 95, 50],
    [0, 15, 35, 55, 30],
]

draw_congestion_map(grid, "my_congestion.svg")
