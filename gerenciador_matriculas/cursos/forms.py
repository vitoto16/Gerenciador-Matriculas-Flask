from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError
from gerenciador_matriculas.models import Curso


class FormCurso(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=35)])
    sequencia = IntegerField('Sequencia', validators=[DataRequired()])
    status = RadioField('Status', choices=['Ativo', 'Inativo'], default='Inativo')
    precoVenda = FloatField('Preco de Venda', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

    def validate_nome(self, nome):
        curso = Curso.query.filter_by(nome=nome.data).first()
        route_editar = '/curso/'
        route_request = request.path
        if route_editar in route_request:
            curso_editado_slug = route_request.split('/')[2]
            curso_editado = Curso.query.filter_by(slug=curso_editado_slug).first()
            if curso != curso_editado:
                raise ValidationError("Este curso já está cadastrado!")
        else:
            if curso:
                raise ValidationError("Este curso já está cadastrado!")
