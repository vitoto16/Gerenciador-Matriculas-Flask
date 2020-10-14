from flask import render_template, redirect, url_for, flash, request
from gerenciador_matriculas import app, db
from gerenciador_matriculas.forms import FormAluno, FormCurso, FormMatricula
from gerenciador_matriculas.models import Aluno, Curso, Matricula

MATRICULAS_STATUS_CHOICES=['ativado', 'bloqueado', 'cancelado']

@app.route('/', methods=['GET', 'POST'])
def home():
    alunos = Aluno.query.all()
    cursos = Curso.query.all()
    form = FormMatricula()
    form.aluno.choices = alunos
    form.curso.choices = cursos
    if form.validate_on_submit():
        alunoId = Aluno.query.filter_by(email=form.aluno.data).first().id
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
        if form.status.data == 'Ativo(a)':
            aluno.status = True

        db.session.add(aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('cadastro-aluno.html', form=form, title='Cadastro Aluno', legend='Cadastro de Aluno')


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
    return render_template('cadastro-curso.html', form=form, title='Cadastro Curso')


@app.route("/aluno/<int:aluno_id>", methods=['GET', 'POST'])
def edita_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    form = FormAluno()
    if form.validate_on_submit():
        aluno.nome = form.nome.data
        aluno.cpf = form.cpf.data
        aluno.email = form.email.data
        if form.status.data == 'Ativo(a)':
            aluno.status = True
        else:
            aluno.status = False
        aluno.dataNascimento = form.dataNascimento.data
        db.session.commit()
        flash('Aluno modificado com sucesso!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.nome.data = aluno.nome
        form.cpf.data = aluno.cpf
        form.email.data = aluno.email
        form.dataNascimento.data = aluno.dataNascimento
        form.status.default = aluno.status
    return render_template('cadastro-aluno.html', aluno=aluno, form=form,
                           title=aluno.nome, legend='Editar Aluno', submit='Modificar')

@app.route("/curso/<slug>", methods=['GET', 'POST'])
def edita_curso(slug):
    curso = Curso.query.filter_by(slug=slug).first()
    form = FormCurso()
    if form.validate_on_submit():
        curso.nome = form.nome.data
        curso.sequencia = form.sequencia.data
        curso.precoVenda = form.precoVenda.data
        if form.status.data == 'Ativo':
            curso.status = True
        else:
            curso.status = False
        db.session.commit()
        flash('Curso modificado com sucesso!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.nome.data = curso.nome
        form.sequencia.data = curso.sequencia
        form.precoVenda.data = curso.precoVenda
        form.status.default = curso.status
    return render_template('cadastro-curso.html', curso=curso, form=form,
                           title=curso.nome, legend='Editar Curso', submit='Modificar')

@app.route('/deleta-aluno/<int:aluno_id>', methods=['GET', 'POST'])
def deleta_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    db.session.delete(aluno)
    db.session.commit()
    flash('Aluno deletado com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/deleta-curso/<slug>', methods=['GET', 'POST'])
def deleta_curso(slug):
    curso = Curso.query.filter_by(slug=slug).first_or_404()
    db.session.delete(curso)
    db.session.commit()
    flash('Curso deletado com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/ativa-matricula/<int:matricula_id>')
def ativa_matricula(matricula_id):
    matricula = Matricula.query.get_or_404(matricula_id)
    if matricula.status != 'Matriculado':
        matricula.status = 'Matriculado'
        db.session.commit()
        flash("Matrícula ativada com sucesso!", 'success')
        return redirect(url_for('home'))
    else:
        flash("Esta matrícula já está ativa!", 'danger')

@app.route('/bloqueia-matricula/<int:matricula_id>')
def bloqueia_matricula(matricula_id):
    matricula = Matricula.query.get_or_404(matricula_id)
    if matricula.status != 'Bloqueado':
        matricula.status = 'Bloqueado'
        db.session.commit()
        flash("Matrícula bloqueada com sucesso!", 'success')
        return redirect(url_for('home'))
    else:
        flash("Esta matrícula já está bloqueada!", 'danger')

@app.route('/cancela-matricula/<int:matricula_id>')
def cancela_matricula(matricula_id):
    matricula = Matricula.query.get_or_404(matricula_id)
    if matricula.status != 'Cancelado':
        matricula.status = 'Cancelado'
        db.session.commit()
        flash("Matrícula cancelada com sucesso!", 'success')
        return redirect(url_for('home'))
    else:
        flash("Esta matrícula já está cancelada!", 'danger')
