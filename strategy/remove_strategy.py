import networkx as nx
import heapq
from strategy.base import BaseStrategy
from strategy.base import ConstructGraph

class RemoveStrategy(BaseStrategy):

    def __init__(self, dim="KP_level", value="KnowledgePointLevel1"):
        super(RemoveStrategy, self).__init__()
        self.dim = dim
        if type(value) == str:
            self.value = [value]
        else:
            self.value = value

    def _fit(self, graph: nx.Graph):

        self.G = graph
        return self

    def _transform(self):

        need_rm_nodes = [node for node in self.G.nodes() if self.G.nodes[node].get(self.dim) in self.value]
        for need_rm_node in need_rm_nodes:
            self.remove_node(need_rm_node)
        return self.G

    def remove_node(self, node):

        self.collect_records(node)
        self.G.remove_node(node)
        return self

