from flask import Flask
import pathlib


app = Flask(__name__)

# app.secret_key = "secret key"
app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["UPLOAD_FOLDER"] = (
    str(pathlib.Path(__file__).parent.absolute()) + "/datasets/"
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

from graphaite.webapp import routes
