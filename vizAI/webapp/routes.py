from flask import render_template
from flask import request, jsonify
from vizAI.webapp import app


import json

from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.sampledata.iris import flowers
from bokeh.embed import components


from flask import Flask
from jinja2 import Template

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]

def make_plot(x, y):
	p = figure(title = "Iris Morphology", sizing_mode="fixed", plot_width=400, plot_height=400)
	p.xaxis.axis_label = x
	p.yaxis.axis_label = y
	p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
	return p



@app.route('/')
@app.route('/index')
def index():
	# create a Figure object
	p = figure(plot_width=1700, plot_height=850)

	# add a Circle renderer to this figure
	p.circle([1, 2.5, 3, 2], [2, 3, 1, 1.5], radius=0.3, alpha=0.5)

	scripts, div = components(p)
	# print(scripts)
	return render_template('index.html', script=scripts, div=div)