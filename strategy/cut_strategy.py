import networkx as nx
import heapq
from strategy.base import BaseStrategy
from strategy.base import ConstructGraph
from graph_stats import degree_select_from_distribute, degree_distribute_stat

class BaseCutStrategy(BaseStrategy):

    def __init__(self, cut_node_nums=30, cut_edges_topk=3):
        super(CutStrategy, self).__init__()
        self.cut_node_nums = cut_node_nums
        self.cut_edges_topk = cut_edges_topk

    def _fit(self, graph: nx.Graph):

        self.G = graph
        return self

    def _transform(self):

        nodes = sorted(dict(self.G.degree), reverse=True)[:self.cut_node_nums]
        for node in nodes:
            #self.collect_records(node)
            self.remove_nodes_edges(node, self.cut_edges_topk)
        return self

    def remove_nodes_edges(self, node, topk):

        edges = self.G.edges(node)

        degree_list = [self.G.degree(i[1]) for i in edges]
        max_num_index = list(map(degree_list.index, heapq.nlargest(topk, degree_list)))
        need_rm_edges = [list(edges)[index_] for index_ in max_num_index]
        for edge in need_rm_edges:
            try:
                self.collect_records(edge[0] + "-" + edge[1])
                self.G.remove_edge(edge[0], edge[1])
            except:
                pass

        return self


class CutStrategy(BaseStrategy):

    def __init__(self, labels, m_nodes_quantile_nums=0.9, n_nodes_quantile_nums=0.9):
        super(CutStrategy, self).__init__()
        self.labels = labels
        self.m_nodes_quantile_nums = m_nodes_quantile_nums
        self.n_nodes_quantile_nums = n_nodes_quantile_nums
        self.labels_details = {}

    def _fit(self, graph: nx.Graph):

        self.G = graph
        #print([i for i in self.G.nodes if self.G.nodes[i]])
        for label in self.labels:
            self.labels_details.update({label: [i for i in self.G.nodes if self.G.nodes[i].get("label") == label]})

        return self

    def _transform(self):

        for label, node_list in self.labels_details.items():
            #print(node_list)
            #nodes = sorted({node:self.G.degree[node] for node in node_list})
            nodes = degree_select_from_distribute({node:self.G.degree[node] for node in node_list},
                                                  self.m_nodes_quantile_nums)

            #nodes = sorted(dict(self.G.degree), reverse=True)[:self.cut_node_nums]
            for node in nodes:
                #self.collect_records(node)
                self.remove_nodes_edges(node, self.n_nodes_quantile_nums)
            print()
        return self

    def remove_nodes_edges(self, node, n_nodes_quantile_nums):

        edges = self.G.edges(node)
        #degree_list = [self.G.degree(i[1]) for i in edges]
        degree_dict = {i[1]:self.G.degree(i[1]) for i in edges}
        rm_edges_nodes = degree_select_from_distribute(degree_dict, n_nodes_quantile_nums)

        #max_num_index = list(map(degree_list.index, heapq.nlargest(topk, degree_list)))
        #need_rm_edges = [list(edges)[index_] for index_ in max_num_index]
        for rm_edges_node in rm_edges_nodes:
            try:
                self.collect_records(node + "-" + rm_edges_node)
                self.G.remove_edge(node, rm_edges_node)
            except:
                pass

        return self
