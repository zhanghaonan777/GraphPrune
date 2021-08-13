import pandas as pd
import networkx as nx
from strategy.base import ConstructGraph
from strategy.cut_strategy import CutStrategy
from strategy.remove_strategy import RemoveStrategy

#CG = ConstructGraph("./data/tripartite_data.csv")
# params
dim = "KP_level"
value = ["KnowledgePointLevel1", "KnowledgePointLevel2", "KnowledgePointLevel3"]
cut_node_nums = 30
cut_edges_topk = 3

CG = ConstructGraph("./data/template_data.csv")
G = CG.build()
#RMS = RemoveStrategy(dim=dim, value=value)
#new_G = RMS.fit_transform(G)
#RMS.write_records("./result/{}_test_prune.txt".format("-".join(value)))
CS = CutStrategy(cut_node_nums=cut_node_nums, cut_edges_topk=cut_edges_topk)
CS.fit_transform(G)
CS.write_records("./result/cut_{}_test_prune.txt".format("-".join([str(cut_node_nums), str(cut_edges_topk)])))

