from app import app
from flask import render_template, url_for, request

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
def contato():
    context = {}
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa')
        context.update({'pesquisa':pesquisa})
    if request.method == 'POST':
        pesquisa = request.form('pesquisa')
        print('post', pesquisa)
        context.update({'pesquisa':pesquisa})
    return render_template('contato.html', context=context)