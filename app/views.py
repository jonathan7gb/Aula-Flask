from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import contatoForm, userForm
from app.models import Contato, User
from app import bcrypt
from flask_login import login_user, logout_user, current_user

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
def contato_cadastro():
    form = contatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('contato.html', context=context, form=form)

@app.route('/contato/lista/')
def contatoLista():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Contato.query.order_by('nome')
    
    if pesquisa != '':
        dados = dados.filter(Contato.nome.ilike(f'%{pesquisa}%'))
    
    context = {'dados' : dados.all()}
    return render_template('contato_lista.html', context=context)

@app.route('/contato/<int:id>')
def contatoDetalhes(id):
    obj = Contato.query.get(id)
    return render_template('contato_detalhes.html', obj = obj)
    
@app.route('/cadastrouser/', methods=['GET', 'POST'])
def cadastro_usuario():
    form = userForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro_user.html', form=form)