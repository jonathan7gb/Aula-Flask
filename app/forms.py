from flask_wtf import FlaskForm
from app import bcrypt
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import db
from app.models import Contato, User

class userForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    btnCadastrar = SubmitField('Cadastrar')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Usuário já cadastrado com esse Email!")

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = User(
            nome = self.nome.data,
            email = self.email.data,
            sobrenome = self.sobrenome.data,
            senha = senha
        )
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Logar')

    def login(self):
        user = User.query.filter_by(email=self.email.data.first())
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode()):
                return user
            else:
                raise Exception("Senha Incorreta!")
        else:
            raise Exception("Usuário não encontrado!!")






class contatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )
        db.session.add(contato)
        db.session.commit()

