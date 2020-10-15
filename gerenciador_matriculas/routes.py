from flask import render_template, redirect, url_for, flash, request, abort, jsonify
from gerenciador_matriculas import app, db, bcrypt
from gerenciador_matriculas.forms import FormAluno, FormCurso, FormMatricula, FormRegistrar, FormLogin
from gerenciador_matriculas.models import Aluno, Curso, Matricula, Gerente
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = FormRegistrar()
    if form.validate_on_submit():
        flash(f"Usuário {form.username.data} criado!", 'success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        gerente = Gerente(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(gerente)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registrar.html', form=form, title='Registrar')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = FormLogin()
    if form.validate_on_submit():
        user = Gerente.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login não realizado. Verifique seu nome de usuário e senha.', 'danger')
    return render_template('login.html', form=form, title='Login')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = FormMatricula()
    if current_user.is_authenticated:
        gerente = Gerente.query.get(current_user.get_id())
        alunos = gerente.alunos
        cursos = gerente.cursos
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
    else:
        return render_template('matriculas.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/cadastro-aluno', methods=['GET', 'POST'])
@login_required
def cadastro_aluno():
    form = FormAluno()
    if form.validate_on_submit():
        aluno = Aluno(nome=form.nome.data,
                      cpf=form.cpf.data,
                      email=form.email.data,
                      dataNascimento=form.dataNascimento.data,
                      gerente=current_user
                      )
        if form.status.data == 'Ativo(a)':
            aluno.status = True

        db.session.add(aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('cadastro-aluno.html', form=form, title='Cadastro Aluno', legend='Cadastro de Aluno')


@app.route('/cadastro-curso', methods=['GET', 'POST'])
@login_required
def cadastro_curso():
    form = FormCurso()
    if form.validate_on_submit():
        curso = Curso(nome=form.nome.data,
                      sequencia=form.sequencia.data,
                      precoVenda=form.precoVenda.data,
                      gerente=current_user
                      )
        if form.status.data == 'Ativo':
            curso.status = True
        db.session.add(curso)
        db.session.commit()
        flash('Curso cadastrado com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('cadastro-curso.html', form=form, title='Cadastro Curso')


@app.route("/aluno/<int:aluno_id>", methods=['GET', 'POST'])
@login_required
def edita_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    if aluno.gerente != current_user:
        abort(403)
    else:
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
@login_required
def edita_curso(slug):
    curso = Curso.query.filter_by(slug=slug).first()
    if curso.gerente != current_user:
        abort(403)
    else:
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
@login_required
def deleta_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    if aluno.gerente != current_user:
        abort(403)
    else:
        db.session.delete(aluno)
        db.session.commit()
        flash('Aluno deletado com sucesso!', 'success')
        return redirect(url_for('home'))

@app.route('/deleta-curso/<slug>', methods=['GET', 'POST'])
@login_required
def deleta_curso(slug):
    curso = Curso.query.filter_by(slug=slug).first_or_404()
    if curso.gerente != current_user:
        abort(403)
    else:
        db.session.delete(curso)
        db.session.commit()
        flash('Curso deletado com sucesso!', 'success')
        return redirect(url_for('home'))

@app.route('/ativa-matricula/<int:matricula_id>')
@login_required
def ativa_matricula(matricula_id):
    matricula = Matricula.query.get_or_404(matricula_id)
    if matricula.aluno.gerente != current_user:
        abort(403)
    else:
        if matricula.status != 'Matriculado':
            matricula.status = 'Matriculado'
            db.session.commit()
            flash("Matrícula ativada com sucesso!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Esta matrícula já está ativa!", 'danger')
            return redirect(url_for('home'))

@app.route('/bloqueia-matricula/<int:matricula_id>')
@login_required
def bloqueia_matricula(matricula_id):
    matricula = Matricula.query.get_or_404(matricula_id)
    if matricula.aluno.gerente != current_user:
        abort(403)
    else:
        if matricula.status != 'Bloqueado':
            matricula.status = 'Bloqueado'
            db.session.commit()
            flash("Matrícula bloqueada com sucesso!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Esta matrícula já está bloqueada!", 'danger')
            return redirect(url_for('home'))

@app.route('/cancela-matricula/<int:matricula_id>')
@login_required
def cancela_matricula(matricula_id):
    matricula = Matricula.query.get_or_404(matricula_id)
    if matricula.aluno.gerente != current_user:
        abort(403)
    else:
        if matricula.status != 'Cancelado':
            matricula.status = 'Cancelado'
            db.session.commit()
            flash("Matrícula cancelada com sucesso!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Esta matrícula já está cancelada!", 'danger')
            return redirect(url_for('home'))

@app.route('/api/aluno/<int:aluno_id>')
@login_required
def alunos_all(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    gerente = aluno.gerente
    if gerente == current_user:
        return jsonify(aluno.serialize())
