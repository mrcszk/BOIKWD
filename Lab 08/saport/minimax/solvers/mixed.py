from dataclasses import dataclass
from .solver import AbstractSolver
from ..model import Game, Equilibrium, Strategy
from ...simplex import model as lpmodel
from ...simplex import solution as lpsolution
from ...simplex.expressions import expression as expr
import numpy as np
from typing import Tuple, List


class MixedSolver(AbstractSolver):

    def solve(self) -> Equilibrium:
        shifted_game, shift = self.shift_game_rewards()

        # don't remove this print, it will be graded :)
        print(f"- shifted game: \n{shifted_game}")

        a_model = self.create_max_model(shifted_game)
        b_model = self.create_min_model(shifted_game)       
        a_solution = a_model.solve()
        b_solution = b_model.solve()
        a_probabilities = self.extract_probabilities(a_solution)
        b_probabilities = self.extract_probabilities(b_solution)
        return Equilibrium(a_solution.objective_value() - shift, Strategy(a_probabilities), Strategy(b_probabilities))

    def shift_game_rewards(self) -> Tuple[Game, float]:
        mini = []
        for x in self.game.reward_matrix:
            mini.append(np.amin(x))

        if np.amax(mini) < 0:
            shift = -1 * np.amax(mini)
        else:
            shift = 0

        return Game(self.game.reward_matrix + shift), shift

    def create_max_model(self, game: Game) -> lpmodel.Model:
        a_actions, b_actions = game.reward_matrix.shape

        a_model = lpmodel.Model("A")
        exp = expr.Expression()
        for i in range(1, a_actions + 1):
            e = a_model.create_variable(f"x{i}")
            exp += e
        z = a_model.create_variable(f"z")
        a_model.add_constraint(exp == 1)
        for j in range(b_actions):
            cons = expr.Expression()
            for i in range(a_actions):
                cons += -1 * game.reward_matrix[i, j] * a_model.variables[i]
            a_model.add_constraint(z + cons <= 0)

        a_model.maximize(z)
        return a_model

    def create_min_model(self, game: Game) -> lpmodel.Model:
        a_actions, b_actions = game.reward_matrix.shape

        b_model = lpmodel.Model("B")
        exp = expr.Expression()
        for i in range(1, b_actions + 1):
            e = b_model.create_variable(f"x{i}")
            # a_model.add_constraint(e >= 0)
            exp += e
        z = b_model.create_variable(f"z")
        b_model.add_constraint(exp == 1)
        for x in game.reward_matrix:
            cons = expr.Expression()
            for i in range(b_actions):
                cons += -1 * x[i] * b_model.variables[i]
            b_model.add_constraint(z + cons >= 0)

        b_model.minimize(z)

        return b_model

    def extract_probabilities(self, solution: lpsolution.Solution) -> List[float]:
        return [solution.value(x) for x in solution.model.variables if not solution.model.objective.depends_on_variable(solution.model, x)]

