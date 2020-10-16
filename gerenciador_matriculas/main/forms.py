from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from gerenciador_matriculas.models import Aluno, Curso, Matricula


def validate_matricula(form, aluno):
    curso = Curso.query.filter_by(nome=form.curso.data).first()
    aluno_selecionado = Aluno.query.filter_by(email=aluno.data).first()
    matriculas = Matricula.query.filter_by(aluno=aluno_selecionado, curso=curso).all()
    for matricula in matriculas:
        if matricula and matricula.status != 'Cancelado':
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
