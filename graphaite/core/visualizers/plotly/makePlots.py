import plotly.express as px
import pandas as pd

from graphaite.core.visualizers.plotly.config import GRAPHS_DICT




def get_plot(data, chart_type, **kwargs):
    """
    Draws and Returns the plot as plotly json based on the data, chart type and param settings of the specific chart type.

    :param data: (Pandas DataFrame) The dataset to draw plot on.
    :param chart_type: (str) The chart type to draw (for example, 'histogram', 'scatter'). Usually, the name should be same as plotly.
    :param kwargs: (dict) The kwargs param for the specific plotly chart type.
    :return: (str as json) the interactive plot as json string.
    """

    ## get the graph object from graphaite
    graphObject = GRAPHS_DICT[chart_type]

    ## filter out those kwargs which are empty/none and not available in the settings of the specific plotly chart type.
    graph_params = {k: v for k, v in kwargs.items() if v is not None and v.strip(' \t\n\r') is not "" and k in graphObject.get_graph_param_keys()}

    ## get plotly graph object from graphaite
    plotly_go = graphObject.get_graph_object()

    ## draw the plot with data and kwargs
    fig = plotly_go(data, height=750, **graph_params)

    ## required layout changes.
    # fig.update_layout({
    #     "plot_bgcolor": "rgba(.9, .9, .9, .1)",
    #     "paper_bgcolor": "rgba(.9, .9, .9, .1)"
    # })

    return fig.to_json()

if __name__ == '__main__':
    data = pd.read_csv("../../../webapp/datasets/tips.csv")
    figData = get_plot(data, chart_type="Histogram", x="total_bill",  color="sex", size="tips")
    print(figData)


