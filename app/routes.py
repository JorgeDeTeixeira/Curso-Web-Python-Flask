from flask import render_template, url_for, jsonify, redirect
from app import app
from app.forms import FilmeForm, UserForm, LoginForm
from app.models import Filme
from flask_login import login_required, login_user, logout_user


@app.route("/")
def homepage():
    context = {
        'usuario': 'Jorge',
        'idade': 20
    }
    return render_template('index.html', context=context)


@app.route('/api/dados')
def dados():
    dados = {'mensagem': "Dados do bacl-end"}
    return jsonify(dados)


@app.route('/calcular/<int:valor>')
def calcular(valor):
    context = {
        'valor': valor,
        'valorDobrado': valor * 2
    }
    return render_template('calcular.html', context=context)


@app.route('/filmes/novo', methods=['GET', 'POST'])
def adicionarFilme():
    form = FilmeForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('adicionarFilme.html', form=form)


@app.route('/filme/lista')
def listarFilmes():
    filmes = Filme.query.order_by(Filme.titulo.desc()).all()
    return render_template('listaFilmes.html', objects=filmes)


@app.route('/filmes/<int:id>')
def detalheFilme(id):
    filme = Filme.query.get(id)
    return render_template('detalheFilme.html', object=filme)


@app.route('/novoUsuario', methods=['GET', 'POST'])
def newUser():
    form = UserForm()
    if form.validate_on_submit():
        user = form.getUser()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('novoUsuario.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('login.html', form=form)
