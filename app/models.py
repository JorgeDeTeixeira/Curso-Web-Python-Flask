from app import db
from datetime import datetime


class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataCriacao = db.Column(db.DateTime, nullable=True,
                            default=datetime.utcnow())
    titulo = db.Column(db.String(50), nullable=True)
    ano = db.Column(db.Integer, nullable=True)
    resumo = db.Column(db.String(1000), nullable=True)
