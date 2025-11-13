import doctest
from typing import TYPE_CHECKING, List, Optional

from physdes.interval import Interval
from physdes.point import Point
from physdes.router.routing_tree import NodeType

if TYPE_CHECKING:
    from physdes.router.routing_tree import GlobalRoutingTree, RoutingNode


def visualize_routing_tree_svg(
    tree: "GlobalRoutingTree",
    keepouts: Optional[List[Point[Interval[int], Interval[int]]]] = None,
    width: int = 800,
    height: int = 600,
    margin: int = 50,
) -> str:
    """
    Visualize a GlobalRoutingTree in SVG format.

    Args:
        tree: GlobalRoutingTree instance to visualize
        width: SVG canvas width
        height: SVG canvas height
        margin: Margin around the drawing area

    Returns:
        SVG string representation

    Examples:
        >>> from physdes.point import Point
        >>> from physdes.router.routing_tree import GlobalRoutingTree
        >>> tree = GlobalRoutingTree(Point(0, 0))
        >>> s1 = tree.insert_steiner_node(Point(1, 1))
        >>> t1 = tree.insert_terminal_node(Point(2, 2), s1)
        >>> svg = visualize_routing_tree_svg(tree, width=200, height=200)
        >>> '<circle cx="50.0" cy="50.0"' in svg
        True
        >>> '<circle cx="100.0" cy="100.0"' in svg
        True
        >>> '<circle cx="150.0" cy="150.0"' in svg
        True
    """
    # Calculate bounds to scale the coordinates
    all_nodes = list(tree.nodes.values())
    if not all_nodes:
        return "<svg></svg>"

    # Get all coordinates to determine bounds
    all_x = [node.pt.xcoord for node in all_nodes]
    all_y = [node.pt.ycoord for node in all_nodes]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Add some padding to bounds
    range_x = max_x - min_x
    range_y = max_y - min_y
    if range_x == 0:
        range_x = 1
    if range_y == 0:
        range_y = 1

    # Scale factors
    scale_x = (width - 2 * margin) / range_x
    scale_y = (height - 2 * margin) / range_y
    scale = min(scale_x, scale_y)

    def scale_coords(x, y):
        """Scale coordinates to fit SVG canvas"""
        scaled_x = margin + (x - min_x) * scale
        scaled_y = margin + (y - min_y) * scale
        return scaled_x, scaled_y

    svg_parts = []

    # SVG header
    svg_parts.append(
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    )
    svg_parts.append('<rect width="100%" height="100%" fill="white"/>')

    # Draw connections first (so nodes appear on top)
    def draw_connections(node: "RoutingNode"):
        for child in node.children:
            # Get scaled coordinates
            x1, y1 = scale_coords(node.pt.xcoord, node.pt.ycoord)
            x2, y2 = scale_coords(child.pt.xcoord, child.pt.ycoord)

            # Draw line
            svg_parts.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>'
            )

        for child in node.children:
            draw_connections(child)

    # Add arrowhead marker definition
    svg_parts.append("<defs>")
    svg_parts.append(
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" '
        'refX="9" refY="3.5" orient="auto">'
    )
    svg_parts.append('<polygon points="0 0, 10 3.5, 0 7" fill="black"/>')
    svg_parts.append("</marker>")
    svg_parts.append("</defs>")

    # Draw all connections starting from source
    draw_connections(tree.source)

    # Draw nodes
    for node in all_nodes:
        x, y = scale_coords(node.pt.xcoord, node.pt.ycoord)

        # Different colors and sizes for different node types
        if node.type == NodeType.SOURCE:
            color = "red"
            radius = 8
            label = "S"
        elif node.type == NodeType.STEINER:
            color = "blue"
            radius = 6
            label = f"S{node.id.split('_')[1]}"
        elif node.type == NodeType.TERMINAL:
            color = "green"
            radius = 6
            label = f"T{node.id.split('_')[1]}"
        else:
            color = "gray"
            radius = 5
            label = node.id

        # Draw node circle
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" stroke="black" stroke-width="1"/>'
        )

        # Draw node label
        svg_parts.append(
            f'<text x="{x + radius + 2}" y="{y + 4}" font-family="Arial" font-size="10" fill="black">{label}</text>'
        )

        # Draw coordinates
        svg_parts.append(
            f'<text x="{x}" y="{y - radius - 5}" font-family="Arial" font-size="8" '
            f'fill="gray" text-anchor="middle">({node.pt.xcoord},{node.pt.ycoord})</text>'
        )

    # Draw keepouts
    if keepouts is not None:
        for keepout in keepouts:
            x1, y1 = scale_coords(keepout.xcoord.lb, keepout.ycoord.lb)
            x2, y2 = scale_coords(keepout.xcoord.ub, keepout.ycoord.ub)
            rwidth = x2 - x1
            rheight = y2 - y1
            color = "orange"
            svg_parts.append(
                f'<rect x="{x1}" y="{y1}" width="{rwidth}" height = "{rheight}" fill="{color}" stroke="black" stroke-width="1"/>'
            )

    # Add legend
    legend_y = 20
    svg_parts.append(
        f'<text x="20" y="{legend_y}" font-family="Arial" font-size="12" font-weight="bold">Legend:</text>'
    )

    legend_items = [
        ("Source", "red", 20, legend_y + 20),
        ("Steiner", "blue", 20, legend_y + 40),
        ("Terminal", "green", 20, legend_y + 60),
    ]

    for text, color, x_pos, y_pos in legend_items:
        svg_parts.append(
            f'<circle cx="{x_pos}" cy="{y_pos - 4}" r="4" fill="{color}" stroke="black"/>'
        )
        svg_parts.append(
            f'<text x="{x_pos + 10}" y="{y_pos}" font-family="Arial" font-size="10">{text}</text>'
        )

    # Display statistics
    stats_y = legend_y + 90
    svg_parts.append(
        f'<text x="20" y="{stats_y}" font-family="Arial" font-size="10" font-weight="bold">Statistics:</text>'
    )
    svg_parts.append(
        f'<text x="20" y="{stats_y + 15}" font-family="Arial" font-size="9">Total Nodes: {len(tree.nodes)}</text>'
    )
    svg_parts.append(
        f'<text x="20" y="{stats_y + 30}" font-family="Arial" font-size="9">Terminals: {len(tree.get_all_terminals())}</text>'
    )
    svg_parts.append(
        f'<text x="20" y="{stats_y + 45}" font-family="Arial" font-size="9">Steiner: {len(tree.get_all_steiner_nodes())}</text>'
    )
    svg_parts.append(
        f'<text x="20" y="{stats_y + 60}" font-family="Arial" font-size="9">Wirelength: {tree.calculate_wirelength():.2f}</text>'
    )

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)


