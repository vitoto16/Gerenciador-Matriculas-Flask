from datetime import datetime
from slugify import slugify
from gerenciador_matriculas import db


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(35), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.Boolean(35), default=False)
    dataNascimento = db.Column(db.DateTime, nullable=False)

    matriculas = db.relationship('Matricula', backref='aluno', lazy=True)

    def __repr__(self):
        return f"Aluno(nome='{self.nome}', cpf='{self.cpf}', email='{self.email}'," \
               f"status='{self.status}', dataNascimento='{self.dataNascimento}')"

    def __str__(self):
        return self.email

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(35), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=False)
    slug = db.Column(db.String(35), unique=True, nullable=False)
    sequencia = db.Column(db.Integer, nullable=False)
    precoVenda = db.Column(db.Float)
    dataCadastro = db.Column(db.DateTime, default=datetime.utcnow)

    matriculas = db.relationship('Matricula', backref='curso', lazy=True)

    def __repr__(self):
        return f"Curso(nome='{self.nome}', slug='{self.slug}', status='{self.status}', sequencia='{self.sequencia}')"

    def __str__(self):
        return self.nome

    @staticmethod
    def slugify(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


db.event.listen(Curso.nome, 'set', Curso.slugify, retval=False)


class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), default='bloqueado')
    ano = db.Column(db.String(5), nullable=False)
    dataCadastro = db.Column(db.DateTime, default=datetime.utcnow())

    alunoId = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    cursoId = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

    def __repr__(self):
        return f"Matricula(alunoId='{self.alunoId}', cursoId='{self.cursoId}', dataCadastro='{self.dataCadastro}')"
