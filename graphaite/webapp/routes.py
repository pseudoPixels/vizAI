import os
from flask import render_template
from flask import jsonify, flash, request, redirect
from werkzeug.utils import secure_filename
import plotly.express as px
import pandas as pd
import json
from flask import Flask
from jinja2 import Template
import uuid


from graphaite.webapp import app
from graphaite.core.visualizers.plotly.makePlots import *
from graphaite.core.utils.dataFrameUtils import *
from graphaite.core.visualizers.plotly.config import GRAPHS_DICT
from graphaite.core.graphControllers.graphGeneratorAI import get_auto_generated_graphs


@app.route('/')
@app.route('/index')
def index():
    data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")
    fig_data = ""  # get_bar_plot(data=data, x="sex", y="age")

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
    # data = data.sort_values(by = [graph_x_axis, graph_y_axis] )

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

    return jsonify({'plotData': fig_data,
                    'chart_params': chart_params})


@app.route('/getDataFrame', methods=['POST'])
def getDataFrame():
    data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")
    table = data.to_json(orient='split', index=False)

    return table


@app.route('/createProject')
def createProject():
    return render_template('create_project.html')


ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_dataset_and_create_project/', methods=['POST'])
def upload_dataset_and_create_project():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/autoviz')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

@app.route('/autoviz')
def autoviz():
    ## The list will be available from project info (CouchDB)
    feature_variables = ['age','pclass','sibsp','parch','fare','sex']

    return render_template('autoviz.html',
    feature_variables=feature_variables)


@app.route('/getAutoViz', methods=['POST'])
def getAutoViz():
    graph_x_axis = "age"
    graph_y_axis = ""
    graph_color = "survived"
    graph_facet = ""
    graph_size = ""
    graph_names = ""

    chart_type = "histogram"
    chart_template = "presentation"

    data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")

    feature_variables = ['age','pclass','sibsp','parch','fare','sex']


    plots = get_auto_generated_graphs(dataset=data, feature_variables=feature_variables, target_variable="survived")


    return jsonify({'plots': plots})
