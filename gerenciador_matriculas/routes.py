from flask import render_template, redirect, url_for, flash
from gerenciador_matriculas import app, db
from gerenciador_matriculas.forms import FormAluno, FormCurso, FormMatricula
from gerenciador_matriculas.models import Aluno, Curso, Matricula

@app.route('/', methods=['GET', 'POST'])
def home():
    alunos = Aluno.query.all()
    cursos = Curso.query.all()
    form = FormMatricula()
    if form.validate_on_submit():
        alunoId = Aluno.query.filter_by(nome=form.aluno.data).first().id
        cursoId = Curso.query.filter_by(nome=form.curso.data).first().id
        matricula = Matricula(alunoId=alunoId,
                              cursoId=cursoId,
                              ano=form.ano.data
                              )
        db.session.add(matricula)
        db.session.commit()
        flash('Matrícula efetuada com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('matriculas.html', alunos=alunos, cursos=cursos, form=form)


@app.route('/cadastro-aluno', methods=['GET', 'POST'])
def cadastro_aluno():
    form = FormAluno()
    if form.validate_on_submit():
        aluno = Aluno(nome=form.nome.data,
                      cpf=form.cpf.data,
                      email=form.email.data,
                      dataNascimento=form.dataNascimento.data
                      )
        db.session.add(aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('cadastro-aluno.html', form=form)


@app.route('/cadastro-curso', methods=['GET', 'POST'])
def cadastro_curso():
    form = FormCurso()
    if form.validate_on_submit():
        curso = Curso(nome=form.nome.data,
                      sequencia=form.sequencia.data,
                      precoVenda=form.precoVenda.data,
                      )
        db.session.add(curso)
        db.session.commit()
        flash('Curso cadastrado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('cadastro-curso.html', form=form)
