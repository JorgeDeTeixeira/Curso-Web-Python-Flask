from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, PasswordField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app import db, bcrypt, app
from werkzeug.utils import secure_filename
import os

from app.models import Filme, User, FilmeComentario


class FilmeForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    ano = IntegerField('Ano', validators=[DataRequired()])
    resumo = TextAreaField('Resumo', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def validateTitulo(self, titulo):
        if Filme.query.filter_by(titulo=titulo.data).first():
            raise ValidationError('Este filme já foi incluso!')

    def save(self):
        arquivo = self.imagem.data
        nomeSeguro = secure_filename(arquivo.filename)
        caminho = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'],
            'filmes',
            nomeSeguro
        )

        filme = Filme(
            titulo=self.titulo.data,
            ano=self.ano.data,
            resumo=self.resumo.data,
            imagem=nomeSeguro
        )

        arquivo.save(caminho)
        db.session.add(filme)
        db.session.commit()


class UserForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    senhaConfirmacao = PasswordField('Confirme a senha', validators=[
                                     DataRequired(), EqualTo('senha')])
    submit = SubmitField('Salvar')

    def validateUsername(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username já utilizado, por utilize outro!')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data)
        user = User(
            email=self.email.data,
            username=self.username.data,
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            password=senha
        )
        db.session.add(user)
        db.session.commit()

    def getUser(self):
        self.save()
        return User.query.filter_by(username=self.username.data).first()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, self.senha.data):
                return user
            else:
                raise Exception('Senha incorreta!')
        else:
            raise Exception("Usuário não encontrado!")


class FilmeComentarioForm(FlaskForm):
    comentario = TextAreaField('Comentário', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def save(self, idFilme, idUser):
        comentario = FilmeComentario(
            comentario=self.comentario.data,
            idFilme=idFilme,
            idUser=idUser
        )

        db.session.add(comentario)
        db.session.commit()
