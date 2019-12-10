from flask import Flask

app = Flask(__name__)

from vizAI.webapp import routes