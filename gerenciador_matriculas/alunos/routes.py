from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from gerenciador_matriculas import db
from gerenciador_matriculas.alunos.forms import FormAluno
from gerenciador_matriculas.models import Aluno
from flask_login import current_user, login_required

alunos = Blueprint('alunos', __name__)


@alunos.route('/cadastro-aluno', methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))

    return render_template('cadastro-aluno.html', form=form, title='Cadastro Aluno', legend='Cadastro de Aluno')


@alunos.route("/aluno/<int:aluno_id>", methods=['GET', 'POST'])
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
            return redirect(url_for('main.home'))
        elif request.method == 'GET':
            form.nome.data = aluno.nome
            form.cpf.data = aluno.cpf
            form.email.data = aluno.email
            form.dataNascimento.data = aluno.dataNascimento
            form.status.default = aluno.status
        return render_template('cadastro-aluno.html', aluno=aluno, form=form,
                               title=aluno.nome, legend='Editar Aluno', submit='Modificar')


@alunos.route('/deleta-aluno/<int:aluno_id>', methods=['GET', 'POST'])
@login_required
def deleta_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    if aluno.gerente != current_user:
        abort(403)
    else:
        db.session.delete(aluno)
        db.session.commit()
        flash('Aluno deletado com sucesso!', 'success')
        return redirect(url_for('main.home'))
