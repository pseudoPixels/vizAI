import pandas as pd
from graphaite.core.utils.dataFrameUtils import *

def get_candidate_graphs(data, x_axis=None, y_axis=None)->list:
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
    if x_axis == None and y_axis = None:
        return None

    ## if x_axis is None, then assign the y_axis to x_axis, since
    ## some plots are possible with only availability of x_axis
    if x_axis == None:
        x_axis = y_axis

    


    categorical_features = get_categorical_features(data=data)
    numerical_features = get_numeric_features(data=data)

    x = kwargs['x'] if 'x' in kwargs else None
    y = kwargs['y'] if 'y' in kwargs else None

    print(x, y)



if __name__ == '__main__':
    df = pd.read_csv("../../webapp/datasets/tips.csv")

    get_candidate_graphs(data=df,x="tips")

