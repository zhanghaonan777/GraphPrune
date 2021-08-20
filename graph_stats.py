import pandas as pd

def degree_select_from_distribute(degree_dict, quantile_nums):
    degree_series = pd.Series(degree_dict)
    nums_ = degree_series.quantile(quantile_nums)
    degree_series = degree_series[degree_series > nums_]
    return degree_series.index

def degree_distribute_stat(degree_dict):
    """
    :return
        {'count': 4.0,
         'mean': 46.0,
         'std': 55.575774098672404,
         'min': 1.0,
         '25%': 7.75,
         '50%': 30.0,
         '75%': 68.25,
         'max': 123.0}
    """
    degree_series = pd.Series(degree_dict)
    return degree_series.describe().to_dict()

def degree_select_from_nums(degree_dict, nums):
    return degree_dict[:nums]


def degree_stats(df, top_strategy_):
    """

    :param df:
    :return:
    """
    # get relation
    df["relation"] = df.apply(lambda row: row[0].split(":")[0] + "-" + row[1].split(":")[0], axis=1)
    having_relations = list(set(df["relation"]))
    for relation_ in having_relations:
        df_ = df[df["relation"] == relation_]


def _degree_stats(df_, top_strategy_):

    a, b = df_.columns()
    a_ser = df_.groupby(a).b.apply(len).sort_values(ascending=False)
    b_ser = df_.groupby(b).a.apply(len).sort_values(ascending=False)
    print("node count of " + a + ":" + len(a_ser))
    print("node count of " + b + ":" + len(b_ser))
    print()





if __name__ == "__main__":
    data = pd.read_csv("./data/tripartite_data.csv", sep="\t", header=None)
    degree_stats(data)
