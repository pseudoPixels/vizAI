from abc import ABC, abstractmethod


class GraphObject(ABC):
    def __init__(self):
        self.PARAMS = {}


    @abstractmethod
    def get_graph_object(self):
        pass

    def get_graph_param_keys(self):
        return list(self.PARAMS.keys())


