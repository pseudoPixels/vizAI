import os
from flask import render_template, session
from flask import jsonify, flash, request, redirect
from werkzeug.utils import secure_filename
import plotly.express as px
import pandas as pd
import json
from flask import Flask, g
from jinja2 import Template
import uuid


from graphaite.webapp import app
from graphaite.core.visualizers.plotly.makePlots import *
from graphaite.core.utils.dataFrameUtils import *
from graphaite.core.visualizers.plotly.config import GRAPHS_DICT
from graphaite.core.graphControllers.graphGeneratorAI import get_auto_generated_graphs
from graphaite.core.utils.fileUtils import delete_files_of_directory

## Models
from graphaite.core.models.graphaiteGraph import GraphaiteGraphModel
from graphaite.core.models.GraphaiteProject import GraphaiteProjectModel

from flaskext.couchdb import CouchDBManager
from couchdb.design import ViewDefinition

app.config.update(
    COUCHDB_SERVER="http://admin:123@localhost:5984", COUCHDB_DATABASE="graphaitedb"
)

views_by_graphaite_project_owner = ViewDefinition(
    "graphaite_views",
    "by_graphaite_project_owner",
    """
    function (doc) {
         if (doc.doc_type == 'graphaite_project') {
            emit(doc.porject_owner_id, doc._id)
        };   
    }
    """,
)


manager = CouchDBManager()
manager.setup(app)
manager.add_viewdef([views_by_graphaite_project_owner])
manager.sync(app)


@app.route("/")
@app.route("/index")
def index():
    data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")
    fig_data = ""  # get_bar_plot(data=data, x="sex", y="age")

    all_features = get_all_features(data=data)
    categorical_features = get_categorical_features(data=data)
    neumeric_features = get_numeric_features(data=data)

    return render_template(
        "index.html",
        pData=fig_data,
        all_features=all_features,
        categorical_features=categorical_features,
        neumeric_features=neumeric_features,
    )


@app.route("/getPlot", methods=["POST"])
def getPlot():
    graph_x_axis = request.form["graph_x_axis"]
    graph_y_axis = request.form["graph_y_axis"]
    graph_color = request.form["graph_color"]
    graph_facet = request.form["graph_facet"]
    graph_size = request.form["graph_size"]
    graph_names = request.form["graph_names"]

    chart_type = request.form["chart_type"]
    chart_template = request.form["chart_template"]

    data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")
    # data = data.sort_values(by = [graph_x_axis, graph_y_axis] )

    fig_data = get_plot(
        data,
        chart_type,
        x=graph_x_axis,
        y=graph_y_axis,
        color=graph_color,
        facet_col=graph_facet,
        size=graph_size,
        names=graph_names,
        barmode="group",
        template=chart_template,
    )

    chart_params = GRAPHS_DICT[chart_type].get_graph_param_keys()

    return jsonify({"plotData": fig_data, "chart_params": chart_params})


@app.route("/getDataFrame/<project_id>", methods=["POST"])
def getDataFrame(project_id):
    aProjectDoc = GraphaiteProjectModel.load(project_id)

    isDataAvailable = True
    try:
        df = pd.read_csv(aProjectDoc.dataset_path)
    except Exception:
        df = pd.DataFrame()
        isDataAvailable = False


    
    # table = data.to_json(orient="split", index=False)

    return jsonify(
        my_table=json.loads(df.to_json(orient="split"))["data"],
        columns=[
            {"title": str(col)}
            for col in json.loads(df.to_json(orient="split"))["columns"]
        ],
        isDataAvailable = isDataAvailable
    )


@app.route("/home")
def createProject():

    userProjects = []
    for aProject in views_by_graphaite_project_owner(g.couch):
        if aProject.key == "golam@example.com":
            aProjectDoc = GraphaiteProjectModel.load(aProject.value)
            userProjects.append({'project_doc_id':aProject.value, 'project_title':aProjectDoc.project_title})

    # print(userProjects)
    return render_template("home.html", userProjects=userProjects)


ALLOWED_EXTENSIONS = set(["csv"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/create_new_project/", methods=["POST"])
def create_new_project():
    projectName = request.form["project_name"]
    projectOwner = "golam@example.com"
    projectID = str(uuid.uuid4())

    newProject = GraphaiteProjectModel(
        project_id=projectID, project_title=projectName, porject_owner_id=projectOwner
    )

    newProject.store()

    return redirect("/manage_datasets/"+projectID)


@app.route("/autoviz")
def autoviz():
    ## The list will be available from project info (CouchDB)
    feature_variables = ["age", "pclass", "sibsp", "parch", "fare", "sex", "survived"]

    return render_template("autoviz.html", feature_variables=feature_variables)


@app.route("/getAutoViz", methods=["POST"])
def getAutoViz():

    data = pd.read_csv("graphaite/webapp/datasets/titanic.csv")
    # feature_variables = ["age", "pclass", "sibsp", "parch", "fare", "sex"]
    target_variable =  request.form.get("target_variable") #"survived"

    feature_variables = request.form.getlist("selected_features")

    # print("="*20)
    # print(target_variable)
    # print("="*20)

    ## get auto generated plots
    plots = get_auto_generated_graphs(
        dataset=data,
        feature_variables=feature_variables,
        target_variable=target_variable,
    )

    ## add the graphs to database
    for aPlotID in plots:
        plotModel = GraphaiteGraphModel(
            graph_id=aPlotID,
            graph_title=" | ".join(plots[aPlotID]["feature_tags"]),
            figure_data=plots[aPlotID]["figure_data"],
            insights=["No insights added yet!"],
            **plots[aPlotID]["graph_settings"]
        )
        plotModel.store()

    return jsonify({"plots": plots})


@app.route("/manage_datasets/<project_id>")
def manage_datasets(project_id):
    # print("="*10, session.get('PROJECT_ID'))
    # print(project_id)
    return render_template("manage_datasets.html", project_id=project_id)


@app.route("/python-flask-files-upload/<project_id>", methods=["POST"])
def upload_file(project_id):
    # check if the post request has the file part
    if "files[]" not in request.files:
        resp = jsonify({"message": "No file part in the request"})
        resp.status_code = 400
        return resp

    files = request.files.getlist("files[]")

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ## load the project info from database
            aProjectDoc = GraphaiteProjectModel.load(project_id)

            ## create directory for this project if not exists already
            thisUserDir = app.config["UPLOAD_FOLDER"] + "/" + aProjectDoc.porject_owner_id
            if not os.path.exists(thisUserDir):
                os.makedirs(thisUserDir)
            thisProjectDir = thisUserDir + "/" + aProjectDoc.project_id
            if not os.path.exists(thisProjectDir):
                os.makedirs(thisProjectDir)
            ## empty the project directory, as there should be one dataset per
            ## project. Deletion is required so user does not takes extra file space per project 
            delete_files_of_directory(target_dir=thisProjectDir)

            ## finally, save the new dataset to the target path
            datasetTargetPath = os.path.join(thisProjectDir+"/", filename)
            file.save(datasetTargetPath)
            success = True

            ## update the dataset path in the database
            aProjectDoc.dataset_path = str(datasetTargetPath)
            aProjectDoc.store()
        else:
            errors[file.filename] = "File type is not allowed"

    if success and errors:
        errors["message"] = "File(s) successfully uploaded"
        resp = jsonify(errors)
        resp.status_code = 206
        return resp
    if success:
        resp = jsonify({"message": "Files successfully uploaded"})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp

