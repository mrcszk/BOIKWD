from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
from typing import List 
class AbstractBnbSolver(AbstractSolver):
    """
    An abstract branch-and-bound solver for the knapsack problems.

    Methods:
    --------
    upper_bound(left : List[Item], solution: Solution) -> float:
        given the list of still available items and the current solution,
        calculates the linear relaxation of the problem
    """
    
    def upper_bound(self, left : List[Item], solution: Solution) -> float:
        now_weight = solution.weight
        now_value = solution.value
        sorted_items = sorted(left, key=lambda item: item.value/item.weight, reverse=True)

        for x in sorted_items:
            if now_weight + x.weight > self.problem.capacity:
                space = self.problem.capacity - now_weight
                part = space / x.weight
                now_value += x.value * part
                return now_value
            now_value = now_value + x.value
            now_weight = now_weight + x.weight

        return now_value

        
    def solve(self) -> Solution:
        raise Exception("this is an abstract solver, don't try to run it!")