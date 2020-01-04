from flask import render_template
from flask import request, jsonify
import plotly.express as px
import pandas as pd
import json
from flask import Flask
from jinja2 import Template


from vizAI.webapp import app
from vizAI.core.visualizers.plotly.makePlots import *
from vizAI.core.utils.dataFrameUtils import *


@app.route('/')
@app.route('/index')
def index():

	data = pd.read_csv("vizAI/webapp/datasets/titanic.csv")
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

	chart_type = request.form['chart_type']

	data = pd.read_csv("vizAI/webapp/datasets/titanic.csv")
	
	fig_data = get_plot(data,
							chart_type=chart_type,
							x=graph_x_axis,
							y=graph_y_axis,
							color=graph_color,
							facet_col=graph_facet,
							barmode="group")

	return jsonify({'plotData': fig_data})