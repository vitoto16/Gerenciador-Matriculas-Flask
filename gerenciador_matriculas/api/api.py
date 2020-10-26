from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from gerenciador_matriculas.models import Aluno, Curso, Gerente, Matricula

api = Blueprint('api', '__name__')

@api.route('/api/alunos')
@login_required
def get_alunos():
    alunos = Aluno.query.filter_by(gerente=current_user).all()

    return jsonify([aluno.serialize() for aluno in alunos])


@api.route('/api/cursos')
@login_required
def get_cursos():
    cursos = Curso.query.filter_by(gerente=current_user).all()

    return jsonify([curso.serialize() for curso in cursos])
