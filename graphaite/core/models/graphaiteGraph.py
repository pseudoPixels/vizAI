from flaskext.couchdb import (
    Document,
    TextField,
    FloatField,
    DictField,
    Mapping,
    ListField,
    IntegerField,
    BooleanField
)


class GraphaiteGraphModel(Document):
    doc_type = "graphaite_graph"

    graph_id = TextField()  ## unique graph id
    graph_title = TextField()  ## title of the graph
    figure_data = TextField()  ## figure data, like json for plotly
    insights = ListField(TextField())  ## visualization insights
    feature_tags = ListField(
        TextField()
    )  ## feature tags used for displaying charts in corresponding categories (mainly, x, y axes are the tags)
    # last_modified_date = DateTimeField(default=datetime.datetime.now)
    isFavourite = BooleanField(default=False)
    isAutoViz = BooleanField(default=True) # is automatically or user created graph

    ### Graph Atributes
    chart_type = TextField()
    x = TextField(default="")
    y = TextField(default="")
    color = TextField(default="")
    barmode = TextField(default="")
    template = TextField(default="")


if __name__ == "__main__":
    pass
