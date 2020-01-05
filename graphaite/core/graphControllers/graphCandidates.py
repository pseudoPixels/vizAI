import pandas as pd
from graphaite.core.utils.dataFrameUtils import *

def get_candidate_graphs(data, **kwargs):
    """
    Given a pandas DataFrame and graph drawing params, returns the list of candidate graphs. THe graph
    selection usually done using the passed x and y axis of the dataset. For example, scatter plot is
    possible candidate when both the axes are available and numeric. Histogram is possible with any of the
    categorical axix and so on.

    :param data: (Pandas DataFrame), the DataFrame to work on
    :param kwargs: (dict kwargs), mainly x and y of the kwargs are checked
    :return: (list) list of candidate graphs
    """

    categorical_features = get_categorical_features(data=data)
    numerical_features = get_numeric_features(data=data)

    x = kwargs['x'] if 'x' in kwargs else None
    y = kwargs['y'] if 'y' in kwargs else None

    print(x, y)



if __name__ == '__main__':
    df = pd.read_csv("../../webapp/datasets/tips.csv")

    get_candidate_graphs(data=df,x="tips")

