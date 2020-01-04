import plotly.express as px
import pandas as pd

from vizAI.core.visualizers.plotly.config import *




def get_plot(data, **kwargs):

    graphObject = GRAPHS_DICT[kwargs["chart_type"]]
    # print(graphObject.get_graph_object())

    # fig = px.scatter(data, x=graph_x_axis, y=graph_y_axis, size=graph_size, color=graph_color, facet_col=graph_facet)
    graph_params = {k: v for k, v in kwargs.items() if v is not None and v.strip(' \t\n\r') is not "" and k in graphObject.get_graph_param_keys()}

    # print("="*20)
    # print(graph_params)
    # print("="*20)

    # print(graph_params)

    plotly_go = graphObject.get_graph_object()
    # kwargs = {"x": graph_x_axis}
    fig = plotly_go(data, **graph_params)#, color=graph_color, facet_col=graph_facet)

    fig.update_layout({
        "plot_bgcolor": "rgba(.9, .9, .9, .1)",
        "paper_bgcolor": "rgba(.9, .9, .9, .1)"
    })

    return fig.to_json()

if __name__ == '__main__':
    data = pd.read_csv("../../../webapp/datasets/tips.csv")
    figData = get_plot(data, chart_type="Histogram", x="total_bill",  color="sex", size="tips")
    # print(figData)


