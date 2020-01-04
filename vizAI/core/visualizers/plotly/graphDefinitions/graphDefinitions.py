import plotly.express as px
from abc import ABC, abstractmethod


class GraphObject(ABC):
    def __init__(self):
        self.PARAMS = {}


    @abstractmethod
    def get_graph_object(self):
        pass

    def get_graph_param_keys(self):
        return list(self.PARAMS.keys())



class Scatter(GraphObject):
    def __init__(self):
        super().__init__()
        self.PARAMS = {
            "x" : {
                "accepts_feature_column" : "single"
            },
            "y" : {
                "accepts_feature_column" : "single"
            },
            "color" : {
                "accepts_feature_column" : "single"
            },
            "symbol" : {
                "accepts_feature_column" : "single"
            },
            "size" : {
                "accepts_feature_column" : "single"
            },
            "hover_name" : {
                "accepts_feature_column" : "single"
            },
            "hover_data" : {
                "accepts_feature_column" : "multiple"
            },
            "custom_data" : {
                "accepts_feature_column" : "multiple"
            },
            "text" : {
                "accepts_feature_column" : "single"
            },
            "facet_row" : {
                "accepts_feature_column" : "single"
            },
            "facet_col" : {
                "accepts_feature_column" : "single"
            },
            # "facet_col_wrap" = 0,
            "error_x" : {
                "accepts_feature_column" : "single"
            },
            "error_x_minus" : {
                "accepts_feature_column" : "single"
            },
            "error_y" : {
                "accepts_feature_column" : "single"
            },
            "error_y_minus" : {
                "accepts_feature_column" : "single"
            },
            "animation_frame" : {
                "accepts_feature_column" : "single"
            },
            "animation_group" : {
                "accepts_feature_column" : "single"
            },
            # category_orders = {},
            # labels = {},
            # color_discrete_sequence = None,
            # color_discrete_map = {},
            # color_continuous_scale = None,
            # range_color = None,
            # color_continuous_midpoint = None,
            # symbol_sequence = None,
            # symbol_map = {},
            # opacity = None,
            # size_max = None,
            "marginal_x" : {
                "accepts_feature_column" : "no",
                "datatype": "str",
                "select_from": ['None', 'rug', 'box', 'violin', 'histogram']
            },
            "marginal_y" : {
                "accepts_feature_column" : "no",
                "datatype": "str",
                "select_from": ['None', 'rug', 'box', 'violin', 'histogram']
            },
            "trendline" : {
                "accepts_feature_column" : "no",
                "datatype": "str",
                "select_from": ['None', 'ols', 'lowess']
            },
            # trendline_color_override = None,
            # log_x = False,
            # log_y = False,
            # range_x = None,
            # range_y = None,
            # render_mode = "auto",
            # title = None,
            # template = None,
            # width = None,
            # height = None
        }



    def get_graph_object(self):
        return px.scatter




class Histogram(GraphObject):
    def __init__(self):
        super().__init__()
        self.PARAMS = {
            "x" : {
                "accepts_feature_column" : "single"
            },
            "y" : {
                "accepts_feature_column" : "single"
            },
            "color" : {
                "accepts_feature_column" : "single"
            },
            "hover_name" : {
                "accepts_feature_column" : "single"
            },
            "hover_data" : {
                "accepts_feature_column" : "multiple"
            },
            "text" : {
                "accepts_feature_column" : "single"
            },
            "facet_row" : {
                "accepts_feature_column" : "single"
            },
            "facet_col" : {
                "accepts_feature_column" : "single"
            },
            # "facet_col_wrap" = 0,
            "animation_frame" : {
                "accepts_feature_column" : "single"
            },
            "animation_group" : {
                "accepts_feature_column" : "single"
            },
            # category_orders = {},
            # labels = {},
            # color_discrete_sequence = None,
            # color_discrete_map = {},
            # color_continuous_scale = None,
            # range_color = None,
            # color_continuous_midpoint = None,
            # symbol_sequence = None,
            # symbol_map = {},
            # opacity = None,
            # size_max = None,
            "marginal" : {
                "accepts_feature_column" : "no",
                "datatype": "str",
                "select_from": ['None', 'rug', 'box', 'violin', 'histogram']
            },
            "orientation" : {
                "accepts_feature_column" : "no",
                "datatype": "str",
                "select_from": ['v', 'h']
            },
            "barmode": {
                "accepts_feature_column": "no",
                "datatype": "str",
                "select_from": ['group', 'overlay', 'relative']
            },
            # trendline_color_override = None,
            # log_x = False,
            # log_y = False,
            # range_x = None,
            # range_y = None,
            # render_mode = "auto",
            # title = None,
            # template = None,
            # width = None,
            # height = None
        }



    def get_graph_object(self):
        return px.histogram


