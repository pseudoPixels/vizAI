from flask import render_template
from flask import request, jsonify
import plotly.express as px
import pandas as pd
import json
from flask import Flask
from jinja2 import Template


from graphaite.webapp import app
from graphaite.core.visualizers.plotly.makePlots import *
from graphaite.core.utils.dataFrameUtils import *
from graphaite.core.visualizers.plotly.config import GRAPHS_DICT

@app.route('/')
@app.route('/index')
def index():

	data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")
	fig_data = ""#get_bar_plot(data=data, x="sex", y="age")

	all_features = get_all_features(data=data)
	categorical_features = get_categorical_features(data=data)
	neumeric_features = get_numeric_features(data=data)

	return render_template('index.html',
						   pData=fig_data,
						   all_features=all_features,
						   categorical_features=categorical_features,
						   neumeric_features=neumeric_features)



@app.route('/getPlot', methods=['POST'])
def getPlot():

	graph_x_axis = request.form['graph_x_axis']
	graph_y_axis = request.form['graph_y_axis']
	graph_color = request.form['graph_color']
	graph_facet = request.form['graph_facet']
	graph_size = request.form['graph_size']
	graph_names = request.form['graph_names']

	chart_type = request.form['chart_type']
	chart_template = request.form['chart_template']

	data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")
	
	fig_data = get_plot(data,
						chart_type,
						x=graph_x_axis,
						y=graph_y_axis,
						color=graph_color,
						facet_col=graph_facet,
						size=graph_size,
						names=graph_names,
						barmode="group",
						template=chart_template)

	chart_params = GRAPHS_DICT[chart_type].get_graph_param_keys()

	return jsonify({'plotData' : fig_data,
					'chart_params' : chart_params})




@app.route('/getDataFrame', methods=['POST'])
def getDataFrame():

	data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")
	table = data.to_json(orient='split', index=False)

	return table

