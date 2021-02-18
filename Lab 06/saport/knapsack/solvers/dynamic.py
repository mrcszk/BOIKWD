from ..abstractsolver import AbstractSolver
from ..model import Solution
import numpy as np
from typing import Tuple

class DynamicSolver(AbstractSolver):
    """
    A naive dynamic programming solver for the knapsack problem. 
    """
    def create_table(self) -> np.array:
        try:
            table = np.zeros((self.problem.capacity + 1, len(self.problem.items) + 1), int)

            for y in range(1, len(table[0])):
                for x in range(1, len(table)):
                    if self.timeout():
                        self.interrupted = True
                        return table
                    item = self.problem.items[y - 1]
                    if item.weight > x:
                        table[x, y] = table[x, y - 1]
                    else:
                        table[x, y] = max(table[x, y - 1], table[x - item.weight, y - 1] + item.value)
            return table
        except MemoryError:
            return None

    def extract_solution(self, table : np.array) -> Solution:
        used_items = []
        optimal = table[-1, -1] > 0

        now_value = table[-1, -1]
        now_row = table.shape[0]-1

        for y in range(table.shape[1]-1, 0, -1):
            if now_value > table[now_row, y-1]:
                item = self.problem.items[y - 1]
                used_items.append(item)
                now_value = now_value - item.value
                for i in range(table.shape[0]):
                    if table[i, -1] == now_value:
                        now_row = i

        return Solution.from_items(used_items, optimal)

    def solve(self) -> Tuple[Solution, float]:
        self.interrupted = False
        self.start_timer()
        
        table = self.create_table()
        solution = self.extract_solution(table) if table is not None else Solution.empty()

        self.stop_timer()
        return solution