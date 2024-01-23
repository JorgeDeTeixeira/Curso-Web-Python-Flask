from flask import render_template, url_for
from app import app


@app.route("/")
def homepage():
    context = {
        'usuario': 'Jorge',
        'idade': 20
    }
    return render_template('index.html', context=context)
