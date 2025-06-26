from app import app
from flask import render_template

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/sobre/')
def about():
    return render_template('sobre.html')