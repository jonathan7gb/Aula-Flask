from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

from app import db
from app.models import contato

class contatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')
    
    def save(self):
        contato2 = contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )
        db.session.add(contato2)
        db.session.commit()