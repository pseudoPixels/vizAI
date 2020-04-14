from flaskext.couchdb import (
    Document,
    TextField,
    FloatField,
    DictField,
    Mapping,
    ListField,
    IntegerField,
)


class GraphaiteGraphModel(Document):
    doc_type = "graphaite_graph"

    graph_id = TextField()  ## unique graph id
    graph_title = TextField()  ## title of the graph
    figure_data = TextField()  ## figure data, like json for plotly
    insights = ListField(TextField())  ## visualization insights
    # last_modified_date = DateTimeField(default=datetime.datetime.now)

    ### Graph Atributes
    chart_type = TextField()
    x = TextField(default="")
    y = TextField(default="")
    color = TextField(default="")
    barmode = TextField(default="")
    template = TextField(default="")


if __name__ == "__main__":
    pass
