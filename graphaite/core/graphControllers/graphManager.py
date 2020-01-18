from graphaite.core.graphControllers.graphObject import GraphObject

class GraphManager():
    def __init__(self):
        pass


    def get_all_graph_params_set(self, graphObject_dict):
        """
        Returns a list of all graph params. That is a superset of graph params for all the graph object passed.

        :param graphObject_dict: (dict) A dict of graph object. For example, graphObject_dict: { "histogram" : gd.Histogram(), "scatter" : gd.Scatter() }
        :return: (list) List of all graph params (i.e., superset of params)
        """

        allParams = set()
        for aKey in  graphObject_dict:
            aGraphObject = graphObject_dict[aKey]
            if isinstance(aGraphObject , GraphObject):
                allParams.update(aGraphObject.get_graph_param_keys())

        return list(allParams)


if __name__ == '__main__':
    from graphaite.core.visualizers.plotly.config import GRAPHS_DICT
    gm = GraphManager()

    all_params = gm.get_all_graph_params_set(graphObject_dict=GRAPHS_DICT)
    print(all_params)

