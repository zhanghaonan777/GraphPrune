import pandas as pd
import networkx as nx
from strategy.base import ConstructGraph
from strategy.cut_strategy import CutStrategy
from strategy.remove_strategy import RemoveStrategy
from sklearn.model_selection import ParameterGrid

#CG = ConstructGraph("./data/tripartite_data.csv")
# params
dim = ["KP_level"]
value = ["KnowledgePointLevel1", "KnowledgePointLevel2", "KnowledgePointLevel3", ["KnowledgePointLevel1", "KnowledgePointLevel2"]]
cut_node_nums = [30, 50, 100, 300, 500, 1000]
cut_edges_topk = [3, 5, 10, 50, 100]
mode = ["RemoveStrategy", "CutStrategy", "all"]

params = {
    'dim': dim,
    'value': value,
    'cut_node_nums': cut_node_nums,
    'cut_edges_topk': cut_edges_topk,
    'mode': mode
}
attr_path = "./data/export_kp_labels.csv"

def run_exp(params):

    dim = params["dim"]
    value = params["value"]
    cut_node_nums = params["cut_node_nums"]
    cut_edges_topk = params["cut_edges_topk"]
    mode = params["mode"]

    CG = ConstructGraph("./data/tripartite_data_v3.csv")
    G = CG.build()
    attr_df = pd.read_csv(attr_path)
    attr_df["n.kp_id"] = attr_df["n.kp_id"].apply(lambda x:"KnowledgePoint:" + x)
    attr_df["KP_level"] = attr_df["labels(n)"].apply(lambda x:x.split(",")[1][:-1])
    kp_attr = attr_df.set_index("n.kp_id")["KP_level"].to_dict()
    for kp, kp_level in kp_attr.items():

        if kp in G.nodes:
            G.nodes[kp]["KP_level"] = kp_level

    if params["mode"] == "RemoveStrategy":
        del params["cut_node_nums"], params["cut_edges_topk"]
        RMS = RemoveStrategy(dim=dim, value=value)
        new_G = RMS.fit_transform(G)
        RMS.write_records("./result/v3/{}_test_prune.txt".format("-".join([str(i).replace(" ",'') for i in params.values()])))
    elif params["mode"] == "CutStrategy":
        del params["dim"], params["value"]
        CS = CutStrategy(cut_node_nums=params["cut_node_nums"], cut_edges_topk=params["cut_edges_topk"])
        new_G = CS.fit_transform(G)
        CS.write_records("./result/v3/{}_test_prune.txt".format("-".join([str(i).replace(" ", '') for i in params.values()])))
    else:
        RMS = RemoveStrategy(dim=dim, value=value)
        new_G = RMS.fit_transform(G)
        RMS.write_records("./result/v3/{}_test_prune.txt".format("-".join([str(i).replace(" ", '') for i in params.values()])))
        CS = CutStrategy(cut_node_nums=params["cut_node_nums"], cut_edges_topk=params["cut_edges_topk"])
        new_G = CS.fit_transform(new_G)
        CS.write_records("./result/v3/{}_test_prune.txt".format("-".join([str(i).replace(" ", '') for i in params.values()])))


if __name__ == "__main__":
    grid_search_params = ParameterGrid(params)
    for params_ in grid_search_params:
        print(params_)
        run_exp(params_)
