import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import deque
import heapq


class DOO:
    """
    Deterministic Optimistic Optimization (DOO) Algorithm

    适用于：k-Lipschitz 连续函数的全局优化
    假设：已知 Lipschitz 常数 k 和搜索空间的分层划分结构
    """

    def __init__(self, f, k, bounds, max_evals=100):
        # 1. 首先初始化所有属性（关键顺序！）
        self.f = f
        self.k = k
        self.bounds = np.array(bounds)
        self.dim = len(bounds)
        self.max_evals = max_evals

        # 初始化数据结构（必须在使用前定义！）
        self.evaluated_points = []  # 存储已评估点
        self.evaluated_values = []  # 存储已评估值
        self.best_point = None
        self.best_value = -np.inf
        self.nodes = []  # ← 关键：初始化优先队列为空列表
        self._node_counter = 0  # 唯一ID计数器（用于打破平局）

        # 2. 然后创建根节点
        root_center = np.mean(self.bounds, axis=1)
        root_value = self._evaluate(root_center)
        root_diam = self._diameter(self.bounds)
        root_upper_bound = root_value + self.k * root_diam

        # 3. 构建根节点字典
        root_node = {
            'bounds': self.bounds.copy(),
            'center': root_center,
            'value': root_value,
            'diam': root_diam,
            'upper_bound': root_upper_bound,
            'depth': 0
        }

        # 4. 现在可以安全推送到堆
        self._node_counter += 1
        heapq.heappush(self.nodes, (-root_upper_bound, self._node_counter, root_node))

    def _diameter(self, bounds):
        """计算 cell 的直径（欧几里得距离）"""
        # 对于超矩形，直径是对角线长度
        return np.linalg.norm(bounds[:, 1] - bounds[:, 0])

    def _evaluate(self, point):
        """评估函数值并更新最佳点"""
        value = self.f(point)
        self.evaluated_points.append(point.copy())
        self.evaluated_values.append(value)

        if value > self.best_value:
            self.best_value = value
            self.best_point = point.copy()

        return value

    def _split_node(self, node):
        """将节点沿最长维度二分"""
        bounds = node['bounds'].copy()

        # 找到最长维度
        lengths = bounds[:, 1] - bounds[:, 0]
        split_dim = np.argmax(lengths)
        split_point = (bounds[split_dim, 0] + bounds[split_dim, 1]) / 2

        # 创建两个子节点
        children = []
        for i in [0, 1]:
            child_bounds = bounds.copy()
            if i == 0:
                child_bounds[split_dim, 1] = split_point
            else:
                child_bounds[split_dim, 0] = split_point

            # 计算子节点中心
            child_center = np.mean(child_bounds, axis=1)

            # 评估子节点中心
            child_value = self._evaluate(child_center)
            child_diam = self._diameter(child_bounds)
            child_upper_bound = child_value + self.k * child_diam

            child_node = {
                'bounds': child_bounds,
                'center': child_center,
                'value': child_value,
                'diam': child_diam,
                'upper_bound': child_upper_bound,
                'depth': node['depth'] + 1
            }
            children.append(child_node)

        return children

    def optimize(self):
        eval_count = 1
        while eval_count < self.max_evals and self.nodes:
            # 修复解包：三个变量
            _, _, node = heapq.heappop(self.nodes)  # ← 关键修复行

            children = self._split_node(node)
            eval_count += len(children)

            for child in children:
                self._node_counter += 1
                # 保持三元组格式
                heapq.heappush(
                    self.nodes,
                    (-child['upper_bound'], self._node_counter, child)
                )

        return self.best_point, self.best_value