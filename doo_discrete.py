import numpy as np
import heapq


class DiscreteDOO:
    """一维离散点优化的 DOO 算法 (仅整数)"""

    def __init__(self, f, k, low, high, max_evals=30):
        self.f = f
        self.k = k
        self.low = int(low)
        self.high = int(high)
        self.max_evals = max_evals

        # 存储评估历史
        self.evaluated = {}  # {x: f(x)}
        self.best_x = None
        self.best_value = -np.inf

        # 优先队列: (-upper_bound, cell_id, (low, high))
        self.nodes = []
        self.cell_counter = 0

        # 评估初始点 (中点)
        x0 = (self.low + self.high) // 2
        self._evaluate(x0)

        # 创建根节点
        diam = self.high - self.low
        upper_bound = self.evaluated[x0] + k * diam
        self.cell_counter += 1
        heapq.heappush(self.nodes, (-upper_bound, self.cell_counter, (self.low, self.high)))

    def _evaluate(self, x):
        """评估整数点 x 并更新最佳值"""
        x = int(np.clip(x, self.low, self.high))
        if x in self.evaluated:
            return self.evaluated[x]

        value = self.f(x)
        self.evaluated[x] = value

        if value > self.best_value:
            self.best_value = value
            self.best_x = x

        return value

    def optimize(self):
        """执行优化并返回最佳整数点"""
        eval_count = 1  # 初始点已评估

        while eval_count < self.max_evals and self.nodes:
            # 选择上界最大的区间
            _, _, (low, high) = heapq.heappop(self.nodes)

            # 跳过已评估的单点区间
            if high - low <= 1:
                continue

            # 分裂区间
            mid = (low + high) // 2

            # 评估左半部分中点
            left_mid = (low + mid) // 2
            left_val = self._evaluate(left_mid)
            left_diam = mid - low
            left_ub = left_val + self.k * left_diam

            # 评估右半部分中点
            right_mid = (mid + high) // 2
            right_val = self._evaluate(right_mid)
            right_diam = high - mid
            right_ub = right_val + self.k * right_diam

            # 添加子区间到优先队列
            self.cell_counter += 1
            heapq.heappush(self.nodes, (-left_ub, self.cell_counter, (low, mid)))

            self.cell_counter += 1
            heapq.heappush(self.nodes, (-right_ub, self.cell_counter, (mid, high)))

            eval_count += 2  # 两个新评估点

        return self.best_x, self.best_value