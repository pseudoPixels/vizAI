from flask import Flask

app = Flask(__name__)

from graphaite.webapp import routes