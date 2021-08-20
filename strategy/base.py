import networkx as nx
import pandas as pd
from collections import defaultdict

class BaseStrategy(object):

    def __init__(self, *args):
        self._is_fitted = False
        self._collect = defaultdict(list)

    @property
    def is_fitted(self):
        """Whether `fit` has been called."""
        return self._is_fitted

    def check_is_fitted(self):
        """Check if the estimator has been fitted.

        Raises
        ------
        NotFittedError
            If the estimator has not been fitted yet.
        """
        if not self.is_fitted:
            raise AttributeError(
                f"This instance of {self.__class__.__name__} has not "
                f"been fitted yet; please call `fit` first."
            )

    def fit(self, X):

        self._fit(X)
        self._is_fitted = True
        return self

    def transform(self):

        self.check_is_fitted()
        self._transform()
        return self.G

    def fit_transform(self, X):

        self.fit(X)
        self.transform()
        return self.G

    def _fit(self):

        raise NotImplementedError("abstract method")

    def _transform(self):

        raise NotImplementedError("abstract method")

    def collect_records(self, x):

        self._collect[self.__class__.__name__].append(x)

    def get_records(self):

        return self._collect


    def write_records(self, result_path):

        result = self.get_records()
        with open(result_path, "a+") as f:
            for strategy, values in result.items():
                for value_ in values:
                    f.write(strategy + "@" + value_)
                    f.write("\n")


class ConstructGraph(object):

    def __init__(self, file_path=None, graph_df=None):

        self._is_build = False
        self.file_path = file_path
        self.graph_df = graph_df
        self.G = nx.Graph()

    @property
    def is_build(self):

        return self._is_build

    def build(self):

        if self.file_path:
            self._build_from_file()
        else:
            self._build_from_df()
        self._is_build = True
        return self.G

    def check_is_build(self):
        """Check if the estimator has been fitted.

        Raises
        ------
        NotFittedError
            If the estimator has not been fitted yet.
        """
        if not self.is_build:
            raise AttributeError(
                f"This instance of {self.__class__.__name__} has not "
                f"been build yet; please call `build` first."
            )


    def _build_from_file(self):

        self.graph_df = pd.read_csv(self.file_path, sep="\t", header=None)
        # process
        self._build_from_df()
        self._is_build = True
        return self

    def _build_from_df(self):

        edges = [i for i in zip(self.graph_df[0].apply(lambda x:x.split("&")[1] if "&" in x else x).to_list(), self.graph_df[1].to_list())]
        self.G.add_edges_from(edges)
        # node attr
        node_attr = {i.split("&")[1]: i.split("&")[0] for i in self.graph_df[0].tolist() if "&" in i}
        for node, attr in node_attr.items():

            # 增加 kp level 属性
            self.add_node_attr(node, "KP_level", attr)

        # 增加label Question:ff8080814cdb1d93014ce51dabdc1d30 -> Question
        for node_ in self.G.nodes:

            self.add_node_attr(node_, "label", node_.split(":")[0])

        self._is_build = True
        return self

    def add_node_attr(self, node, key, value):

        self.G.nodes[node][key] = value
        return self

    def graph_stat(self, topk=20):

        self.check_is_build()
        nodes_count = self.G.number_of_nodes()
        edges_count = self.G.number_of_edges()
        stat_dic = {
            "nodes_count": nodes_count,
            "edges_count": edges_count
        }
        return stat_dic




