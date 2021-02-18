from .solver import AbstractSolver
from ..model import Network

import networkx as nx
from typing import List
import numpy as np
import time


class EdmondsKarp(AbstractSolver):

    def solve(self) -> int:
        # basic body for the edmonds-karp algorithm
        max_flow = 0
        rgraph = self.create_residual_graph()
        apath = self.find_augmenting_path(rgraph, self.network.source_node, self.network.sink_node)
        while apath != None:
            max_flow += self.update_residual_graph(rgraph, apath)
            apath = self.find_augmenting_path(rgraph, self.network.source_node, self.network.sink_node)
        return max_flow

    def create_residual_graph(self) -> nx.DiGraph:
        rgraph = nx.DiGraph()
        rgraph = self.network.digraph.copy()
        for x in self.network.digraph.edges:
            capacity = self.network.capacity(self.network.digraph, x[0], x[1])
            rgraph.add_edge(x[1], x[0], capacity=0, label=(str(capacity) + "++"))
        return rgraph

    def find_augmenting_path(self, graph: nx.DiGraph, src: int, sink: int) -> List[int]:
        queue = [src]
        path = {src: []}

        while queue:
            elem = queue.pop()
            for v in graph.out_edges(elem):
                v = list(v)
                if self.network.capacity(graph, v[0], v[1]) > 0 and v[1] not in path:
                    path[v[1]] = path[elem] + [(elem, v[1])]
                    if v[1] == sink:
                        out = [item for t in path[v[1]] for item in t]
                        res = []
                        [res.append(x) for x in out if x not in res]
                        return res
                    queue.append(v[1])

    def update_residual_graph(self, graph: nx.DiGraph, path: List[int]) -> int:
        flow = float('inf')

        mini = []
        for i in range(len(path) - 1):
            mini.append(self.network.capacity(graph, path[i], path[i + 1]))

        flow = min(mini)
        for i in range(len(path) - 1):
            self.network.set_capacity(graph, path[i], path[i + 1], mini[i] - flow)

        for i in range(len(path), 0):
            self.network.set_capacity(graph, path[i], path[i - 1], mini[i] + flow)

        return flow
