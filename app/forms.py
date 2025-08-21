from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import db, bcrypt, app
from app.models import Contato, User, Post, PostComentarios

import os
from werkzeug.utils import secure_filename

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
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Logar')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
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

class PostForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        imagem = self.imagem.data
        nome_seguro = secure_filename(imagem.filename)

        pasta_post = os.path.join(app.config['UPLOAD_FILES'], 'post')
        os.makedirs(pasta_post, exist_ok=True)

        caminho = os.path.join(pasta_post, nome_seguro)

        imagem.save(caminho)

        post = Post(
            mensagem=self.mensagem.data,
            user_id=user_id,
            imagem=nome_seguro
        )

        db.session.add(post)
        db.session.commit()

class PostComentarioForm(FlaskForm):
     comentario = StringField('Comentario', validators=[DataRequired()])
     btnSubmit = SubmitField('Enviar')

     def save(self, user_id, post_id):
        comentario = PostComentarios (
             comentario=self.comentario.data,
             user_id= user_id,
             post_id = post_id
        )

        db.session.add(comentario)
        db.session.commit()
