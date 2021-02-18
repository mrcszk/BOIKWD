import numpy as np
from .model import Assignment, AssignmentProblem, NormalizedAssignmentProblem
from typing import List, Dict, Tuple, Set


class Solver:
    '''
    A hungarian solver for the assignment problem.

    Methods:
    --------
    __init__(problem: AssignmentProblem):
        creates a solver instance for a specific problem
    solve() -> Assignment:
        solves the given assignment problem
    extract_mins(costs: np.Array):
        substracts from columns and rows in the matrix to create 0s in the matrix
    find_max_assignment(costs: np.Array) -> Dict[int,int]:
        finds the biggest possible assinments given 0s in the cost matrix
        result is a dictionary, where index is a worker index, value is the task index
    add_zero_by_crossing_out(costs: np.Array, partial_assignment: Dict[int,int])
        creates another zero(s) in the cost matrix by crossing out lines (rows/cols) with zeros in the cost matrix,
        then substracting/adding the smallest not crossed out value
    create_assignment(raw_assignment: Dict[int, int]) -> Assignment:
        creates an assignment instance based on the given dictionary assignment
    '''
    def __init__(self, problem: AssignmentProblem):
        self.problem = NormalizedAssignmentProblem.from_problem(problem)

    def solve(self) -> Assignment:
        costs = np.array(self.problem.costs)

        while True:
            self.extracts_mins(costs)
            max_assignment = self.find_max_assignment(costs)
            if len(max_assignment) == self.problem.size():
                return self.create_assignment(max_assignment)
            costs = self.add_zero_by_crossing_out(costs, max_assignment)

    def extracts_mins(self, costs):
        for i in range(costs.shape[0]):
            min_in_row = np.min(costs[i])
            for j in range(costs.shape[1]):
                costs[i, j] = costs[i, j] - min_in_row

        for j in range(costs.shape[1]):
            min_in_col = np.min(costs[:, j])
            for i in range(costs.shape[0]):
                costs[i, j] = costs[i, j] - min_in_col

    def add_zero_by_crossing_out(self, costs: np.array, partial_assignment: Dict[int,int]):
        assignment = [-2]*(costs.shape[1])
        for key, value in partial_assignment.items():
            assignment[key] = value

        rows_not_used = np.where(np.array(assignment) == -2)[0]

        row_to_omit = []
        col_with_0 = []
        for row in rows_not_used:
            col_with_0.append(np.where(costs[row] == 0)[0])

        for col in col_with_0:
            row_to_omit.append(np.where(np.array(assignment) == col))

        rows = [0]*costs.shape[1]

        for x in list(rows_not_used):
            rows[x] = 1

        for x in row_to_omit[0]:
            rows[int(x)] = 1

        row_to_cross = np.where(np.array(rows) == 0)

        new_tab = np.delete(costs, row_to_cross, 0)
        new_tab = np.delete(new_tab, col_with_0, 1)

        minimum = np.amin(new_tab)

        costs = costs - minimum

        for x in row_to_cross:
            costs[x, :] = costs[x, :] + minimum

        for x in col_with_0:
            costs[:, x] = costs[:, x] + minimum

        return costs

    def find_max_assignment(self, costs) -> Dict[int,int]:
        assigment = {}
        rows = []
        for i in range(costs.shape[0]):
            row = np.where(costs[i] == 0)[0]
            rows.append(row)

        loop = True
        lit = 0
        while loop:
            min_list_row = []
            min_in_row = 0
            for i in range(len(rows)):
                if len(rows[i]) != 0 and min_list_row == []:
                    min_list_row = rows[i]
                    min_in_row = i
                    if len(min_list_row) == 1:
                        break
                elif len(rows[i]) != 0 and len(rows[i]) < len(min_list_row):
                    min_list_row = rows[i]
                    min_in_row = i
                    if len(min_list_row) == 1:
                        break

            if min_in_row not in assigment:
                assigment[min_in_row] = min_list_row[0]
                for i in range(len(rows)):
                    for x in min_list_row:
                        rows[i] = np.delete(rows[i], np.where(rows[i] == x))

            for x in rows:
                if len(x) != 0 and lit < 15:
                    loop = True
                    lit += 1
                    break
                loop = False

        return assigment

    def create_assignment(self, raw_assignment: Dict[int, int]) -> Assignment:
        assignment = [-1] * len(self.problem.original_problem.costs)
        objective = 0

        for key in raw_assignment:
            if self.problem.original_problem.costs.shape[0] > key \
                    and self.problem.original_problem.costs.shape[1] > raw_assignment[key]:
                assignment[key] = raw_assignment[key]
                objective += self.problem.original_problem.costs[key, raw_assignment[key]]

        return Assignment(assignment, objective)
