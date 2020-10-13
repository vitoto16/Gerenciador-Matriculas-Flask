from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from gerenciador_matriculas.models import Aluno, Curso, Matricula


class FormAluno(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=35)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dataNascimento = DateField('Data de Nascimento (dd/mm/aaaa) ', validators=[DataRequired()], format='%d/%m/%Y')
    submit = SubmitField('Cadastrar')

    def validate_cpf(self, cpf):
        aluno = Aluno.query.filter_by(cpf=cpf.data).first()
        if aluno:
            raise ValidationError("Este cpf já está cadastrado!")

    def validate_email(self, email):
        aluno = Aluno.query.filter_by(email=email.data).first()
        if aluno:
            raise ValidationError("Este e-mail já está cadastrado!")


class FormCurso(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=35)])
    sequencia = IntegerField('Sequencia', validators=[DataRequired()])
    precoVenda = FloatField('Preco de Venda', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

    def validate_nome(self, nome):
        curso = Curso.query.filter_by(nome=nome.data).first()
        if curso:
            raise ValidationError("Este curso já está cadastrado!")

def validate_matricula(form, aluno):
    curso = Curso.query.filter_by(nome=form.curso.data).first()
    aluno_selecionado = Aluno.query.filter_by(email=aluno.data).first()
    matriculado = Matricula.query.filter_by(alunoId=aluno_selecionado.id, cursoId=curso.id).first()
    if matriculado:
        raise ValidationError("Este aluno já está cadastrado neste curso!")

class FormMatricula(FlaskForm):
    aluno = SelectField('Alunos Cadastrados', choices=Aluno.query.all(), validators=[validate_matricula])
    curso = SelectField('Cursos Cadastrados', choices=Curso.query.all())
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

