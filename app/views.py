from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import contatoForm, userForm, LoginForm, PostForm, PostComentarioForm
from app.models import Contato, User, Post, PostComentarios
from app import bcrypt
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def homepage():
    nome = "Jonathan"
    idade = 17
    interesses = ["Python", "Flask", "Desenvolvimento Web"]
    form =LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('login_user.html', form=form)

@app.route('/contato/', methods=['GET', 'POST'])
@login_required
def contato_cadastro():
    form = contatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('contato.html', context=context, form=form)

@app.route('/contato/lista/')
@login_required
def contatoLista():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Contato.query.order_by('nome')
    
    if pesquisa != '':
        dados = dados.filter(Contato.nome.ilike(f'%{pesquisa}%'))
    
    context = {'dados' : dados.all()}
    return render_template('contato_lista.html', context=context)

@app.route('/contato/<int:id>')
@login_required
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

@app.route('/sair/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/post/novo', methods=['GET', 'POST'])
@login_required
def PostNovo():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('homepage'))
    return render_template('post_novo.html', form=form)

@app.route('/post/lista')
@login_required
def PostLista():
    posts = Post.query.all()
    print(current_user.posts)
    return render_template('post_lista.html', posts=posts)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def PostComentarios(id):
    post = Post.query.get(id)
    form = PostComentarioForm()
    if form.validate_on_submit():
        form.save(current_user.id, id)
        return redirect(url_for('PostComentarios', id=id))
    return render_template('post.html', post=post, form=form)

@app.route('/contato/excluir/<int:id>', methods=['POST'])
@login_required
def excluirContato(id):
    obj = Contato.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('contatoLista')) 