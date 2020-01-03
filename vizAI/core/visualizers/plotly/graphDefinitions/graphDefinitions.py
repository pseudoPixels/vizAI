import plotly.express as px
from abc import ABC, abstractmethod


class GraphObject(ABC):
    def __init__(self):
        self.PARAMS = {
                "data_frame":{"Default": None},
                "x":{"Default": None}
        }
        self.add_or_update_graph_specific_params()

    @abstractmethod
    def get_graph_object(self):
        pass


    @abstractmethod
    def add_or_update_graph_specific_params(self):
        pass


    def get_params(self):
        return self.PARAMS


class Scatter(GraphObject):
    def __init__(self):
        super().__init__()


    def get_graph_object(self):
        return px.scatter

    def add_or_update_graph_specific_params(self):
        self.PARAMS["yetAnother_param"] = {
            "Default": None,
            "DataType": str,
            "acceptsFeatureColumn": "single",
            "featureColumnType": "Numeric"
        }


scr = Scatter()
print(scr.get_params())

