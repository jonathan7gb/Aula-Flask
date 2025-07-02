from app import app
from flask import render_template

@app.route('/')
def homepage():
    nome = "Jonathan"
    idade = 17
    interesses = ["Python", "Flask", "Desenvolvimento Web"]
    
    dicionario = {
        'nome': nome,
        'idade': idade,
        'interesses': interesses
    }
    return render_template('index.html', dicionario=dicionario)

@app.route('/sobre/')
def sobre():
    return render_template('sobre.html')

@app.route('/contato/')
def novaPAgina():
    return 'Outra views'
    