from flaskext.couchdb import Document, TextField, FloatField, DictField, Mapping,ListField, IntegerField


class GraphaiteGraph(Document):
    doc_type = 'graphaite_graph'

    graph_id = TextField()
    figure_data = TextField()
    x_axis = TextField()