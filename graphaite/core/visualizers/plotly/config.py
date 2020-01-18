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


#
# scatter([data_frame, x, y, color, symbol, …])
#
# In a scatter plot, each row of data_frame is represented by a symbol
#
# scatter_3d([data_frame, x, y, z, color, …])
#
# In a 3D scatter plot, each row of data_frame is represented by a
#
# scatter_polar([data_frame, r, theta, color, …])
#
# In a polar scatter plot, each row of data_frame is represented by a
#
# scatter_ternary([data_frame, a, b, c, …])
#
# In a ternary scatter plot, each row of data_frame is represented by a
#
# scatter_mapbox([data_frame, lat, lon, …])
#
# In a Mapbox scatter plot, each row of data_frame is represented by a
#
# scatter_geo([data_frame, lat, lon, …])
#
# In a geographic scatter plot, each row of data_frame is represented
#
# line([data_frame, x, y, line_group, color, …])
#
# In a 2D line plot, each row of data_frame is represented as vertex of
#
# line_3d([data_frame, x, y, z, color, …])
#
# In a 3D line plot, each row of data_frame is represented as vertex of
#
# line_polar([data_frame, r, theta, color, …])
#
# In a polar line plot, each row of data_frame is represented as vertex
#
# line_ternary([data_frame, a, b, c, color, …])
#
# In a ternary line plot, each row of data_frame is represented as
#
# line_mapbox([data_frame, lat, lon, color, …])
#
# In a Mapbox line plot, each row of data_frame is represented as
#
# line_geo([data_frame, lat, lon, locations, …])
#
# In a geographic line plot, each row of data_frame is represented as
#
# area([data_frame, x, y, line_group, color, …])
#
# In a stacked area plot, each row of data_frame is represented as
#
# bar([data_frame, x, y, color, facet_row, …])
#
# In a bar plot, each row of data_frame is represented as a rectangular
#
# bar_polar([data_frame, r, theta, color, …])
#
# In a polar bar plot, each row of data_frame is represented as a wedge
#
# violin([data_frame, x, y, color, facet_row, …])
#
# In a violin plot, rows of data_frame are grouped together into a
#
# box([data_frame, x, y, color, facet_row, …])
#
# In a box plot, rows of data_frame are grouped together into a
#
# strip([data_frame, x, y, color, facet_row, …])
#
# In a strip plot each row of data_frame is represented as a jittered
#
# histogram([data_frame, x, y, color, …])
#
# In a histogram, rows of data_frame are grouped together into a
#
# pie([data_frame, names, values, color, …])
#
# In a pie plot, each row of data_frame is represented as a sector of a
#
# treemap([data_frame, names, values, …])
#
# A treemap plot represents hierarchial data as nested rectangular
#
# sunburst([data_frame, names, values, …])
#
# A sunburst plot represents hierarchial data as sectors laid out over
#
# funnel([data_frame, x, y, color, facet_row, …])
#
# In a funnel plot, each row of data_frame is represented as a
#
# funnel_area([data_frame, names, values, …])
#
# In a funnel area plot, each row of data_frame is represented as a
#
# scatter_matrix([data_frame, dimensions, …])
#
# In a scatter plot matrix (or SPLOM), each row of data_frame is
#
# parallel_coordinates([data_frame, …])
#
# In a parallel coordinates plot, each row of data_frame is represented
#
# parallel_categories([data_frame, …])
#
# In a parallel categories (or parallel sets) plot, each row of
#
# choropleth([data_frame, lat, lon, …])
#
# In a choropleth map, each row of data_frame is represented by a
#
# choropleth_mapbox([data_frame, geojson, …])
#
# In a Mapbox choropleth map, each row of data_frame is represented by a
#
# density_contour([data_frame, x, y, z, …])
#
# In a density contour plot, rows of data_frame are grouped together
#
# density_heatmap([data_frame, x, y, z, …])
#
# In a density heatmap, rows of data_frame are grouped together into
#
# density_mapbox([data_frame, lat, lon, z, …])
#
# In a Mapbox density map, each row of data_frame contributes to the intensity of
#
# imshow(img[, zmin, zmax, origin, …])
#
# Display an image, i.e.