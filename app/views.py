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
        return redirect(url_for('homepage'))
    return render_template('contato.html', context=context, form=form)

@app.route('/contato/lista/')
def contatoLista():
    if request.method == 'POST':
        pesquisa = request.args.get('pesquisa', '')
    dados = contato.query.order_by('nome')
    
    if pesquisa != '':
        dados = dados.filter(nome=pesquisa)
    
    context = {'dados' : dados.all()}
    return render_template('contato_lista.html', context=context)