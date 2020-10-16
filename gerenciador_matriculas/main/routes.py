from flask import render_template, redirect, url_for, flash, abort, Blueprint
from gerenciador_matriculas import db
from gerenciador_matriculas.main.forms import FormMatricula
from gerenciador_matriculas.models import Aluno, Curso, Matricula, Gerente
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('main.home'))
        return render_template('matriculas.html', alunos=alunos, cursos=cursos, form=form)
    else:
        return render_template('matriculas.html', form=form)


@main.route('/ativa-matricula/<int:matricula_id>')
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
            return redirect(url_for('main.home'))
        else:
            flash("Esta matrícula já está ativa!", 'danger')
            return redirect(url_for('main.home'))


@main.route('/bloqueia-matricula/<int:matricula_id>')
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
            return redirect(url_for('main.home'))
        else:
            flash("Esta matrícula já está bloqueada!", 'danger')
            return redirect(url_for('main.home'))


@main.route('/cancela-matricula/<int:matricula_id>')
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
            return redirect(url_for('main.home'))
        else:
            flash("Esta matrícula já está cancelada!", 'danger')
            return redirect(url_for('main.home'))
