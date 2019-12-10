from flask import render_template
from flask import request, jsonify
from vizAI.webapp import app

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')