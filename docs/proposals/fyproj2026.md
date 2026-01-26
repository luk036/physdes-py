# 多FPGA系统多网络路由最终项目提案

## 项目标题
基于Steiner Forest算法的多FPGA系统多网络路由优化

## 1. 项目背景与意义

### 1.1 研究背景
随着现代电子系统复杂性的不断增加，单个FPGA往往无法满足大规模设计的需求。多FPGA系统通过将设计分割到多个FPGA上，成为实现大规模数字电路的有效解决方案。然而，在多FPGA系统中，如何高效地路由跨FPGA的网络连接成为一个关键挑战。

### 1.2 研究意义
- **实际应用价值**：多FPGA系统在高性能计算、原型验证和大规模数字系统设计中应用广泛
- **技术挑战**：多网络路由需要解决资源竞争、拥塞管理和跨FPGA连接优化问题
- **理论贡献**：将Steiner Forest算法应用于多FPGA路由可为该领域提供新的解决方案

## 2. 文献综述与现状分析

### 2.1 Steiner Forest问题
Steiner Forest问题是经典Steiner Tree问题的推广，是网络优化中的重要问题。该问题寻求在图中找到连接指定终端对的最小成本子图。

### 2.2 现有FPGA路由算法
- 传统单网络路由算法：主要针对单个网络进行优化
- 多网络路由算法：考虑多网络间的资源竞争
- 现有算法缺乏对多FPGA系统特殊约束的考虑

### 2.3 项目基础
本项目基于physdes-py库中的Steiner Forest实现，该实现采用原始对偶方法，具有良好的理论基础和实现质量。

## 3. 研究目标与内容

### 3.1 主要研究目标
1. **算法扩展**：将Steiner Forest算法扩展到多FPGA系统环境
2. **拥塞管理**：实现有效的拥塞感知路由算法
3. **多网络优化**：解决多网络间的资源竞争问题
4. **性能评估**：验证算法在多FPGA环境中的有效性

### 3.2 具体研究内容
1. **多FPGA环境建模**：建立适合多FPGA系统的图论模型
2. **改进的Steiner Forest算法**：针对多FPGA系统特点优化算法
3. **拥塞感知机制**：在路由过程中考虑资源拥塞
4. **优先级调度策略**：为不同网络分配路由优先级
5. **实现与验证**：实现算法并进行实验验证

## 4. 技术路线与方法

### 4.1 算法设计
基于physdes-py库中的steiner_forest_grid实现，进行以下扩展：

1. **资源约束建模**：
   - FPGA内部连接：较低成本
   - 跨FPGA连接：较高成本（考虑延迟、带宽限制）

2. **拥塞管理**：
   - 实时更新拥塞图
   - 在边成本中添加拥塞惩罚项

3. **多网络处理**：
   - 网络优先级排序
   - 迭代式多网络路由

### 4.2 实现方案
```python
def multi_fpga_multi_net_routing(
    fpga_grid_height: int,
    fpga_grid_width: int,
    fpga_count: int,
    net_pairs: List[List[Tuple[Tuple[int, int], Tuple[int, int]]]],
    fpga_mapping: Dict[Tuple[int, int], int]
) -> Dict:
    """
    多FPGA系统多网络路由实现
    """
    congestion_map = [[0 for _ in range(fpga_grid_width)] for _ in range(fpga_grid_height)]

    all_routes = []
    total_cost = 0.0

    # 为每个网络计算带拥塞惩罚的Steiner Forest
    for i, pairs in enumerate(net_pairs):
        routes, cost, sources, terminals, steiner_nodes = steiner_forest_with_congestion(
            fpga_grid_height, fpga_grid_width, pairs, congestion_map
        )

        # 更新拥塞图
        update_congestion_map(congestion_map, routes)

        all_routes.append({
            'net_id': i,
            'routes': routes,
            'cost': cost,
            'sources': sources,
            'terminals': terminals,
            'steiner_nodes': steiner_nodes
        })

        total_cost += cost

    return {
        'all_routes': all_routes,
        'total_cost': total_cost,
        'congestion_map': congestion_map,
        'fpga_mapping': fpga_mapping
    }
```

### 4.3 实验方法
1. **仿真实验**：在模拟的多FPGA环境中测试算法性能
2. **对比实验**：与传统路由算法进行性能对比
3. **参数调优**：优化算法参数以获得最佳性能

## 5. 预期成果

### 5.1 理论成果
- 多FPGA系统多网络路由的理论模型
- 改进的Steiner Forest算法及其性能分析

### 5.2 实践成果
- 多FPGA多网络路由算法的Python实现
- 完整的测试用例和性能评估
- 详细的文档和使用示例

### 5.3 学术成果
- 最终项目报告
- 可能的学术论文发表

## 6. 项目实施计划

### 第一阶段（1-4周）：文献调研与理论分析
- 深入研究Steiner Forest算法理论
- 分析多FPGA系统路由特点
- 完善问题建模

### 第二阶段（5-8周）：算法设计与实现
- 扩展Steiner Forest算法
- 实现拥塞管理机制
- 开发多网络处理功能

### 第三阶段（9-12周）：实验验证与优化
- 设计实验方案
- 实现测试用例
- 性能评估与算法优化

### 第四阶段（13-16周）：文档撰写与总结
- 撰写项目报告
- 整理实验结果
- 准备项目答辩

## 7. 项目可行性分析

### 7.1 技术可行性
- 有成熟的Steiner Forest算法作为基础
- physdes-py库提供了良好的代码基础
- 算法理论基础扎实

### 7.2 资源可行性
- 项目基于现有开源库，无需额外硬件资源
- Python实现便于开发和测试
- 有充分的文档和示例参考

### 7.3 时间可行性
- 项目范围适中，符合最终项目要求
- 分阶段实施计划合理可行
- 有明确的里程碑和评估指标

## 8. 创新点

1. **算法创新**：将Steiner Forest算法首次系统性地应用于多FPGA系统多网络路由
2. **模型创新**：提出适合多FPGA环境的拥塞感知路由模型
3. **实现创新**：基于physdes-py库的可扩展实现架构

## 9. 预期挑战与解决方案

### 9.1 主要挑战
- 多网络间的复杂资源竞争
- 跨FPGA连接的时序约束
- 算法复杂度与性能的平衡

### 9.2 解决方案
- 采用迭代优化策略
- 引入优先级调度机制
- 使用启发式算法降低复杂度

## 10. 评估指标

- **路由成功率**：成功路由的网络比例
- **总成本**：路由总成本（包括延迟、功耗等）
- **拥塞水平**：资源拥塞程度
- **运行时间**：算法执行时间
- **资源利用率**：FPGA资源使用效率

---
**提案人**：[学生姓名]
**指导教师**：[教师姓名]
**提交日期**：2025年