def save_routing_tree_svg(
    tree: "GlobalRoutingTree",
    keepouts: Optional[List[Point[Interval[int], Interval[int]]]] = None,
    filename: str = "routing_tree.svg",
    width: int = 800,
    height: int = 600,
) -> None:
    """
    Save the routing tree visualization as an SVG file.

    Args:
        tree: GlobalRoutingTree instance
        filename: Output filename
        width: SVG canvas width
        height: SVG canvas height
    """
    svg_content = visualize_routing_tree_svg(tree, keepouts, width, height, 50)
    with open(filename, "w") as f:
        f.write(svg_content)
    print(f"Routing tree saved to {filename}")


def visualize_routing_tree3d_svg(
    tree3d: "GlobalRoutingTree",
    keepouts: Optional[
        List[Point[Point[Interval[int], Interval[int]], Interval[int]]]
    ] = None,
    scale_z: int = 100,
    width: int = 800,
    height: int = 600,
    margin: int = 50,
) -> str:
    """
    Visualize a GlobalRoutingTree in SVG format.

    .. code-block:: text

            +z
              ^
              |
              |
              +-----> +x
             /
            v
          +y

    Args:
        tree3d: GlobalRoutingTree instance to visualize
        width: SVG canvas width
        height: SVG canvas height
        margin: Margin around the drawing area

    Returns:
        SVG string representation

    Examples:
        >>> from physdes.point import Point
        >>> from physdes.router.routing_tree import GlobalRoutingTree
        >>> tree = GlobalRoutingTree(Point(Point(0, 0), 0))
        >>> s1 = tree.insert_steiner_node(Point(Point(1, 0), 1))
        >>> t1 = tree.insert_terminal_node(Point(Point(2, 0), 2), s1)
        >>> svg = visualize_routing_tree3d_svg(tree, width=200, height=200)
        >>> '<circle cx="50.0" cy="50.0"' in svg
        True
        >>> '<circle cx="100.0" cy="100.0"' in svg
        True
        >>> '<circle cx="150.0" cy="150.0"' in svg
        True
    """
    # Calculate bounds to scale the coordinates
    all_nodes = list(tree3d.nodes.values())
    if not all_nodes:
        return "<svg></svg>"

    layer_colors = ["red", "orange", "blue", "green"]

    # Get all coordinates to determine bounds
    all_x = [node.pt.xcoord.xcoord for node in all_nodes]
    # all_z = [node.pt.xcoord.ycoord for node in all_nodes]
    all_y = [node.pt.ycoord for node in all_nodes]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Add some padding to bounds
    range_x = max_x - min_x
    range_y = max_y - min_y
    if range_x == 0:
        range_x = 1
    if range_y == 0:
        range_y = 1

    # Scale factors
    scale_x = (width - 2 * margin) / range_x
    scale_y = (height - 2 * margin) / range_y
    scale = min(scale_x, scale_y)

    def scale_coords(x, y):
        """Scale coordinates to fit SVG canvas"""
        scaled_x = margin + (x - min_x) * scale
        scaled_y = margin + (y - min_y) * scale
        return scaled_x, scaled_y

    svg_parts = []

    # SVG header
    svg_parts.append(
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    )
    svg_parts.append('<rect width="100%" height="100%" fill="white"/>')

    # Draw connections first (so nodes appear on top)
    def draw_connections(node: "RoutingNode"):
        for child in node.children:
            # Get scaled coordinates
            x1, y1 = scale_coords(node.pt.xcoord.xcoord, node.pt.ycoord)
            x2, y2 = scale_coords(child.pt.xcoord.xcoord, child.pt.ycoord)
            color = layer_colors[
                (child.pt.xcoord.ycoord // scale_z) % len(layer_colors)
            ]
            # Draw line
            svg_parts.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{color}" stroke-width="2" marker-end="url(#arrowhead)"/>'
            )

        for child in node.children:
            draw_connections(child)

    # Add arrowhead marker definition
    svg_parts.append("<defs>")
    svg_parts.append(
        '<marker id="arrowhead" markerWidth="10" markerHeight="7" '
        'refX="9" refY="3.5" orient="auto">'
    )
    svg_parts.append('<polygon points="0 0, 10 3.5, 0 7" fill="black"/>')
    svg_parts.append("</marker>")
    svg_parts.append("</defs>")

    # Draw all connections starting from source
    draw_connections(tree3d.source)

    # Draw nodes
    for node in all_nodes:
        x, y = scale_coords(node.pt.xcoord.xcoord, node.pt.ycoord)

        # Different colors and sizes for different node types
        if node.type == NodeType.SOURCE:
            color = "red"
            radius = 8
            label = "S"
        elif node.type == NodeType.STEINER:
            color = "blue"
            radius = 6
            label = f"S{node.id.split('_')[1]}"
        elif node.type == NodeType.TERMINAL:
            color = "green"
            radius = 6
            label = f"T{node.id.split('_')[1]}"
        else:
            color = "gray"
            radius = 5
            label = node.id

        # Draw node circle
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" stroke="black" stroke-width="1"/>'
        )

        # Draw node label
        svg_parts.append(
            f'<text x="{x + radius + 2}" y="{y + 4}" font-family="Arial" font-size="10" fill="black">{label}</text>'
        )

        # Draw coordinates
        svg_parts.append(
            f'<text x="{x}" y="{y - radius - 5}" font-family="Arial" font-size="8" '
            f'fill="gray" text-anchor="middle">({node.pt.xcoord.xcoord},{node.pt.ycoord})</text>'
        )

    # Draw keepouts
    if keepouts is not None:
        for keepout in keepouts:
            x1, y1 = scale_coords(keepout.xcoord.xcoord.lb, keepout.ycoord.lb)
            x2, y2 = scale_coords(keepout.xcoord.xcoord.ub, keepout.ycoord.ub)
            rwidth = x2 - x1
            rheight = y2 - y1
            color = "pink"
            svg_parts.append(
                f'<rect x="{x1}" y="{y1}" width="{rwidth}" height = "{rheight}" fill="{color}" stroke="black" stroke-width="1"/>'
            )

    # Add legend
    legend_y = 20
    svg_parts.append(
        f'<text x="20" y="{legend_y}" font-family="Arial" font-size="12" font-weight="bold">Legend:</text>'
    )

    legend_items = [
        ("Source", "red", 20, legend_y + 20),
        ("Steiner", "blue", 20, legend_y + 40),
        ("Terminal", "green", 20, legend_y + 60),
    ]

    for text, color, x_pos, y_pos in legend_items:
        svg_parts.append(
            f'<circle cx="{x_pos}" cy="{y_pos - 4}" r="4" fill="{color}" stroke="black"/>'
        )
        svg_parts.append(
            f'<text x="{x_pos + 10}" y="{y_pos}" font-family="Arial" font-size="10">{text}</text>'
        )

    # Display statistics
    stats_y = legend_y + 90
    svg_parts.append(
        f'<text x="20" y="{stats_y}" font-family="Arial" font-size="10" font-weight="bold">Statistics:</text>'
    )
    svg_parts.append(
        f'<text x="20" y="{stats_y + 15}" font-family="Arial" font-size="9">Total Nodes: {len(tree3d.nodes)}</text>'
    )
    svg_parts.append(
        f'<text x="20" y="{stats_y + 30}" font-family="Arial" font-size="9">Terminals: {len(tree3d.get_all_terminals())}</text>'
    )
    svg_parts.append(
        f'<text x="20" y="{stats_y + 45}" font-family="Arial" font-size="9">Steiner: {len(tree3d.get_all_steiner_nodes())}</text>'
    )
    svg_parts.append(
        f'<text x="20" y="{stats_y + 60}" font-family="Arial" font-size="9">Wirelength: {tree3d.calculate_wirelength():.2f}</text>'
    )

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)


def save_routing_tree3d_svg(
    tree3d: "GlobalRoutingTree",
    keepouts: Optional[
        List[Point[Point[Interval[int], Interval[int]], Interval[int]]]
    ] = None,
    scale_z: int = 100,
    filename: str = "routing_tree3d.svg",
    width: int = 800,
    height: int = 600,
) -> None:
    """
    Save the routing tree3d visualization as an SVG file.

    Args:
        tree3d: GlobalRoutingTree instance
        filename: Output filename
        width: SVG canvas width
        height: SVG canvas height
    """
    svg_content = visualize_routing_tree3d_svg(tree3d, keepouts, scale_z, width, height)
    with open(filename, "w") as f:
        f.write(svg_content)
    print(f"Routing tree3d saved to {filename}")


if __name__ == "__main__":
    doctest.testmod()
