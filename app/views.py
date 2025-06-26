from app import app
from flask import render_template

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/sobre/')
def sobre():
    return render_template('sobre.html')