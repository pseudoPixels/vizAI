import plotly.express as px
from graphaite.core.visualizers.plotly.graphDefinitions import graphDefinitions as gd


GRAPHS_DICT = {
    "histogram" : gd.Histogram(),
    "scatter" : gd.Scatter(),
    "line" : gd.Line(),
    "area" : gd.Area(),
    "violin" : gd.Violin(),
    "box" : gd.Box(),
    "strip" : gd.Strip(),
    "funnel" : gd.Funnel(),
    "pie" : gd.Pie()
}

