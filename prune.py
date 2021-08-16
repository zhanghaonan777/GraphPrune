import pandas as pd
import networkx as nx
from strategy.base import ConstructGraph
from strategy.cut_strategy import CutStrategy
from strategy.remove_strategy import RemoveStrategy
from sklearn.model_selection import ParameterGrid

#CG = ConstructGraph("./data/tripartite_data.csv")
# params
dim = ["KP_level"]
value = ["KnowledgePointLevel1", "KnowledgePointLevel2", "KnowledgePointLevel3"]
cut_node_nums = [30]
cut_edges_topk = [3]
mode = ["RemoveStrategy", "CutStrategy", "all"]

params = {
    'dim': dim,
    'value': value,
    'cut_node_nums': cut_node_nums,
    'cut_edges_topk': cut_edges_topk,
    'mode': mode
}

def run_exp(params):

    dim = params["dim"]
    value = params["value"]
    cut_node_nums = params["cut_node_nums"]
    cut_edges_topk = params["cut_edges_topk"]
    mode = params["mode"]

    CG = ConstructGraph("./data/template_data.csv")
    G = CG.build()
    if params["mode"] == "RemoveStrategy":
        del params["cut_node_nums"], params["cut_edges_topk"]
        RMS = RemoveStrategy(dim=dim, value=value)
        new_G = RMS.fit_transform(G)
        RMS.write_records("./result/{}_test_prune.txt".format("-".join([str(i) for i in params.values()])))
    elif params["mode"] == "CutStrategy":
        del params["dim"], params["value"]
        CS = CutStrategy(cut_node_nums=params["cut_node_nums"], cut_edges_topk=params["cut_edges_topk"])
        new_G = CS.fit_transform(G)
        CS.write_records("./result/{}_test_prune.txt".format("-".join([str(i) for i in params.values()])))
    else:
        RMS = RemoveStrategy(dim=dim, value=value)
        new_G = RMS.fit_transform(G)
        RMS.write_records("./result/{}_test_prune.txt".format("-".join([str(i) for i in params.values()])))
        CS = CutStrategy(cut_node_nums=params["cut_node_nums"], cut_edges_topk=params["cut_edges_topk"])
        new_G = CS.fit_transform(new_G)
        CS.write_records("./result/{}_test_prune.txt".format("-".join([str(i) for i in params.values()])))


if __name__ == "__main__":
    grid_search_params = ParameterGrid(params)
    for params_ in grid_search_params:
        print(params_)
        run_exp(params_)
