import os
from flask import render_template, session, url_for
from flask import jsonify, flash, request, redirect
from werkzeug.utils import secure_filename
import plotly.express as px
import pandas as pd
import json
from flask import Flask, g
from jinja2 import Template
import uuid
from flask_bcrypt import Bcrypt


from graphaite.webapp import app
from graphaite.core.visualizers.plotly.makePlots import *
from graphaite.core.utils.dataFrameUtils import *
from graphaite.core.visualizers.plotly.config import GRAPHS_DICT
from graphaite.core.graphControllers.graphGeneratorAI import get_auto_generated_graphs
from graphaite.core.utils.fileUtils import delete_files_of_directory
from graphaite.core.utils.dataFrameUtils import get_all_features





## Models
from graphaite.core.models.graphaiteGraph import GraphaiteGraphModel
from graphaite.core.models.GraphaiteProject import GraphaiteProjectModel
from graphaite.core.models.graphaiteUser import GraphaiteUserModel

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

views_by_graphaite_graph = ViewDefinition(
    "graphaite_views",
    "by_graphaite_graph",
    """
    function (doc) {
         if (doc.doc_type == 'graphaite_graph') {
            emit(doc.graph_id, doc._id)
        };   
    }
    """,
)

views_by_graphaite_user = ViewDefinition(
    "graphaite_views",
    "by_graphaite_user",
    """
    function (doc) {
         if (doc.doc_type == 'graphaite_user') {
            emit(doc.email, doc.password)
        };   
    }
    """,
)


manager = CouchDBManager()
manager.setup(app)
manager.add_viewdef([views_by_graphaite_project_owner, views_by_graphaite_graph, views_by_graphaite_user])
manager.sync(app)

## password hashing
bcrypt = Bcrypt(app)



## Forms
# from graphaite.webapp.forms import RegistrationForm, LoginForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    # def validate_email(self, email):
    #     # row = 
    #     print("="*20)
    #     print(views_by_graphaite_user(g.couch))
    #     print("="*20)

    #     for aUser in views_by_graphaite_user(g.couch):
    #         if aUser.key == email:
    #             raise ValidationError("That email is taken. Please choose a different one.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")




# @app.route("/")
@app.route("/graph_editor/<project_id>/<graph_id>")
def graph_editor(project_id, graph_id):

    projectDoc = GraphaiteProjectModel.load(project_id)

    data = pd.read_csv(projectDoc.dataset_path)
    fig_data = ""  # get_bar_plot(data=data, x="sex", y="age")

    graphDoc = None
    for aGraph in views_by_graphaite_graph(g.couch):
        if aGraph.key == graph_id:
            graphDoc = GraphaiteGraphModel.load(aGraph.value)
            break

    if graphDoc is not None:
        fig_data = graphDoc.figure_data


    all_features = get_all_features(data=data)
    categorical_features = get_categorical_features(data=data)
    neumeric_features = get_numeric_features(data=data)

    graph_settings = {"graph_x":graphDoc.x, "graph_y":graphDoc.y, "graph_color":graphDoc.color}

    return render_template(
        "index.html",
        pData=fig_data,
        all_features=all_features,
        categorical_features=categorical_features,
        neumeric_features=neumeric_features,
        graph_settings=graph_settings,
        project_id=project_id,
        graph_id=graph_id
    )


@app.route("/getPlot/<project_id>", methods=["POST"])
def getPlot(project_id):
    projectDoc = GraphaiteProjectModel.load(project_id)

    graph_x_axis = request.form["graph_x"]
    graph_y_axis = request.form["graph_y"]
    graph_color = request.form["graph_color"]
    graph_facet = request.form["graph_facet"]
    graph_size = request.form["graph_size"]
    graph_names = request.form["graph_names"]

    chart_type = request.form["chart_type"]
    chart_template = request.form["chart_template"]

    data = pd.read_csv(projectDoc.dataset_path)
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


@app.route("/autoviz/<project_id>")
def autoviz(project_id):

    aProjectDoc = GraphaiteProjectModel.load(project_id)
    # graphsOfThisProject = aProjectDoc.graphaite_graph_ids

    df = pd.read_csv(aProjectDoc.dataset_path)
    ## The list will be available from project info (CouchDB)
    feature_variables = get_all_features(data=df) #["age", "pclass", "sibsp", "parch", "fare", "sex", "survived"]


    return render_template("autoviz.html", 
    feature_variables=feature_variables, 
    project_id=project_id)#, 
    #plots=plots)


@app.route("/getAutoViz/<project_id>", methods=["POST"])
def getAutoViz(project_id):
    ## getting user seelected target and feature varaibles 
    new_target_variable =  request.form.get("target_variable")
    new_feature_variables = request.form.getlist("selected_features")

    ## get existing target and featrue variables from db 
    aProjectDoc = GraphaiteProjectModel.load(project_id)
    prev_target_variable = aProjectDoc.selected_target_variable
    prev_feature_variables = aProjectDoc.selected_feature_variables


    plots = {}


    ## check if the previous an new targe and feature variables are exact same.
    ## if they are exact same, we just load of db and send instead of generating plots again.
    if (prev_target_variable == new_target_variable) and (sorted(prev_feature_variables) == sorted(new_feature_variables)):

        graphIDsOfThisProject = aProjectDoc.graphaite_graph_ids

        for aGraph in views_by_graphaite_graph(g.couch):
            if aGraph.key in graphIDsOfThisProject:
                aGraphDoc = GraphaiteGraphModel.load(aGraph.value)

                plots[aGraph.value] = {
                        "figure_data": str(aGraphDoc.figure_data),
                        "feature_tags": aGraphDoc.feature_tags,
                        "figure_title": aGraphDoc.graph_title,
                        "graph_id": aGraphDoc.graph_id
                }


    ## some settings (such as, target or feature variables) changed and need to regenerate auto plots 
    else:
            
        data = pd.read_csv(aProjectDoc.dataset_path)

        ## get auto generated plots
        plots = get_auto_generated_graphs(
            dataset=data,
            feature_variables=new_feature_variables,
            target_variable=new_target_variable,
        )

        aProjectDoc.graphaite_graph_ids = []
        ## add the graphs to database
        for aPlotID in plots:
            plotModel = GraphaiteGraphModel(
                graph_id=aPlotID,
                graph_title=" | ".join(plots[aPlotID]["feature_tags"]),
                figure_data=plots[aPlotID]["figure_data"],
                insights=["No insights added yet!"],
                feature_tags = plots[aPlotID]["feature_tags"],
                **plots[aPlotID]["graph_settings"]
            )

            plotModel.store()
           
            ## add the graphid to the corresponding project data model
            aProjectDoc.graphaite_graph_ids.append(aPlotID)
            aProjectDoc.store()

        ## since the target and feature variable changed, update and store them
        aProjectDoc.selected_target_variable = new_target_variable
        aProjectDoc.selected_feature_variables = new_feature_variables
        aProjectDoc.store()



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



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():

        for aUser in views_by_graphaite_user(g.couch):
            if aUser.key == form.email.data:
                    flash('That email is taken. Please choose a different one.', 'danger')
                    return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = GraphaiteUserModel(email = form.email.data, password=hashed_password)
        user.store()
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('createProject'))
    return render_template('register.html', title='Register', form=form)
