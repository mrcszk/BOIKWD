from ..abstractsolver import AbstractSolver
from ..model import Problem, Solution, Item
from typing import List 
from ...integer.model import Model
from ...simplex.expressions.expression import Expression
from ...simplex.expressions.atom import Atom


class IntegerSolver(AbstractSolver):
    """
    An Integer Programming solver for the knapsack problems

    Methods:
    --------
    create_model() -> Models:
        creates and returns an integer programming model based on the self.problem
    """

    def create_model(self) -> Model:
        model = Model("integer_model")
        i = 1
        con = Expression()
        maxi = Expression()
        for x in self.problem.items:
            c = model.create_variable(f"x{i}")
            model.add_constraint(c <= 1)
            con += x.weight * c
            maxi += x.value * c
            i += 1
        model.add_constraint(con <= self.problem.capacity)
        model.maximize(maxi)
        return model
    
    def solve(self) -> Solution:
        m = self.create_model()
        integer_solution = m.solve(self.timelimit)
        items = [item for (i,item) in enumerate(self.problem.items) if integer_solution.value(m.variables[i]) > 0]
        solution = Solution.from_items(items, not m.solver.interrupted)
        self.total_time = m.solver.total_time
        return solution
