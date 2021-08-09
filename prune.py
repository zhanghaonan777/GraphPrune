import pandas as pd
import networkx as nx
from strategy.base import ConstructGraph
from strategy.cut_strategy import CutStrategy
from strategy.remove_strategy import RemoveStrategy

#CG = ConstructGraph("./data/tripartite_data.csv")
CG = ConstructGraph("./data/template_data.csv")
G = CG.build()
RMS = RemoveStrategy()
new_G = RMS.fit_transform(G)
RMS.write_records("./result/test_prune.txt")
CS = CutStrategy()
CS.fit_transform(new_G)
CS.write_records("./result/test_prune.txt")

