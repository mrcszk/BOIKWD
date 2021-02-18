from copy import deepcopy
from .expressions.variable import Variable
from .expressions.objective import Objective, ObjectiveType
from saport.simplex.expressions.constraint import *


class Solution:
    """
        A class to represent a solution to linear programming problem.


        Attributes
        ----------
        model : Model
            model corresponding to the solution
        assignment : list[float]
            list with the values assigned to the variables
            order of values should correspond to the order of variables in model.variables list


        Methods
        -------
        __init__(model: Model, assignment: list[float]) -> Solution:
            constructs a new solution for the specified model and assignment
        value(var: Variable) -> float:
            returns a value assigned to the specified variable
        objective_value()
            returns value of the objective function
    """

    def __init__(self, model, assignment):
        "Assignment is just a list of values"
        self.assignment = assignment
        self.model = model

    def value(self, var):
        return self.assignment[var.index]

    def objective_value(self):
        return self.model.objective.evaluate(self.assignment)       

    def __str__(self):
        print(self.model)
        text = f'- objective value: {self.objective_value()}\n'
        text += '- assignment:\n'
        for (i, var) in enumerate(self.assignment):
            text += f'\t {self.model.variables[i].name} : {var}'
        return text




class Solver:
    """
        A class to represent a simplex solver.

        Methods
        -------
        solve(model: Model) -> Solution:
            solves the given model and return the first solution
    """

    def __init__(self):
        self.new_variables = 1
        self.sol = []

    def solve(self, model):
        normal_model = self._normalize_model(deepcopy(model))
        solution = self._find_initial_solution(normal_model)
        tableaux = self._tableux(normal_model, solution)
        #TODO: 
        # - print normal model
        # - print initial solution
        # - print tableux

        self._print(tableaux)

        return solution

    def _normalize_model(self, model):
        """
            _normalize_model(model: Model) -> Model:
                returns a normalized version of the given model 
        """
        #TODO: this method should create a new canonical model based on the current one
        # - canonical model has only the MAX objective
        # - canonical model has only EQ constraints (thanks to the additional slack / surplus variables)
        #   you should add extra (slack, surplus) variables and store them somewhere as the solver attribute

        normalized_model = model

        if normalized_model.objective.type == ObjectiveType.MIN:
            normalized_model.maximize(model.objective.expression)
            for i in range(0, len(normalized_model.objective.expression.atoms)):
                normalized_model.objective.expression.atoms[i].factor *= (-1)

        for x in normalized_model.constraints:
            # if x.bound == 0:
            #     continue
            v = normalized_model.create_variable(f's{self.new_variables}')
            if x.type == ConstraintType.LE:
                x.expression = x.expression + v
            else:
                x.expression = x.expression - v
            x.type = ConstraintType.EQ
            self.new_variables += 1

        return normalized_model

    def _find_initial_solution(self, model):
        """
        _find_initial_solution(model: Model) -> Solution
            returns an initial solution for the given model
        """
        #TODO: this method should find an initial feasible solution to the model
        # - should use the slack / surplus variables added during the normalization

        normalized_model = model
        assignment = [0] * (len(normalized_model.variables) - self.new_variables + 1)

        for x in normalized_model.constraints:
            assignment.append(x.bound)

        return Solution(normalized_model, assignment)

    def _tableux(self, model, solution):
        """
        _tableux(model: Model, solution: Solution) -> list[list[float]]
            returns a tableux for the given model and solution
        """
        normalized_model = model

        #TODO: this method should create an array (list of lists is fine, but you can change it)
        # representing the tableux for the given model and solution
        len_var = len(normalized_model.variables)
        len_con = len(normalized_model.constraints)

        # first row - letters
        tab = []
        for i in range(0, len_var + 3):
            if i == 0 or i == len_var + 2:
                tab.append(' ')
            elif i == 1:
                tab.append('z')
            else:
                tab.append(normalized_model.variables[i-2].name)
        self.sol.append(tab)

        # second row
        tab = []
        for i in range(0, len_var+2):
            if i == 0:
                tab.append(1)
            elif i > len_var - self.new_variables+1:
                tab.append(0)
            else:
                tab.append(normalized_model.objective.expression.atoms[i-1].factor * (-1))

        tab.insert(0, 'z')
        self.sol.append(tab)
        # rest of rows
        for j in range(0, len_con):
            tab = [normalized_model.variables[len_var - self.new_variables + j + 1].name]
            for i in range(0, len_var+2):
                if i == 0:
                    tab.append(0)
                elif i <= len_var - len_con:
                    if i < len(normalized_model.constraints[j].expression.atoms):
                        tab.append(normalized_model.constraints[j].expression.atoms[i-1].factor)
                elif i == len_var - len_con + j + 1:
                    tab.append(normalized_model.constraints[j].expression.
                               atoms[len(normalized_model.constraints[j].expression.atoms)-1].factor)
                elif i == len_var+1:
                    tab.append(normalized_model.constraints[j].bound)
                else:
                    tab.append(0)
            self.sol.append(tab)

        return self.sol

    def _print(self, tableaux):
        print("tableaux:")
        for row in tableaux:
            print(''.join(str(x).ljust(7) for x in row))
        print("\n")
