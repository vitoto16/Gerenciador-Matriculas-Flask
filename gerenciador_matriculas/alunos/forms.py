from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from gerenciador_matriculas.models import Aluno


def valida_campos_aluno(form, field):
    if field.name == 'cpf':
        aluno = Aluno.query.filter_by(cpf=field.data).first()
        print(field.name, field.data)
    elif field.name == 'email':
        aluno = Aluno.query.filter_by(email=field.data).first()
    else:
        aluno = Aluno.query.first()

    route_editar = '/aluno/'
    route_request = request.path
    if route_editar in route_request:
        aluno_editado_id = route_request.split('/')[2]
        aluno_editado = Aluno.query.get(aluno_editado_id)
        if aluno != aluno_editado:
            raise ValidationError(f"Este {field.name} já está cadastrado!")
    else:
        if aluno:
            raise ValidationError(f"Este {field.name} já está cadastrado!")


class FormAluno(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=35)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11), valida_campos_aluno])
    email = StringField('Email', validators=[DataRequired(), Email(), valida_campos_aluno])
    status = RadioField('Status', choices=['Ativo(a)', 'Inativo(a)'], validators=[DataRequired()])
    dataNascimento = DateField('Data de Nascimento (dd/mm/aaaa) ', validators=[DataRequired()], format='%d/%m/%Y')
    submit = SubmitField('Cadastrar')
