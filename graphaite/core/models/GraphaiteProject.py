from flaskext.couchdb import (
    Document,
    TextField,
    FloatField,
    DictField,
    Mapping,
    ListField,
    IntegerField,
)


class GraphaiteProjectModel(Document):
    doc_type = "graphaite_project"

    project_id = TextField()  ## unique graph id
    project_title = TextField()  ## title of the graph
    porject_owner_id = TextField()  ## figure data, like json for plotly
    # last_modified_date = DateTimeField(default=datetime.datetime.now)

    ### Graph Atributes
    dataset_path = TextField()
    selected_feature_variables = ListField(TextField())
    selected_target_variable = TextField(default="")

    graphaite_graph_ids = ListField(TextField())

    favourites_graphaite_graph_ids = ListField(TextField()) ##graph ids which are added to favourites


if __name__ == "__main__":
    pass
