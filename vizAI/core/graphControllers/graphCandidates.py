import pandas as pd

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

    pass

