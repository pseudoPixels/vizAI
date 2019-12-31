import plotly.express as px

def get_bar_plot(data, graph_x_axis=None, graph_y_axis=None, graph_color=None, graph_facet=None, graph_size=None):

    fig = px.scatter(data, x=graph_x_axis, y=graph_y_axis, size=graph_size, color=graph_color, facet_col=graph_facet)


    fig.update_layout({
        "plot_bgcolor": "rgba(.9, .9, .9, .1)",
        "paper_bgcolor": "rgba(.9, .9, .9, .1)"
    })

    return fig.to_json()