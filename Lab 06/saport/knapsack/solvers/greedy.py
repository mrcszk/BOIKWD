from numpy.core.arrayprint import format_float_positional
from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
import time


class AbstractGreedySolver(AbstractSolver):
    """
    An abstract greedy solver for the knapsack problems.

    Methods:
    --------
    greedy_heuristic(item : Item) -> float:
        return a value representing how much the given items is valuable to the greedy algorithm
        bigger value > earlier to take in the backpack
    """

    def greedy_heuristic(self, item: Item) -> float:
        raise Exception("Greedy solver requires a heuristic!")

    def solve(self) -> Solution:
        now_weight = 0
        now_value = 0
        choosen_items = []
        self.start_timer()

        sorted_items = sorted(self.problem.items, key=self.greedy_heuristic, reverse=True)
        for x in sorted_items:
            if now_weight + x.weight <= self.problem.capacity:
                choosen_items.append(x)
                now_weight = now_weight + x.weight
                now_value = now_value + x.value
        self.stop_timer()

        return Solution(items=choosen_items, value=now_value, weight=now_weight, optimal=False)