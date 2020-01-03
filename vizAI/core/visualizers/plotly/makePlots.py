import plotly.express as px
import pandas as pd

from vizAI.core.visualizers.plotly.config import *




def get_bar_plot(data, **kwargs):

    # fig = px.scatter(data, x=graph_x_axis, y=graph_y_axis, size=graph_size, color=graph_color, facet_col=graph_facet)
    graph_params = {k: v for k, v in kwargs.items() if v is not None and v.strip(' \t\n\r') is not ""}

    # print("="*20)
    # print(graph_params)
    # print("="*20)


    # kwargs = {"x": graph_x_axis}
    fig = GRAPHS_DICT["histogram"]["GO"](data, **graph_params)#, color=graph_color, facet_col=graph_facet)

    fig.update_layout({
        "plot_bgcolor": "rgba(.9, .9, .9, .1)",
        "paper_bgcolor": "rgba(.9, .9, .9, .1)"
    })

    return fig.to_json()

if __name__ == '__main__':
    data = pd.read_csv("../../../webapp/datasets/tips.csv")
    figData = get_bar_plot(data, x="total_bill",  color="sex")
    print(figData)


