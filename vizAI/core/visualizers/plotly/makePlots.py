import plotly.express as px

def get_bar_plot(data, x, y, color=None):
    if color is None:
        fig = px.bar(data, x=x, y=y)
    else:
        fig = px.bar(data, x=x, y=y, color=color, barmode='group')


    fig.update_layout({
        "plot_bgcolor": "rgba(.9, .9, .9, .1)",
        "paper_bgcolor": "rgba(.9, .9, .9, .1)"
    })

    return fig.to_json()