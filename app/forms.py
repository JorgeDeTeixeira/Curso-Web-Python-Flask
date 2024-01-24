from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app import db, bcrypt

from app.models import Filme, User


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