from copy import deepcopy
from ..simplex import solver as lpsolver
import math
import time


class Solver:
    """
        Naive branch and bound solver for integer programming problems


        Attributes
        ----------
        model : Model
            integer programming model to be solved
        timelimit: int
            what is the maximal solving time (in seconds)
        total_time: float
            how long it took to solve the problem
        start_time: float
            when the solving started
        interrupted: bool
            whether solving has been interrupted (by timeout)

        Methods
        -------
        start_timer():
            remember the starting time for the solver
        stop_timer():
            stores the total solving time
        wall_time() -> float:
            returns how long solver has been working
        timeout() -> bool:
            whether solver should stop working due to the timeout

        solve(model: Model, timelimit: int) -> Solution:
            solves the given model within a specified timelimit
        branch_and_bound(model: Model):
            processes given model in branch and bound fashion (recursively)
        find_float_assignment(solution: Solution):
            finds a variable with non-integer value in the current solution
            returns None if the solution is a correct integer solution
        model_with_new_constraint(self, model, constraint):
            creates a new model with an additional constraint
    """

    def solve(self, model, timelimit):
        self.timelimit = timelimit
        self.total_time = None
        self.start_time = None
        self.interrupted = False

        self.model = model
        self.lower_bound = float('-inf')
        self.best_solution = None

        self.start_timer()
        self.branch_and_bound(model)
        self.stop_timer()

        return self.best_solution

    def branch_and_bound(self, model):
        if self.timeout():
            self.interrupted = True
            return

        sol = lpsolver.Solver().solve(model)

        if not sol.is_feasible:
            return

        if not sol.is_bounded:
            return

        change, i = self.find_float_assignment(sol)

        if self.lower_bound > sol.objective_value():
            return

        if change is None:
            if self.lower_bound < sol.objective_value():
                self.lower_bound = sol.objective_value()
                self.best_solution = sol
            return

        model2 = self.model_with_new_constraint(model, model.variables[i] >= (int(change) + 1))
        self.branch_and_bound(model2)

        model3 = self.model_with_new_constraint(model, model.variables[i] <= (int(change)))
        self.branch_and_bound(model3)

    def find_float_assignment(self, solution):
        i = 0
        for x in solution.assignment:
            y = int(x * 100000000)
            if int(x) * 100000000 != y:
                return x, i
            i += 1
        return None, i

    def model_with_new_constraint(self, model, constraint):
        new_model = deepcopy(model)
        new_model.add_constraint(constraint)
        return new_model

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        self.total_time = self.wall_time()

    def wall_time(self) -> float:
        return time.time() - self.start_time

    def timeout(self) -> bool:
        return self.wall_time() > self.timelimit
