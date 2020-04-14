import pandas as pd
from graphaite.core.utils.dataFrameUtils import get_feature_type
from graphaite.core.utils.dataFrameUtils import FeatureType


def get_candidate_graphs(data, x_axis=None, y_axis=None) -> list:
    """ Given a pandas DataFrame and graph drawing params, returns the list of candidate graphs. THe graph
    selection usually done using the passed x and y axis of the dataset. For example, scatter plot is
    possible candidate when both the axes are available and numeric. Histogram is possible with any of the
    categorical axix and so on.
  
    Args:
        data (Pandas DataFrame): the DataFrame to work on
        x_axis (str, optional): name of the feature variable for x axis to use. Defaults to None.
        y_axis (str, optional): name of the feature variable for y axis to use. Defaults to None.
    
    Returns:
        list: list of all possible candidate graph that can be visualized with
    """

    ## if no axes are provided, no graph candidates possible
    if x_axis == None and y_axis == None:
        return None

    ## if x_axis is None, then assign the y_axis to x_axis, since
    ## some plots are possible with only availability of x_axis
    if x_axis == None:
        x_axis = y_axis
        y_axis = None

    graph_candidates = []
    ## Only one feature available
    if y_axis is None:
        graph_candidates.append("histogram")

    ## both the axes are available
    else:
        x_axis_feature_type = get_feature_type(data=data, target_feature=x_axis)
        y_axis_feature_type = get_feature_type(data=data, target_feature=y_axis)

        if (
            x_axis_feature_type == FeatureType.NUMERICAL
            and y_axis_feature_type == FeatureType.NUMERICAL
        ):
            graph_candidates.append("scatter")
            graph_candidates.append("line")
            graph_candidates.append("area")
        if (
            x_axis_feature_type == FeatureType.CATEGORICAL
            and y_axis_feature_type == FeatureType.NUMERICAL
        ):
            graph_candidates.append("box")
            graph_candidates.append("violin")

    if len(graph_candidates) == 0:
        return None

    return graph_candidates


if __name__ == "__main__":
    df = pd.read_csv("../../webapp/datasets/tips.csv")

    get_candidate_graphs(data=df, x="tips")

