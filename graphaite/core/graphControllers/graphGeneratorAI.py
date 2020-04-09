from graphaite.core.graphControllers.graphCandidates import get_candidate_graphs
import pathlib
import pandas as pd

def get_auto_generated_graphs(dataset, feature_variables=None, target_variable=None):
    """Auto generates graphs based on feature variables data types. 
    This method uses rules based AI to generate graphs.
    
    Args:
        dataset (pandas dataframe): The Dataset to generate visualizations on
        feature_variables (list of string, optional): Preferred list of features to use for making the visualizations. Defaults to None.
        target_variable (string, optional): The target variable against which the visualization to make. Defaults to None.
    """

    if feature_variables == None:
        return None
    
    auto_visualizations = []
    ## univariate vizualizations
    for aFeature in feature_variables:
        graph_candidates = get_candidate_graphs(data=dataset, x_axis=aFeature)
        auto_visualizations.append(graph_candidates)

    return auto_visualizations

if __name__ == "__main__":
    WEBAPP_DIR = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/webapp/"
    df = pd.read_csv(WEBAPP_DIR+"/datasets/titanic.csv")
    
    l = get_auto_generated_graphs(dataset=df, feature_variables=["sex", "age"])


    print(l)
    # df = pd.read_csv(WEBAPP_DIR+"/datasets/titanic.csv")