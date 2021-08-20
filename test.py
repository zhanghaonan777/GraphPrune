import pandas as pd
import networkx as nx
from strategy.base import ConstructGraph
from strategy.cut_strategy import CutStrategy
from strategy.remove_strategy import RemoveStrategy
from sklearn.model_selection import ParameterGrid

attr_path = "./data/export_kp_labels.csv"
m_nodes_quantile_nums = 0.9
n_nodes_quantile_nums = 0.9

CG = ConstructGraph("./data/tripartite_data_v5.csv")
G = CG.build()
attr_df = pd.read_csv(attr_path)
attr_df["n.kp_id"] = attr_df["n.kp_id"].apply(lambda x: "KnowledgePoint:" + x)
attr_df["KP_level"] = attr_df["labels(n)"].apply(lambda x: x.split(",")[1][:-1])
kp_attr = attr_df.set_index("n.kp_id")["KP_level"].to_dict()
# 增加 KP_level 属性
for kp, kp_level in kp_attr.items():

    if kp in G.nodes:
        G.nodes[kp]["KP_level"] = kp_level

CS = CutStrategy(labels=["KnowledgePoint", "Courseware", "Question"],
                 m_nodes_quantile_nums=m_nodes_quantile_nums, n_nodes_quantile_nums=n_nodes_quantile_nums)
new_G = CS.fit_transform(G)
CS.write_records(
    "./result/test_prune.txt")
