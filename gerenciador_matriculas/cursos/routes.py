from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from gerenciador_matriculas import db
from gerenciador_matriculas.cursos.forms import FormCurso
from gerenciador_matriculas.models import Curso
from flask_login import current_user, login_required

cursos = Blueprint('cursos', __name__)


@cursos.route('/cadastro-curso', methods=['GET', 'POST'])
@login_required
def cadastro_curso():
    form = FormCurso()
    if form.validate_on_submit():
        curso = Curso(nome=form.nome.data,
                      sequencia=form.sequencia.data,
                      status=form.status,
                      precoVenda=form.precoVenda.data,
                      gerente=current_user
                      )
        db.session.add(curso)
        db.session.commit()
        flash('Curso cadastrado com sucesso!', 'success')
        return redirect(url_for('main.home'))

    return render_template('cadastro-curso.html', form=form, title='Cadastro Curso')


@cursos.route("/curso/<slug>", methods=['GET', 'POST'])
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
            return redirect(url_for('main.home'))
        elif request.method == 'GET':
            form.nome.data = curso.nome
            form.sequencia.data = curso.sequencia
            form.precoVenda.data = curso.precoVenda
            form.status.default = curso.status
        return render_template('cadastro-curso.html', curso=curso, form=form,
                               title=curso.nome, legend='Editar Curso', submit='Modificar')


@cursos.route('/deleta-curso/<slug>', methods=['GET', 'POST'])
@login_required
def deleta_curso(slug):
    curso = Curso.query.filter_by(slug=slug).first_or_404()
    if curso.gerente != current_user:
        abort(403)
    else:
        db.session.delete(curso)
        db.session.commit()
        flash('Curso deletado com sucesso!', 'success')
        return redirect(url_for('main.home'))
