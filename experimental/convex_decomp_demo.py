import matplotlib.pyplot as plt
import numpy as np


class Point:
    """表示二维点"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"


class RectilinearPolygon:
    """表示直角多边形"""

    def __init__(self, vertices):
        """
        初始化直角多边形
        参数: vertices - 按顺时针或逆时针顺序排列的顶点列表
        """
        self.vertices = [Point(v[0], v[1]) for v in vertices]
        self.edges = []

        # 创建边
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            self.edges.append((p1, p2))

    def is_convex_vertex(self, p_prev, p_curr, p_next):
        """
        判断顶点是否为凸点
        对于直角多边形，内角为90°(凸)或270°(凹)
        假设顶点按顺时针顺序排列
        """
        # 计算向量
        v1 = (p_curr.x - p_prev.x, p_curr.y - p_prev.y)
        v2 = (p_next.x - p_curr.x, p_next.y - p_curr.y)

        # 计算叉积的z分量 (在2D中)
        cross_z = v1[0] * v2[1] - v1[1] * v2[0]

        # 对于顺时针多边形，凸点的叉积为正（指向屏幕外）
        return cross_z > 0

    def find_concave_vertices(self):
        """查找所有凹点（内角为270°的顶点）"""
        concave_vertices = []
        n = len(self.vertices)

        for i in range(n):
            p_prev = self.vertices[(i - 1) % n]
            p_curr = self.vertices[i]
            p_next = self.vertices[(i + 1) % n]

            if not self.is_convex_vertex(p_prev, p_curr, p_next):
                concave_vertices.append((i, p_curr))

        return concave_vertices

    def point_on_edge(self, p, edge):
        """检查点是否在边上（包括端点）"""
        p1, p2 = edge

        # 检查是否在边界框内
        min_x = min(p1.x, p2.x)
        max_x = max(p1.x, p2.x)
        min_y = min(p1.y, p2.y)
        max_y = max(p1.y, p2.y)

        if not (min_x <= p.x <= max_x and min_y <= p.y <= max_y):
            return False

        # 检查共线性
        # 对于轴对齐边，只需检查x或y坐标是否相等
        if p1.x == p2.x:  # 垂直线
            return abs(p.x - p1.x) < 1e-9
        else:  # 水平线
            return abs(p.y - p1.y) < 1e-9

    def find_intersection(self, p, direction, edges_to_ignore=None):
        """
        从点p沿方向direction延伸，找到与多边形边界的第一个交点
        方向: 'left', 'right', 'up', 'down'
        返回交点坐标，如果找不到则返回None
        """
        if edges_to_ignore is None:
            edges_to_ignore = []

        best_intersection = None
        min_distance = float("inf")

        for i, edge in enumerate(self.edges):
            if i in edges_to_ignore:
                continue

            p1, p2 = edge

            # 根据方向计算可能的交点
            if direction == "left":
                # 向左延伸，寻找垂直线段
                if p1.x == p2.x and p1.x < p.x:  # 垂直线在左侧
                    # 检查y坐标是否在线段范围内
                    min_y = min(p1.y, p2.y)
                    max_y = max(p1.y, p2.y)
                    if min_y <= p.y <= max_y:
                        distance = p.x - p1.x
                        if distance < min_distance:
                            min_distance = distance
                            best_intersection = Point(p1.x, p.y)

            elif direction == "right":
                # 向右延伸，寻找垂直线段
                if p1.x == p2.x and p1.x > p.x:  # 垂直线在右侧
                    min_y = min(p1.y, p2.y)
                    max_y = max(p1.y, p2.y)
                    if min_y <= p.y <= max_y:
                        distance = p1.x - p.x
                        if distance < min_distance:
                            min_distance = distance
                            best_intersection = Point(p1.x, p.y)

            elif direction == "down":
                # 向下延伸，寻找水平线段
                if p1.y == p2.y and p1.y < p.y:  # 水平线在下方
                    min_x = min(p1.x, p2.x)
                    max_x = max(p1.x, p2.x)
                    if min_x <= p.x <= max_x:
                        distance = p.y - p1.y
                        if distance < min_distance:
                            min_distance = distance
                            best_intersection = Point(p.x, p1.y)

            elif direction == "up":
                # 向上延伸，寻找水平线段
                if p1.y == p2.y and p1.y > p.y:  # 水平线在上方
                    min_x = min(p1.x, p2.x)
                    max_x = max(p1.x, p2.x)
                    if min_x <= p.x <= max_x:
                        distance = p1.y - p.y
                        if distance < min_distance:
                            min_distance = distance
                            best_intersection = Point(p.x, p1.y)

        return best_intersection

    def get_possible_cut_directions(self, p_prev, p_curr, p_next):
        """
        根据凹点的相邻边确定可能的切割方向
        返回方向列表
        """
        directions = []

        # 确定相邻边的方向
        prev_vector = (p_curr.x - p_prev.x, p_curr.y - p_prev.y)
        next_vector = (p_next.x - p_curr.x, p_next.y - p_curr.y)

        # 由于是直角多边形，向量只能是(±dx,0)或(0,±dy)
        # 凹点的特征是两条相邻边指向同一个象限

        # 找出缺失的方向（指向多边形内部的方向）
        # 对于凹点，向内方向是两个相邻边的反向
        if prev_vector[0] > 0:  # 从左来
            if next_vector[1] > 0:  # 向上去
                # 凹点在左下角，可能向右或向下切割
                directions = ["right", "down"]
            elif next_vector[1] < 0:  # 向下去
                # 凹点在左上角，可能向右或向上切割
                directions = ["right", "up"]
        elif prev_vector[0] < 0:  # 从右来
            if next_vector[1] > 0:  # 向上去
                # 凹点在右下角，可能向左或向下切割
                directions = ["left", "down"]
            elif next_vector[1] < 0:  # 向下去
                # 凹点在右上角，可能向左或向上切割
                directions = ["left", "up"]
        elif prev_vector[1] > 0:  # 从下来
            if next_vector[0] > 0:  # 向右去
                # 凹点在左下角，可能向右或向上切割
                directions = ["right", "up"]
            elif next_vector[0] < 0:  # 向左去
                # 凹点在右下角，可能向左或向上切割
                directions = ["left", "up"]
        elif prev_vector[1] < 0:  # 从上来
            if next_vector[0] > 0:  # 向右去
                # 凹点在左上角，可能向右或向下切割
                directions = ["right", "down"]
            elif next_vector[0] < 0:  # 向左去
                # 凹点在右上角，可能向左或向下切割
                directions = ["left", "down"]

        return directions

    def convex_decomposition_by_concave_cutting(self):
        """
        基于凹点切割的凸分解算法
        返回凸多边形列表
        """
        # 复制当前多边形进行分解
        poly = RectilinearPolygon([(v.x, v.y) for v in self.vertices])
        convex_parts = []

        # 递归分解直到多边形成为凸多边形
        def decompose_recursive(polygon):
            # 检查是否为凸多边形（没有凹点）
            concave_vertices = polygon.find_concave_vertices()

            if not concave_vertices:
                # 已经是凸多边形
                convex_parts.append(polygon.vertices)
                return

            # 选择第一个凹点进行切割
            idx, concave_vertex = concave_vertices[0]
            n = len(polygon.vertices)

            # 获取相邻顶点
            p_prev = polygon.vertices[(idx - 1) % n]
            p_curr = concave_vertex
            p_next = polygon.vertices[(idx + 1) % n]

            # 获取可能的切割方向
            directions = polygon.get_possible_cut_directions(p_prev, p_curr, p_next)

            # 尝试每个可能的切割方向
            cut_successful = False
            for direction in directions:
                # 寻找切割线终点
                intersection = polygon.find_intersection(p_curr, direction)

                if intersection and intersection != p_curr:
                    # 创建切割线
                    cut_line = (p_curr, intersection)

                    # 将多边形分割为两个子多边形
                    sub_polys = polygon.split_by_cut_line(idx, cut_line)

                    if sub_polys and len(sub_polys) == 2:
                        # 递归分解子多边形
                        for sub_poly in sub_polys:
                            decompose_recursive(sub_poly)
                        cut_successful = True
                        break

            if not cut_successful:
                # 如果切割失败，使用备选方案：矩形剖分
                print("切割失败，使用矩形剖分作为备选")
                rectangles = polygon.simple_rectangle_partition()
                for rect in rectangles:
                    convex_parts.append(rect)

        decompose_recursive(poly)
        return convex_parts

    def split_by_cut_line(self, vertex_idx, cut_line):
        """
        用切割线分割多边形
        返回两个子多边形，如果分割失败则返回None
        """
        p1, p2 = cut_line

        # 获取多边形顶点列表
        vertices = self.vertices

        # 找到切割线终点在多边形边上的位置
        end_on_edge = False
        end_edge_idx = -1

        for i, edge in enumerate(self.edges):
            if self.point_on_edge(p2, edge) and p2 != edge[0] and p2 != edge[1]:
                end_on_edge = True
                end_edge_idx = i
                break

        if not end_on_edge:
            # 终点不在边上，分割失败
            return None

        # 创建两个子多边形的顶点列表
        poly1_vertices = []
        poly2_vertices = []

        # 第一个子多边形：从凹点到切割点，然后沿多边形边界回到起点
        # 从凹点开始
        start_idx = vertex_idx

        # 找到终点所在的边
        end_edge = self.edges[end_edge_idx]
        end_edge_start, end_edge_end = end_edge

        # 确定终点在边上的顺序
        # 计算终点到边起点的距离
        abs(p2.x - end_edge_start.x) + abs(p2.y - end_edge_start.y)
        abs(p2.x - end_edge_end.x) + abs(p2.y - end_edge_end.y)

        # 将顶点添加到第一个多边形
        # 从凹点开始，沿多边形边界到终点
        current_idx = start_idx
        while True:
            poly1_vertices.append(vertices[current_idx])
            if current_idx == end_edge_idx:
                # 到达终点所在的边
                # 添加切割终点
                poly1_vertices.append(p2)
                break
            current_idx = (current_idx + 1) % len(vertices)

        # 添加从切割终点经切割起点回到凹点的路径
        poly1_vertices.append(p1)

        # 第二个子多边形：从切割点到凹点，然后沿多边形边界回到切割点
        # 从切割终点开始
        poly2_vertices.append(p2)

        # 沿多边形边界到凹点
        current_idx = (end_edge_idx + 1) % len(vertices)
        while current_idx != (start_idx + 1) % len(vertices):
            poly2_vertices.append(vertices[current_idx])
            current_idx = (current_idx + 1) % len(vertices)

        # 添加凹点
        poly2_vertices.append(p1)

        # 检查两个多边形是否有效（至少3个顶点）
        if len(poly1_vertices) < 3 or len(poly2_vertices) < 3:
            return None

        # 创建多边形对象
        poly1 = RectilinearPolygon([(v.x, v.y) for v in poly1_vertices])
        poly2 = RectilinearPolygon([(v.x, v.y) for v in poly2_vertices])

        return [poly1, poly2]

    def simple_rectangle_partition(self):
        """
        简单的矩形剖分算法（备选方案）
        返回矩形顶点列表的列表
        """
        # 找到多边形的边界框
        min_x = min(v.x for v in self.vertices)
        max_x = max(v.x for v in self.vertices)
        min_y = min(v.y for v in self.vertices)
        max_y = max(v.y for v in self.vertices)

        # 简单的网格剖分（这里简化为将多边形分割为两个矩形）
        # 在实际应用中，应实现更复杂的矩形剖分算法
        rectangles = []

        # 这是一个简化的示例：找到多边形的大致中点进行分割
        mid_x = (min_x + max_x) / 2

        # 创建两个矩形（假设分割线在x=mid_x处）
        rect1 = [
            Point(min_x, min_y),
            Point(mid_x, min_y),
            Point(mid_x, max_y),
            Point(min_x, max_y),
        ]

        rect2 = [
            Point(mid_x, min_y),
            Point(max_x, min_y),
            Point(max_x, max_y),
            Point(mid_x, max_y),
        ]

        rectangles.append(rect1)
        rectangles.append(rect2)

        return rectangles

    def get_edges(self):
        """获取多边形的边"""
        return self.edges


def generate_rectilinear_polygon():
    """生成一个示例直角多边形"""
    # 创建一个L形直角多边形
    vertices = [
        (0, 0),  # 左下角
        (8, 0),  # 右下角
        (8, 4),  # 右中角
        (4, 4),  # 凹点
        (4, 8),  # 中上角
        (0, 8),  # 左上角
    ]
    return RectilinearPolygon(vertices)


def generate_complex_rectilinear_polygon():
    """生成一个更复杂的直角多边形"""
    vertices = [
        (1, 1),  # 起点
        (10, 1),  # 右1
        (10, 4),  # 上1
        (7, 4),  # 凹点1
        (7, 7),  # 上2
        (4, 7),  # 左1
        (4, 4),  # 凹点2
        (1, 4),  # 左2
    ]
    return RectilinearPolygon(vertices)


def plot_polygon_decomposition(polygon, convex_parts):
    """绘制多边形及其凸分解结果"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 绘制原始多边形
    ax1.set_title("原始直角多边形")
    ax1.set_aspect("equal")

    # 绘制顶点
    vertices = polygon.vertices
    xs = [v.x for v in vertices]
    ys = [v.y for v in vertices]
    xs.append(vertices[0].x)  # 闭合多边形
    ys.append(vertices[0].y)
    ax1.plot(xs, ys, "b-", linewidth=2, label="边界")
    ax1.scatter(xs[:-1], ys[:-1], c="red", s=50, zorder=5, label="顶点")

    # 标记凹点
    concave_vertices = polygon.find_concave_vertices()
    concave_xs = [v[1].x for v in concave_vertices]
    concave_ys = [v[1].y for v in concave_vertices]
    ax1.scatter(concave_xs, concave_ys, c="orange", s=100, marker="s", zorder=6, label="凹点")

    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 绘制凸分解结果
    ax2.set_title(f"凸分解结果 (共{len(convex_parts)}个凸多边形)")
    ax2.set_aspect("equal")

    # 为每个凸部分使用不同颜色
    colors = plt.cm.tab20(np.linspace(0, 1, len(convex_parts)))

    for i, part in enumerate(convex_parts):
        # 提取顶点坐标
        part_xs = [v.x for v in part]
        part_ys = [v.y for v in part]
        part_xs.append(part[0].x)  # 闭合多边形
        part_ys.append(part[0].y)

        # 绘制填充区域
        ax2.fill(part_xs, part_ys, alpha=0.5, color=colors[i])

        # 绘制边界
        ax2.plot(part_xs, part_ys, "k-", linewidth=1.5)

        # 标记顶点
        ax2.scatter(part_xs[:-1], part_ys[:-1], c="black", s=30, zorder=5)

        # 添加凸部分标签
        centroid_x = sum(v.x for v in part) / len(part)
        centroid_y = sum(v.y for v in part) / len(part)
        ax2.text(
            centroid_x,
            centroid_y,
            str(i + 1),
            fontsize=12,
            fontweight="bold",
            ha="center",
            va="center",
        )

    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def print_polygon_info(polygon):
    """打印多边形信息"""
    print("=" * 60)
    print("直角多边形信息:")
    print(f"顶点数: {len(polygon.vertices)}")
    print("顶点坐标:", polygon.vertices)

    concave_vertices = polygon.find_concave_vertices()
    print(f"凹点数量: {len(concave_vertices)}")
    if concave_vertices:
        print("凹点位置:", [v[1] for v in concave_vertices])

    print("=" * 60)


