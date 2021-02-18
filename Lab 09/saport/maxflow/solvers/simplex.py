from .solver import AbstractSolver
from ...simplex.model import Model as LinearModel
from ...simplex.expressions.expression import Expression as LinearExpression
import numpy as np
from ..model import Network


class SimplexSolver(AbstractSolver):

    def solve(self) -> int:
        m = LinearModel(self.network.name)

        exp = LinearExpression()
        for x in self.network.digraph.edges:
            v = m.create_variable(f"x{x}")
            m.add_constraint(v <= self.network.capacity(self.network.digraph, x[0], x[1]))
            if x[0] == 0:
                exp += v

        list_in = []
        for i in range(0, self.network.digraph.number_of_nodes()):
            list_in.append(self.network.digraph.in_edges(i))
        list_out = []
        for i in range(0, self.network.digraph.number_of_nodes()):
            list_out.append(self.network.digraph.out_edges(i))

        for i in range(len(list_in)):
            if self.network.digraph.out_edges(i) and self.network.digraph.in_edges(i) and i != self.network.source_node and i != self.network.sink_node:
                exp2 = LinearExpression()
                for x in list_in[i]:
                    exp2 += m.variables[[v.index for v in m.variables if v.name == f"x{x}"].pop()]
                for x in list_out[i]:
                    exp2 -= m.variables[[v.index for v in m.variables if v.name == f"x{x}"].pop()]
                m.add_constraint(exp2 == 0)
            elif i == self.network.source_node and list_in[i]:
                exp2 = LinearExpression()
                for x in list_in[i]:
                    exp2 += m.variables[[v.index for v in m.variables if v.name == f"x{x}"].pop()]
                m.add_constraint(exp2 == 0)
            elif i == self.network.sink_node and list_out[i]:
                exp2 = LinearExpression()
                for x in list_out[i]:
                    exp2 += m.variables[[v.index for v in m.variables if v.name == f"x{x}"].pop()]
                m.add_constraint(exp2 == 0)

        m.maximize(exp)
        solution = m.solve()
        return int(solution.objective_value())


