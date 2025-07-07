from app import app, db
from flask import render_template, url_for, request
from app.forms import contatoForm

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


@app.route('/contato/', methods=['GET', 'POST'])
def contato():
    form = contatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        
    return render_template('contato.html', context=context, form=form)