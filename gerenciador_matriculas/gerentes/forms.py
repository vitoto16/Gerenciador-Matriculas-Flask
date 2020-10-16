from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from gerenciador_matriculas.models import Gerente


class FormRegistrar(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=4, max=35)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        gerente = Gerente.query.filter_by(username=username.data).first()
        if gerente:
            raise ValidationError("Este nome de usuário já está sendo usado!")

    def validate_email(self, email):
        gerente = Gerente.query.filter_by(email=email.data).first()
        if gerente:
            raise ValidationError("Este e-mail já está sendo usado!")


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')
