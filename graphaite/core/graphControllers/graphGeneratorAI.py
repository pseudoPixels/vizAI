from graphaite.core.graphControllers.graphCandidates import get_candidate_graphs
from graphaite.core.visualizers.plotly.makePlots import *


import pathlib
import pandas as pd
import uuid


def get_auto_generated_graphs(dataset, feature_variables=None, target_variable=None):
    """Auto generates graphs based on feature variables data types. 
    This method uses rules based AI to generate graphs.
    
    Args:
        dataset (pandas dataframe): The Dataset to generate visualizations on
        feature_variables (list of string, optional): Preferred list of features to use for making the visualizations. Defaults to None.
        target_variable (string, optional): The target variable against which the visualization to make. Defaults to None.
    
    Returns:
        dict : {
            'plot_id_1': {
                'figure_data' : {<plotly Json Object>},
                'feature_tags' : ['tag_1', 'tag_2', '...'],
                'graph_settings' : {<kwargs for the corresponding graph settings>},
                "graph_id": <unique id which can be used for storing/tracking this graph in db>
            },

            'plot_id_2': {
                'figure_data' : {<plotly Json Object>},
                'feature_tags' : ['tag_A', 'tag_B', '...'],
                'graph_settings' : {<kwargs for the corresponding graph settings>},
                "graph_id": <unique id which can be used for storing/tracking this graph in db>
            },
            ...
        }
    
    """

    if feature_variables == None:
        return None

    auto_visualizations = {}

    ## univariate vizualizations
    for aFeature in feature_variables:
        ## based on the feature(s), get the possible graph candidates
        graph_candidates = get_candidate_graphs(data=dataset, x_axis=aFeature)

        ## in case we have got some graph candidates, lets visualize with them
        if graph_candidates != None:
            for aGraphCandidate in graph_candidates:
                ## settings for that particular graph
                ## TODO: should be obtained from corresponding graph definitions.
                graph_settings = {
                    "chart_type": aGraphCandidate,
                    "x": aFeature,
                    "color": target_variable,
                    "barmode": "group",
                    "template": "presentation",
                    "height": 430,
                }

                ## Visualize with data and graph settings
                fig_data = get_plot(data=dataset, **graph_settings)

                ## Add feature tags
                feature_tags = []
                feature_tags.append(aFeature)

                ## Assign unique graph id
                plot_id = str(
                    uuid.uuid4()
                )  ## TODO: plot id will have to fetched from db

                ## add the graph to return object
                auto_visualizations[plot_id] = {
                    "figure_data": fig_data,
                    "feature_tags": feature_tags,
                    "graph_settings": graph_settings,
                    "graph_id": plot_id,
                }

    ##Bivariate Features
    for xFeature in feature_variables:
        for yFeature in feature_variables:
            if xFeature != yFeature:

                ## Get possible graph candidates with the corresponding features
                graph_candidates = get_candidate_graphs(
                    data=dataset, x_axis=xFeature, y_axis=yFeature
                )

                ## in case we have got some graph candidates, lets visualize with them
                if graph_candidates != None:
                    for aGraphCandidate in graph_candidates:

                        ## settings for that particular graph
                        ## TODO: should be obtained from corresponding graph definitions.
                        graph_settings = {
                            "chart_type": aGraphCandidate,
                            "x": xFeature,
                            "y": yFeature,
                            "color": target_variable,
                            "barmode": "group",
                            "template": "presentation",
                            "height": 430,
                        }
                        ## Visualize with data and graph settings
                        fig_data = get_plot(data=dataset, **graph_settings)
                        ## Add feature tags
                        feature_tags = []
                        feature_tags.append(xFeature)
                        feature_tags.append(yFeature)

                        ## Assign unique graph id
                        plot_id = str(
                            uuid.uuid4()
                        )  ## TODO: plot id will have to fetched from db

                        ## Add the plot info to return dictionary object
                        auto_visualizations[plot_id] = {
                            "figure_data": fig_data,
                            "feature_tags": feature_tags,
                            "graph_settings": graph_settings,
                            "graph_id": plot_id,
                        }

    return auto_visualizations


if __name__ == "__main__":
    WEBAPP_DIR = (
        str(pathlib.Path(__file__).parent.parent.parent.absolute()) + "/webapp/"
    )
    df = pd.read_csv(WEBAPP_DIR + "/datasets/titanic.csv")

    l = get_auto_generated_graphs(dataset=df, feature_variables=["sex", "age", "fare"])

    print(l)
    # df = pd.read_csv(WEBAPP_DIR+"/datasets/titanic.csv")
