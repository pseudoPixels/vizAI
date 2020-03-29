import os
from flask import render_template
from flask import jsonify, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import random
import time
import plotly.express as px
import pandas as pd
import json
from flask import Flask
from jinja2 import Template

from graphaite.webapp import app
from graphaite.core.visualizers.plotly.makePlots import *
from graphaite.core.utils.dataFrameUtils import *
from graphaite.core.visualizers.plotly.config import GRAPHS_DICT

### For Celery
from celery import Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

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
    return render_template('autoviz.html')


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

    fig_data = get_plot(data,
                        chart_type,
                        x=graph_x_axis,
                        y=graph_y_axis,
                        color=graph_color,
                        facet_col=graph_facet,
                        size=graph_size,
                        names=graph_names,
                        barmode="group",
                        template=chart_template,
                        height=430)

    chart_params = GRAPHS_DICT[chart_type].get_graph_param_keys()

    return jsonify({'plotData': fig_data,
                    'chart_params': chart_params})







@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


# pip install celery==4.4.1
