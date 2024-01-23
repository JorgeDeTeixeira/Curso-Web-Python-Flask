from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from app import db

from app.models import Filme


class FilmeForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    ano = IntegerField('Ano', validators=[DataRequired()])
    resumo = TextAreaField('Resumo', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def validateTitulo(self, titulo):
        if Filme.query.filter_by(titulo=titulo.data).first():
            raise ValidationError('Este filme já foi incluso!')

    def save(self):
        filme = Filme(
            titulo=self.titulo.data,
            ano=self.ano.data,
            resumo=self.resumo.data
        )

        db.session.add(filme)
        db.session.commit()
