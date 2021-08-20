import pandas as pd
import networkx as nx
from strategy.base import ConstructGraph
from strategy.cut_strategy import CutStrategy
from strategy.remove_strategy import RemoveStrategy
from sklearn.model_selection import ParameterGrid
from copy import deepcopy

#CG = ConstructGraph("./data/tripartite_data.csv")
# params
version = "v2_new"

dim = ["KP_level"]
value = ["KnowledgePointLevel1", "KnowledgePointLevel2", "KnowledgePointLevel3", ["KnowledgePointLevel1", "KnowledgePointLevel2"]]
m_nodes_quantile_nums = [0.95, 0.9, 0.85, 0.8]
n_nodes_quantile_nums = [0.95, 0.9, 0.85, 0.8]
mode = ["RemoveStrategy", "CutStrategy", "all"]

#
RemoveStrategyParams = {
    'dim': dim,
    'value': value,
    'm': ['x'],
    'n': ['x'],
    'mode': ["RemoveStrategy"]
}

CutStrategyParams = {
    'dim': dim,
    'value': ['x'],
    'm': m_nodes_quantile_nums,
    'n': n_nodes_quantile_nums,
    'mode': ["CutStrategy"]
}
AllStrategyParams = {

    'dim': dim,
    'value': value,
    'm': m_nodes_quantile_nums,
    'n': n_nodes_quantile_nums,
    'mode': ["all"]
}


attr_path = "./data/export_kp_labels.csv"
attr_df = pd.read_csv(attr_path)
attr_df["n.kp_id"] = attr_df["n.kp_id"].apply(lambda x:"KnowledgePoint:" + x)
attr_df["KP_level"] = attr_df["labels(n)"].apply(lambda x:x.split(",")[1][:-1])
kp_attr = attr_df.set_index("n.kp_id")["KP_level"].to_dict()

CG = ConstructGraph("./data/tripartite_data_v2.csv")
Origin_G = CG.build()


def run_exp(params):

    dim = params.get("dim")
    value = params.get("value")
    mode = params.get("mode")
    m = params.get("m")
    n = params.get("n")

    G = deepcopy(Origin_G)
    # 增加 KP_level 属性
    for kp, kp_level in kp_attr.items():

        if kp in G.nodes:
            G.nodes[kp]["KP_level"] = kp_level

    if mode == "RemoveStrategy":
        #del params["cut_node_nums"], params["cut_edges_topk"]
        RMS = RemoveStrategy(dim=dim, value=value)
        new_G = RMS.fit_transform(G)
        RMS.write_records("./result/{}/{}_test_prune.txt".format(version, "-".join([str(i).replace(" ",'') for i in params.values()])))
    elif mode == "CutStrategy":
        #del params["dim"], params["value"]
        CS = CutStrategy(labels=["KnowledgePoint", "Courseware", "Question"] ,m_nodes_quantile_nums=m, n_nodes_quantile_nums=n)
        new_G = CS.fit_transform(G)
        CS.write_records("./result/{}/{}_test_prune.txt".format(version, "-".join([str(i).replace(" ", '') for i in params.values()])))
    else:
        RMS = RemoveStrategy(dim=dim, value=value)
        new_G = RMS.fit_transform(G)
        RMS.write_records("./result/{}/{}_test_prune.txt".format(version, "-".join([str(i).replace(" ", '') for i in params.values()])))
        CS = CutStrategy(labels=["KnowledgePoint", "Courseware", "Question"], m_nodes_quantile_nums=m, n_nodes_quantile_nums=n)
        new_G = CS.fit_transform(new_G)
        CS.write_records("./result/{}/{}_test_prune.txt".format(version, "-".join([str(i).replace(" ", '') for i in params.values()])))
    # 清空缓存
    del G


if __name__ == "__main__":

    print("-" * 100, "AllParams")
    grid_search_params = ParameterGrid(AllStrategyParams)
    for params_ in grid_search_params:
        print(params_)
        run_exp(params_)
    grid_search_params = ParameterGrid(RemoveStrategyParams)
    print("-" * 100, "RemoveStrategyParams")
    for params_ in grid_search_params:
        print(params_)
        run_exp(params_)
    #
    # print("-" * 100, "CutStrategyParams")
    # grid_search_params = ParameterGrid(CutStrategyParams)
    # for params_ in grid_search_params:
    #     print(params_)
    #     run_exp(params_)