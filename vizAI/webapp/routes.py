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

	data = pd.read_csv("vizAI/webapp/datasets/tips.csv")
	fig_data = get_bar_plot(data=data, x="sex", y="total_bill")

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
	color = request.form['color']

	data = pd.read_csv("vizAI/webapp/datasets/tips.csv")
	fig_data = get_bar_plot(data=data, x="sex", y="total_bill", color=color)

	return jsonify({'plotData': fig_data})