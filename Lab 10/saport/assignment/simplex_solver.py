import numpy as np
from .model import AssignmentProblem, Assignment, NormalizedAssignmentProblem
from ..simplex.model import Model
from ..simplex.expressions.expression import Expression
from dataclasses import dataclass
from typing import List


class Solver:
    """
    A simplex solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    """

    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        model = Model("assignment")

        for i in range(self.problem.costs.shape[0]):
            for j in range(self.problem.costs.shape[1]):
                model.create_variable(f"x{i, j}")

        for var in model.variables:
            model.add_constraint(var <= 1)

        for i in range(self.problem.costs.shape[1]):
            exp = Expression()
            for x in model.variables[
                     self.problem.costs.shape[0] * i:self.problem.costs.shape[0] * i + self.problem.costs.shape[0]]:
                exp += x
            model.add_constraint((exp == 1))

        for j in range(self.problem.costs.shape[0]):
            exp = Expression()
            for i in range(0, len(model.variables), self.problem.costs.shape[1]):
                exp += model.variables[i + j]
            model.add_constraint((exp == 1))

        exp = Expression.from_vectors(model.variables, self.problem.costs.flatten())

        model.minimize(exp)
        solution = model.solve()

        assignment = [-1] * len(self.problem.original_problem.costs)
        sol = []
        value = 0
        for i in range(self.problem.costs.shape[1]):
            sol.append(solution.assignment[
                       i * self.problem.costs.shape[0]:i * self.problem.costs.shape[0] + self.problem.costs.shape[1]])

        for i in range(len(self.problem.original_problem.costs)):
            for j in range(len(self.problem.original_problem.costs[0])):
                if sol[i][j] == 1:
                    assignment[i] = j
                    value += self.problem.original_problem.costs[i, j]

        return Assignment(assignment, value)
