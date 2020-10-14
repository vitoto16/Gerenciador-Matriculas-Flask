from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, FloatField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from gerenciador_matriculas.models import Aluno, Curso, Matricula


def asserting_uniques(form, field):
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
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11), asserting_uniques])
    email = StringField('Email', validators=[DataRequired(), Email(), asserting_uniques])
    status = RadioField('Status', choices=['Ativo(a)', 'Inativo(a)'], validators=[DataRequired()])
    dataNascimento = DateField('Data de Nascimento (dd/mm/aaaa) ', validators=[DataRequired()], format='%d/%m/%Y')
    submit = SubmitField('Cadastrar')


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


def validate_matricula(form, aluno):
    curso = Curso.query.filter_by(nome=form.curso.data).first()
    aluno_selecionado = Aluno.query.filter_by(email=aluno.data).first()
    matriculado = Matricula.query.filter_by(alunoId=aluno_selecionado.id, cursoId=curso.id).first()
    if matriculado:
        raise ValidationError("Este aluno já está matriculado neste curso!")


class FormMatricula(FlaskForm):
    aluno = SelectField('Alunos Cadastrados', validators=[DataRequired(), validate_matricula])
    curso = SelectField('Cursos Cadastrados', validators=[DataRequired()])
    ano = StringField('Ano', validators=[DataRequired()])
    submit = SubmitField('Matricular')

    def validate_aluno(self, aluno):
        selecionado = Aluno.query.filter_by(email=aluno.data).first()
        if not selecionado.status:
            raise ValidationError("O cadastro deste aluno não está ativo!")

    def validate_curso(self, curso):
        selecionado = Curso.query.filter_by(nome=curso.data).first()
        if not selecionado.status:
            raise ValidationError("O cadastro deste curso não está ativo!")
