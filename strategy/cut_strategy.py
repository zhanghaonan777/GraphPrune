import networkx as nx
import heapq
from strategy.base import BaseStrategy
from strategy.base import ConstructGraph

class CutStrategy(BaseStrategy):

    def __init__(self, cut_node_nums=30):
        super(CutStrategy, self).__init__()
        self.cut_node_nums = cut_node_nums

    def _fit(self, graph: nx.Graph):

        self.G = graph
        return self

    def _transform(self):

        nodes = sorted(dict(self.G.degree), reverse=True)[:self.cut_node_nums]
        for node in nodes:
            #self.collect_records(node)
            self.remove_nodes_edges(node)
        return self

    def remove_nodes_edges(self, node, topk=3):

        edges = self.G.edges(node)

        degree_list = [self.G.degree(i[1]) for i in edges]
        max_num_index = list(map(degree_list.index, heapq.nlargest(topk, degree_list)))
        need_rm_edges = [list(edges)[index_] for index_ in max_num_index]
        for edge in need_rm_edges:

            self.collect_records(edge[0] + "-" + edge[1])
            self.G.remove_edge(edge[0], edge[1])

        return self

