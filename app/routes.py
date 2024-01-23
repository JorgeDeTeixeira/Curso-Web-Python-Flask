from flask import render_template, url_for, jsonify
from app import app


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
