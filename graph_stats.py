import pandas as pd

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
