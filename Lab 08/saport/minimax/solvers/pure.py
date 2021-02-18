from dataclasses import dataclass
from .solver import AbstractSolver
from ..model import Game, Equilibrium, Strategy
from typing import List
import numpy as np


class PureSolver(AbstractSolver):

    def solve(self) -> List[Equilibrium]:
        mini = []
        mini_result = []
        maxi = []
        maxi_result = []
        for x in self.game.reward_matrix:
            mini.append(np.amin(x))
            result = np.where(x == np.amin(x))
            mini_result.append(result[0])

        for x in range(self.game.reward_matrix.shape[1]):
            y = np.array(self.game.reward_matrix[:, x])
            maxi.append(np.amax(y))
            result = np.where(y == np.amax(y))
            maxi_result.append(result[0])

        equ = []
        for i in range(len(mini)):
            for j in range(len(maxi)):
                if mini[i] == maxi[j]:
                    if self.game.reward_matrix[maxi_result[j], mini_result[i]] == mini[i]:
                        strategy_a = [0] * self.game.reward_matrix.shape[0]
                        strategy_b = [0] * self.game.reward_matrix.shape[1]
                        strategy_a[maxi_result[j][0]] = 1
                        strategy_b[mini_result[i][0]] = 1
                        equ.append(Equilibrium(mini[i], Strategy(strategy_a), Strategy(strategy_b)))

        return equ