def main():
    """主函数"""
    print("直角多边形凸分解算法演示")
    print("=" * 60)

    # 选择多边形示例
    print("请选择多边形示例:")
    print("1. 简单L形多边形")
    print("2. 复杂直角多边形")
    choice = input("请输入选择 (1或2): ").strip()

    if choice == "1":
        polygon = generate_rectilinear_polygon()
    elif choice == "2":
        polygon = generate_complex_rectilinear_polygon()
    else:
        print("无效选择，使用默认L形多边形")
        polygon = generate_rectilinear_polygon()

    # 打印多边形信息
    print_polygon_info(polygon)

    # 执行凸分解
    print("正在进行凸分解...")
    convex_parts = polygon.convex_decomposition_by_concave_cutting()

    print(f"分解完成! 共得到 {len(convex_parts)} 个凸多边形")
    for i, part in enumerate(convex_parts):
        print(f"凸多边形 {i+1}: 顶点数={len(part)}, 顶点={part}")

    # 可视化结果
    plot_polygon_decomposition(polygon, convex_parts)

    # 算法分析
    print("\n算法分析:")
    print("-" * 40)
    print("1. 算法类型: 基于凹点切割的贪心算法")
    print("2. 基本思想: 识别凹点并向内延伸切割线，将多边形分割为凸部分")
    print("3. 时间复杂度: O(n²)，其中n为顶点数")
    print("4. 优点: 直观易懂，能处理大多数直角多边形")
    print("5. 局限性: 可能不是最优分解（凸片数最少），切割线选择可能影响结果")
    print("6. 改进方向:")
    print("   - 使用更智能的切割方向选择策略")
    print("   - 考虑全局最优而不是贪心局部选择")
    print("   - 实现更高效的矩形剖分算法作为备选")


if __name__ == "__main__":
    main()
