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
    x = TextField()
    y = TextField()
    color = TextField()


if __name__ == "__main__":
    pass
